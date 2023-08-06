#!/usr/bin/env python
# -*- coding: utf-8 -*-
import decimal
import inspect
from collections import deque
from dataclasses import is_dataclass, fields, Field
from enum import Enum
from typing import ClassVar, Any, Collection, Optional, List, Set, Tuple, FrozenSet, Deque, Dict, T, KT, VT

__all__ = (
    'parse',
    'InvalidFieldError',
)


class InvalidFieldError(ValueError):
    def __init__(self, message: str, field_path: Tuple[str, ...]):
        super().__init__(message, field_path)
        self.message = message
        self.field_path = field_path


def _hasargs(type_, *args):
    try:
        if not type_.__args__:
            return False
        res = all(arg in type_.__args__ for arg in args)
    except AttributeError:
        return False
    else:
        return res


def _issubclass_safe(cls, classinfo):
    try:
        result = issubclass(cls, classinfo)
    except Exception:
        return False
    else:
        return result


def _is_tuple(type_) -> bool:
    try:
        # __origin__ exists in 3.7 on user defined generics
        return _issubclass_safe(type_.__origin__, Tuple) or _issubclass_safe(type_, Tuple)
    except AttributeError:
        return False


def _is_collection(type_) -> bool:
    try:
        # __origin__ exists in 3.7 on user defined generics
        return _issubclass_safe(type_.__origin__, Collection) or _issubclass_safe(type_, Collection)
    except AttributeError:
        return False


def _is_optional(type_) -> bool:
    return _issubclass_safe(type_, Optional) or _hasargs(type_, type(None))


def _is_union(type_: ClassVar) -> bool:
    try:
        return bool(type_.__args__)
    except:
        return False


def get_collection_factory(cls):
    origin = cls.__origin__ or cls
    res = {
        List: list,
        list: list,
        Set: set,
        set: set,
        Tuple: tuple,
        tuple: tuple,
        FrozenSet: frozenset,
        frozenset: frozenset,
        Deque: deque,
        deque: deque
    }.get(origin)
    if not res:
        raise NotImplementedError("Class %s not supported" % cls)
    return res


def _is_dict(cls):
    try:
        origin = cls.__origin__ or cls
        return origin in (dict, Dict)
    except AttributeError:
        return False


def parse(data: Any, cls: ClassVar, trim_trailing_underscore=True, type_factories=None):
    """
    * Создание класса данных из словаря
    * Примитивы проверяются на соответствие типов
    * Из коллекций поддерживается list и tuple
    * При парсинге Union ищет первый подходящий тип
    """
    if type_factories and cls in type_factories:
        return type_factories[cls](data)

    if is_dataclass(cls):
        parsed: dict = {}
        field: Field
        for field in fields(cls):
            if trim_trailing_underscore:
                name = field.name.rstrip("_")
            else:
                name = field.name
            if field.init:
                if name in data:
                    try:
                        parsed[field.name] = parse(data[name],
                                                   field.type,
                                                   trim_trailing_underscore=trim_trailing_underscore,
                                                   type_factories=type_factories)
                    except InvalidFieldError as field_error:
                        raise InvalidFieldError(field_error.message, field_error.field_path + (name,))
                    except ValueError as exc:
                        raise InvalidFieldError(str(exc), (name,))
        return cls(**parsed)

    if _is_optional(cls) and data is None:
        return None
    elif _is_dict(cls):
        key_type_arg = cls.__args__[0] if cls.__args__ else Any
        value_type_arg = cls.__args__[1] if cls.__args__ else Any
        return {
            parse(k, key_type_arg, trim_trailing_underscore=trim_trailing_underscore, type_factories=type_factories):
                parse(v, value_type_arg, trim_trailing_underscore=trim_trailing_underscore,
                      type_factories=type_factories)
            for k, v in data.items()
        }
    elif _is_collection(cls) and not isinstance(data, str) and not isinstance(data, bytes):
        if _is_tuple(cls):
            if not _hasargs(cls):
                return tuple(
                    parse(x, Any, trim_trailing_underscore=trim_trailing_underscore, type_factories=type_factories) for
                    x in data)
            if len(cls.__args__) == 2 and cls.__args__[1] is Ellipsis:
                return tuple(parse(x, cls.__args__[0], trim_trailing_underscore=trim_trailing_underscore,
                                   type_factories=type_factories) for x in data)
            elif len(cls.__args__) != len(data):
                raise ValueError("Length of data (%s) != length of types (%s)" % (len(data), len(cls.__args__)))
            else:
                return tuple(parse(x, cls.__args__[i], trim_trailing_underscore=trim_trailing_underscore,
                                   type_factories=type_factories) for i, x in enumerate(data))
        else:
            collection_factory = get_collection_factory(cls)
            type_arg = cls.__args__[0] if cls.__args__ else Any
            return collection_factory(
                parse(x, type_arg, trim_trailing_underscore=trim_trailing_underscore, type_factories=type_factories) for
                x in data
            )
    elif _is_union(cls):
        for t in cls.__args__:
            if t is not None:
                try:
                    return parse(data, t, trim_trailing_underscore=trim_trailing_underscore,
                                 type_factories=type_factories)
                except ValueError:
                    pass  # ignore value error as it is union
                except TypeError:
                    pass  # ignore type error as it is union
        raise ValueError("Cannot parse `%s` as any of `%s`" % (data, cls.__args__))
    elif cls in (Any, T, KT, VT, inspect._empty):
        return data
    elif _issubclass_safe(cls, Enum):
        return cls(data)
    elif _issubclass_safe(cls, str) and isinstance(data, str):
        return data
    elif _issubclass_safe(cls, bool) and isinstance(data, bool):
        return data
    elif _issubclass_safe(cls, bool) and (isinstance(data, str) or isinstance(data, bytes)):
        return bool(data)
    elif _issubclass_safe(cls, int) and isinstance(data, int):
        return data
    elif _issubclass_safe(cls, int) and isinstance(data, str):
        return int(data)
    elif _issubclass_safe(cls, int) and isinstance(data, bytes):
        return int(data)
    elif _issubclass_safe(cls, float) and (
            isinstance(data, float) or
            isinstance(data, int) or
            isinstance(data, str) or
            isinstance(data, bytes)
    ):
        return float(data)
    elif _issubclass_safe(cls, decimal.Decimal) and isinstance(data, str):
        try:
            return decimal.Decimal(data)
        except decimal.InvalidOperation:
            raise ValueError(f'Invalid decimal string representation {data}')
    elif _issubclass_safe(cls, complex) and (
            isinstance(data, float) or isinstance(data, int) or isinstance(data, complex)):
        return complex(data)
    else:
        try:
            arguments = inspect.signature(cls.__init__).parameters
            res = {}
            for k, v in arguments.items():
                if k != "self":
                    res[k] = parse(data.get(k), v.annotation, trim_trailing_underscore=trim_trailing_underscore,
                                   type_factories=type_factories)
            return cls(**res)
        except AttributeError as e:
            raise ValueError("Unknown type `%s` or invalid data: %s" % (cls, repr(data)))
