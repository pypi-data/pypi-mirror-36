import warnings
from collections import defaultdict, OrderedDict
from functools import partial, update_wrapper
from contextlib import contextmanager

from .utils import add_metaclass, ensure_iterable, Mapping

from .xml import (
    id_maker, CVParam, UserParam,
    ParamGroupReference, _element)


class ChildTrackingMeta(type):
    def __new__(cls, name, parents, attrs):
        if not hasattr(cls, "_cache"):
            cls._cache = defaultdict(dict)
        new_type = type.__new__(cls, name, parents, attrs)
        ns = getattr(new_type, "component_namespace", None)
        cls._cache[ns][name] = new_type
        return new_type

    @classmethod
    def resolve_component(self, namespace, name):
        try:
            return self._cache[namespace][name]
        except KeyError:
            return self._cache[None][name]


class SpecializedContextCache(OrderedDict):
    def __init__(self, type_name):
        super(SpecializedContextCache, self).__init__()
        self.type_name = type_name
        self.bijection = dict()

    def __getitem__(self, key):
        try:
            item = dict.__getitem__(self, key)
            return item
        except KeyError:
            if key is None:
                return None
            warnings.warn("No reference was found for %r in %s" % (key, self.type_name), stacklevel=3)
            new_value = id_maker(self.type_name, key)
            self[key] = new_value
            return new_value

    def __setitem__(self, key, value):
        super(SpecializedContextCache, self).__setitem__(key, value)
        self.bijection[value] = key

    def __repr__(self):
        return '%s\n%s' % (self.type_name, dict.__repr__(self))


class VocabularyResolver(object):
    def __init__(self, vocabularies=None):
        self.vocabularies = vocabularies

    def get_vocabulary(self, id):
        for vocab in self.vocabularies:
            if vocab.id == id:
                return vocab
            try:
                if vocab.full_name == id:
                    return vocab
            except AttributeError:
                pass
        raise KeyError(id)

    def param_group_reference(self, id):
        return ParamGroupReference(id)

    def param(self, name, value=None, cv_ref=None, **kwargs):
        accession = kwargs.get("accession")

        if isinstance(name, CVParam):
            return name
        elif isinstance(name, ParamGroupReference):
            return name
        elif isinstance(name, (tuple, list)) and value is None:
            name, value = name
        elif isinstance(name, Mapping):
            mapping = dict(name)
            if len(mapping) == 1 and 'ref' in mapping:
                return self.param_group_reference(mapping['ref'])
            value = value or mapping.pop('value', None)
            accession = accession or mapping.pop("accession", None)
            cv_ref = cv_ref or mapping.pop("cv_ref", None) or mapping.pop("cvRef", None)
            unit_name = mapping.pop("unit_name", None) or mapping.pop("unitName", None)
            unit_accession = mapping.pop("unit_accession", None) or mapping.pop("unitAccession", None)
            unit_cv_ref = mapping.pop('unit_cv_ref', None) or mapping.pop('unitCvRef', None)
            name = mapping.pop('name', None)
            if name is None:
                if len(mapping) == 1:
                    name, value = tuple(mapping.items())[0]
                else:
                    raise ValueError("Could not coerce parameter from %r" % (mapping,))
            else:
                kwargs.update({k: v for k, v in mapping.items()
                               if k not in (
                    "name", "value", "accession")})
                # case normalize unit information so that cvParam can detect them
                if unit_name is not None:
                    kwargs.setdefault("unit_name", unit_name)
                if unit_accession is not None:
                    kwargs.setdefault("unit_accession", unit_accession)
                if unit_cv_ref is not None:
                    kwargs.setdefault("unit_cv_ref", unit_cv_ref)
        unit_name = kwargs.get("unit_name")
        unit_accession = kwargs.get("unit_accession")
        unit_ref = kwargs.get('unit_cv_ref')
        if unit_name is not None or unit_accession is not None:
            if unit_accession is not None:
                unit_term, source = self.term(unit_accession, include_source=True)
                unit_name = unit_term.name
                unit_accession = unit_term.id
                unit_ref = source.id
            elif unit_name is not None:
                unit_term, source = self.term(unit_name, include_source=True)
                unit_name = unit_term.name
                unit_accession = unit_term.id
                unit_ref = source.id
            kwargs['unit_name'] = unit_name
            kwargs['unit_accession'] = unit_accession
            kwargs['unit_cv_ref'] = unit_ref

        if name is None:
            raise ValueError("Could not coerce parameter from %r, %r, %r" % (name, value, kwargs))
        if cv_ref is None:
            for cv in self.vocabularies:
                try:
                    term = cv[name]
                    name = term["name"]
                    accession = term["id"]
                    cv_ref = cv.id
                except KeyError:
                    pass
        if cv_ref is None:
            return UserParam(name=name, value=value, **kwargs)
        else:
            kwargs.setdefault("ref", cv_ref)
            kwargs.setdefault("accession", accession)
            return CVParam(name=name, value=value, **kwargs)

    def term(self, name, include_source=False):
        deferred = None
        for cv in self.vocabularies:
            try:
                term = cv[name]
                if term.get("is_obsolete", False):
                    deferred = term, cv
                    raise KeyError(name)
                if include_source:
                    return term, cv
                else:
                    return term
            except KeyError:
                pass
        else:
            if deferred:
                if include_source:
                    return deferred
                else:
                    return deferred[0]
            raise KeyError(name)

    def load_vocabularies(self):
        for vocab in self.vocabularies:
            vocab.load()

    def prepare_params(self, params):
        out = []
        for param in ensure_iterable(params):
            out.append(self.param(param))
        return out


class DocumentContext(dict, VocabularyResolver):
    def __init__(self, vocabularies=None):
        dict.__init__(self)
        VocabularyResolver.__init__(self, vocabularies)

    def param_group_reference(self, id):
        # This is a inelegant, as ReferenceableParamGroup is not part document type
        # independent, and may not be consistent
        param_group_index = self['ReferenceableParamGroup']
        return ParamGroupReference(param_group_index[id])

    def __getitem__(self, key):
        if not isinstance(key, str):
            if isinstance(key, (type, ReprBorrowingPartial)):
                key = key.__name__
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            if isinstance(key, (type, ReprBorrowingPartial)):
                key = key.__name__
        dict.__setitem__(self, key, value)

    def __missing__(self, key):
        if not isinstance(key, str):
            if isinstance(key, (type, ReprBorrowingPartial)):
                key = key.__name__
        self[key] = SpecializedContextCache(key)
        return self[key]


NullMap = DocumentContext()


class ReprBorrowingPartial(partial):
    """
    Create a partial instance that uses the wrapped callable's
    `__repr__` method instead of a generic partial
    """
    def __init__(self, func, *args, **kwargs):
        self._func = func
        # super(ReprBorrowingPartial, self).__init__(func, *args, **kwargs)
        update_wrapper(self, func)

    @property
    def type(self):
        return self._func

    def __repr__(self):
        return repr(self.func)

    def __getattr__(self, name):
        return getattr(self._func, name)

    def ensure(self, data):
        if not isinstance(data, self.type):
            return self(**data)
        else:
            if data.context is not self.context:
                raise ValueError("Cannot bind a component from another context")
        return data


class ComponentDispatcherBase(object):
    """
    A container for a :class:`DocumentContext` which provides
    an automatically parameterized version of all :class:`ComponentBase`
    types which use this instance's context.

    Attributes
    ----------
    context : :class:`DocumentContext`
        The mapping responsible for managing the global
        state of all created components.
    """
    def __init__(self, context=None, vocabularies=None, component_namespace=None):
        if vocabularies is None:
            vocabularies = []
        if context is None:
            context = DocumentContext(vocabularies=vocabularies)
        else:
            if vocabularies is not None:
                context.vocabularies.extend(vocabularies)
        self.component_namespace = component_namespace
        self.context = context

    def __getattr__(self, name):
        """
        Provide access to an automatically parameterized
        version of all :class:`ComponentBase` types which
        use this instance's context.

        Parameters
        ----------
        name : str
            Component Name

        Returns
        -------
        ReprBorrowingPartial
            A partially parameterized instance constructor for
            the :class:`ComponentBase` type requested.
        """
        component = ChildTrackingMeta.resolve_component(self.component_namespace, name)
        tp = ReprBorrowingPartial(component, context=self.context)
        tp.context = self.context
        return tp

    def ensure_component(self, data, tp):
        if isinstance(data, tp.type):
            if self.context is not data.context:
                raise ValueError("Cannot bind a component from another context")
            return data
        else:
            return tp(**data)

    def register(self, entity_type, id):
        """
        Pre-declare an entity in the document context. Ensures that
        a reference look up will be satisfied.

        Parameters
        ----------
        entity_type : str
            An entity type, either a tag name or a component name
        id : int
            The unique id number for the thing registered

        Returns
        -------
        str
            The constructed reference id
        """
        if isinstance(id, int):
            value = id_maker(entity_type, id)
        else:
            value = str(id)
        self.context[entity_type][id] = value
        return value

    @property
    def vocabularies(self):
        return self.context.vocabularies

    def load_vocabularies(self):
        self.context.load_vocabularies()

    def param(self, *args, **kwargs):
        return self.context.param(*args, **kwargs)

    def prepare_params(self, params):
        return self.context.prepare_params(params)

    def term(self, *args, **kwargs):
        return self.context.term(*args, **kwargs)

    def get_vocabulary(self, *args, **kwargs):
        return self.context.get_vocabulary(*args, **kwargs)

# ------------------------------------------
# Base Component Definitions


@add_metaclass(ChildTrackingMeta)
class ComponentBase(object):
    """A base class for all parts of an XML document which
    describe structures composed of more than a single XML
    tag without any children. In addition to wrapping additional
    descriptive data, this type's metaclass is :class:`ChildTrackingMeta`
    which enables :class:`ComponentDispatcherBase` to automatically bind
    a :class:`DocumentContext` object to the `context` paramter of the
    constructor of dynamically generated wrappers.

    Forwards any missing attribute requests to :attr:`element` for resolution
    against's the XML tag's attributes.
    """
    is_open = False
    _entering = None

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, key):
        if key == "element":
            raise AttributeError(
                ("The `element` attribute failed to instantiate "
                 "or is being accessed too early."))
        try:
            return self.element.attrs[key]
        except KeyError:
            raise AttributeError(key)

    def write(self, xml_file):
        raise NotImplementedError()

    @contextmanager
    def begin(self, xml_file=None, with_id=True):
        if xml_file is None:
            xml_file = getattr(self, "xml_file", None)
            if xml_file is None:
                raise ValueError("xml_file must be provided if this component is not bound!")
        self._entering = self.element(xml_file, with_id=with_id).__enter__()
        self.is_open = True
        yield

    def __call__(self, xml_file):
        self.write(xml_file)

    def __repr__(self):
        return "%s\n%s" % (
            self.element, "\n".join([
                "  %s: %r" % (k, v) for k, v in self.__dict__.items()
                if k not in ("context", "element") and not k.startswith("_")])
        )

    def prepare_params(self, params, **kwargs):
        if isinstance(params, Mapping):
            if ("name" not in params and "accession" not in params) and ("ref" not in params):
                params = list(params.items())
            else:
                params = [params]
        elif isinstance(params, (list, tuple)):
            params = list(params)
        else:
            params = list(ensure_iterable(params)) or []
        params.extend(kwargs.items())
        return params

    def add_param(self, param):
        if isinstance(param, list):
            self.params.extend(param)
        else:
            self.params.append(param)
        return self

    def write_params(self, xml_file, params=None):
        if params is None:
            params = self.params
        params = self.prepare_params(params)
        user_params = []
        cv_params = []
        references = []
        for param in params:
            param = self.context.param(param)
            if isinstance(param, ParamGroupReference):
                references.append(param)
            elif isinstance(param, UserParam):
                user_params.append(param)
            else:
                cv_params.append(param)
        for param in (references + cv_params + user_params):
            param(xml_file)


class ParameterContainer(ComponentBase):
    """An base class for a component whose only purpose
    is to contain one or more cv- or userParams.

    Attributes
    ----------
    context : DocumentContext
        The document metadata store
    element : lxml.etree.Element
        The XML tag object to be written
    params : list
        The list of parameters to include
    """
    def __init__(self, tag_name, params=None, element_args=None, context=NullMap, **kwargs):
        if element_args is None:
            element_args = dict()
        if params is None:
            params = []
        self.params = self.prepare_params(params, **kwargs)
        self.context = context
        self.element = _element(tag_name, **element_args)

    def write(self, xml_file):
        with self.element(xml_file, with_id=False):
            for param in self.params:
                self.context.param(param)(xml_file)


class IDParameterContainer(ParameterContainer):
    def write(self, xml_file):
        with self.element(xml_file, with_id=True):
            for param in self.params:
                self.context.param(param)(xml_file)
