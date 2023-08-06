# -*- coding: utf-8 -*-

import pydoc
import typing
import builtins
from collections import OrderedDict
from ..misc import get_boolean
from .base import NamespaceHandler, BaseParser, is_expression, Scope
from .base import ObjectDef
from .base import BaseDef, ValueDef, BasicValueDef, CallableValueDef, \
    EvaluateValueDef, ReferenceValueDef, ListValueDef,  DictValueDef
from lxml import etree


class XmlObjectsNamespaceHandler(NamespaceHandler):
    NAMESPACE = "coupling/objects"

    def __init__(self):
        parser = XmlObjectDefParser()
        for tag in ("int", "str", "bool", "float", "callable", "list", "dict", "object", "etree"):
            self.register_parser(tag, parser)


ElementType = etree._Element


class XmlObjectDefParser(BaseParser):
    def parse(self, element: ElementType, container) -> BaseDef:
        return self.get_object_def(element)

    @classmethod
    def get_object_def(cls, element: ElementType) -> BaseDef:
        tag = etree.QName(element).localname
        if tag == "object":
            define = cls.get_custom_object_def(element)
        elif tag == "callable":
            raise NotImplementedError
        elif tag == "etree":
            raise NotImplementedError
        else:
            obj_id = element.get("id")  # or "anonymous." + str(uuid.uuid1())
            type_ = getattr(builtins, tag)
            define = ObjectDef(obj_id, type_)
            if type_ in (str, int, bool, float):
                text = element.text.strip()
                if is_expression(text):
                    value = EvaluateValueDef(text, type_)
                else:
                    value = BasicValueDef(element.text.strip(), type_)
                define.args.append(value)
            elif type_ is list:
                define.args.append(cls.get_list_value_def(element))
            elif type_ is dict:
                define.args.append(cls.get_dict_value_def(element))
            else:
                raise ValueError("Unsupported tag %s" % element.tag)
        return define

    @classmethod
    def get_custom_object_def(cls, element: ElementType) -> ObjectDef:
        obj_id = element.get("id")  # or "anonymous." + str(uuid.uuid1())
        class_ = element.get("class")
        if pydoc.locate(class_) is None:
            raise ValueError("Can't locate the class: %s" % class_)

        scope = Scope.value_of(element.get("scope", Scope.SINGLETON.value).lower())
        lazy_init = element.get("lazy-init", "true").lower()
        define = ObjectDef(obj_id, pydoc.locate(class_), scope, get_boolean(lazy_init))
        for sub_element in list(element):
            if sub_element.tag is not etree.Comment:
                tag = etree.QName(sub_element).localname
                if tag == "argument":
                    arg_name = sub_element.get("name")
                    arg_value = cls.get_value_def(sub_element)
                    if arg_name is None:
                        define.args.append(arg_value)
                    else:
                        define.kwargs[arg_name] = arg_value
                elif tag == "property":
                    prop_name = sub_element.get("name")
                    prop_value = cls.get_value_def(sub_element)
                    if prop_value is not None:
                        define.props[prop_name] = prop_value
                else:
                    raise ValueError("Unsupported sub element with tag %s of %s" % (tag, element))
        return define

    @classmethod
    def get_value_def(cls, element: ElementType) -> ValueDef:
        value = element.get("value")
        if value is None:
            ref = element.get("ref")
            if ref is None:
                last_sub_node = list(element)[-1]
                value_def = cls.get_value_def_in_sub_element(last_sub_node)
            else:
                value_def = ReferenceValueDef(ref)
        else:
            if is_expression(value):
                value_def = EvaluateValueDef(value.strip(), object)
            else:
                s_type = element.get("type", "str")
                o_type = getattr(builtins, s_type)
                value_def = BasicValueDef(value, o_type)
        return value_def

    @classmethod
    def get_value_def_in_sub_element(cls, element: ElementType) -> typing.Union[ValueDef, ObjectDef]:
        tag = etree.QName(element).localname
        if tag in ("str", "int", "bool", "float"):
            type_ = getattr(builtins, tag)
            text = element.text.strip()
            if is_expression(text):
                return EvaluateValueDef(text, type_)
            else:
                return BasicValueDef(text, type_)
        elif tag == "list":
            return cls.get_list_value_def(element)
        elif tag == "dict":
            return cls.get_dict_value_def(element)
        elif tag == "ref":
            return ReferenceValueDef(element.text.strip())
        elif tag == "callable":
            return CallableValueDef(element.text.strip())
        elif tag == "object":
            text = element.text.strip()
            if is_expression(text):
                return EvaluateValueDef(text, object)
            else:
                return cls.get_custom_object_def(element)
        elif tag == "etree":
            if hasattr(element, "nsmap") and get_boolean(element.get("cleanup-namespace", True)):
                etree.cleanup_namespaces(element)
                # for iter_element in element.iter():
                #     iter_element.tag = etree.QName(iter_element).localname
            return ValueDef(list(element)[0])
        else:
            raise ValueError

    @classmethod
    def get_list_value_def(cls, element: ElementType) -> ValueDef:
        l = []
        scoped = get_boolean(element.get("scoped", False))
        for sub_element in list(element):
            if sub_element.tag is not etree.Comment:
                value_def = cls.get_value_def_in_sub_element(sub_element)
                l.append(value_def)

        if not l:
            return EvaluateValueDef(element.text.strip(), scoped=scoped)
        return ListValueDef(l)

    @classmethod
    def get_dict_value_def(cls, element: ElementType) -> ValueDef:
        ordered = get_boolean(element.get("ordered", False))
        scoped = get_boolean(element.get("scoped", False))
        d = OrderedDict() if ordered else {}
        for sub_element in list(element):
            if sub_element.tag is not etree.Comment and etree.QName(sub_element).localname == "item":
                key = sub_element.get("name")
                value_def = cls.get_value_def(sub_element)
                d[key] = value_def

        if not d:
            return EvaluateValueDef(element.text.strip(), scoped=scoped)
        return DictValueDef(d)
