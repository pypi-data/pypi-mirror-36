# -*- coding: utf-8 -*-

import pydoc
from abc import ABCMeta, abstractmethod
from enum import Enum
from lxml import etree
from ..misc import get_boolean, evaluate


def is_expression(value: str) -> bool:
    if isinstance(value, str):
        s = value.strip()
        if s.startswith("#{"):
            if s.endswith("}"):
                return True
            else:
                raise ValueError("Expression should starts with '#{' and ends with '}'")
    return False


class Scope(Enum):
    PROTOTYPE = "prototype"
    SINGLETON = "singleton"

    @classmethod
    def value_of(cls, s):
        if s == "prototype":
            return cls.PROTOTYPE
        elif s == "singleton":
            return cls.SINGLETON
        else:
            raise AttributeError


class InvalidObjectScope(Exception):
    pass


class BaseParser(metaclass=ABCMeta):
    NAMESPACE = None

    @abstractmethod
    def parse(self, element, container):
        pass


class NamespaceHandler(metaclass=ABCMeta):
    parsers = {}

    @property
    @abstractmethod
    def NAMESPACE(self):
        pass

    def parse(self, element, container):
        return self.find_parser(element).parse(element, container)

    def find_parser(self, element):
        parser = self.parsers.get(etree.QName(element).localname)
        if parser is None:
            msg = "Can't find parser for %s." % element
            raise KeyError(msg)
        return parser

    def register_parser(self, element_name, parser):
        self.parsers[element_name] = parser


class BaseDef(metaclass=ABCMeta):
    @abstractmethod
    def get_actual_value(self, container, extra_map=None):
        raise NotImplementedError


class ValueDef(BaseDef):
    def __init__(self, value):
        self.value = value

    def get_actual_value(self, container, extra_map=None):
        return self.value


class ObjectDef(BaseDef):
    def __init__(self, id, cls, scope=Scope.SINGLETON, lazy_init=False):
        super(ObjectDef, self).__init__()
        self.id = id
        self.cls = cls
        self.scope = scope
        self.lazy_init = lazy_init
        self.args = []
        self.kwargs = {}
        self.props = {}
        self.value = None   # will be set when scope is SINGLETON.

    def get_actual_value(self, container, extra_map=None):
        if self.id is None:
            if self.scope == Scope.SINGLETON:
                value = getattr(self, "value", None)
                if value is None:
                    value = container.create_object(self)
                    self.value = value
                return value
            elif self.scope == Scope.PROTOTYPE:
                value = container.create_object(self)
                return value
            else:
                raise InvalidObjectScope
        return container.get_object(self.id)

    def __repr__(self):
        return "<ObjectDef(id:%s, class:%s, scope:%s, lazy_init=%s)>" % (self.id, self.cls, self.scope, self.lazy_init)


class BasicValueDef(ValueDef):
    def __init__(self, value, type):
        if type not in (str, int, float, bool):
            raise ValueError
        super(BasicValueDef, self).__init__(value)
        self.type = type

    def get_actual_value(self, container, extra_map=None):
        if self.value is None:
            return None

        if self.type is str:
            return self.value
        elif self.type is bool:
            return get_boolean(self.value)
        else:
            return self.type(self.value)


class CallableValueDef(ValueDef):
    def get_actual_value(self, container, extra_map=None):
        return pydoc.locate(self.value)


class EvaluateValueDef(ValueDef):
    def __init__(self, value, type=object, scoped=False):
        if type not in (str, int, float, bool, object):
            raise ValueError
        if is_expression(value):
            value = value[2:-1]
        super(EvaluateValueDef, self).__init__(value)
        self.type = type
        self.scoped = scoped

    def get_actual_value(self, container, extra_map=None):
        extra_map = extra_map or {}
        local_context = dict()
        if not self.scoped:
            local_context.update(container.objects)
            local_context.update(extra_map)
        value = evaluate(self.value, globals(), local_context)
        if not isinstance(value, self.type):
            raise ValueError("evaluate result is not an instance of type '%s'" % self.type)
        return value


class ReferenceValueDef(ValueDef):
    def get_actual_value(self, container, extra_map=None):
        if extra_map is not None and self.value in extra_map:
            return extra_map[self.value]
        return container.get_object(self.value)


class ListValueDef(ValueDef):
    def get_actual_value(self, container, extra_map=None):
        for i in range(len(self.value)):
            if isinstance(self.value[i], BaseDef):
                self.value[i] = self.value[i].get_actual_value(container, extra_map)
        return self.value


class DictValueDef(ValueDef):
    def get_actual_value(self, container, extra_map=None):
        for k in self.value.keys():
            v = self.value[k]
            if isinstance(v, BaseDef):
                value = v.get_actual_value(container, extra_map)
            elif isinstance(v, list):
                value = ListValueDef(v).get_actual_value(container, extra_map)
            elif isinstance(v, dict):
                value = DictValueDef(v).get_actual_value(container, extra_map)
            elif is_expression(v):
                value = EvaluateValueDef(v, object).get_actual_value(container, extra_map)
            else:
                value = v
            self.value[k] = value
        return self.value
