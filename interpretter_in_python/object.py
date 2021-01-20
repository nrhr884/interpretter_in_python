from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass


class ObjectType(Enum):
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"


@dataclass
class Object(ABC):
    @abstractmethod
    def inspect(self) -> str:
        pass
    @abstractmethod
    def type(self) -> ObjectType:
        pass


@dataclass
class Integer(Object):
    value: int

    def inspect(self) -> str:
        return str(value)
    
    def type(self) -> ObjectType:
        return ObjectType.INTEGER_OBJ


@dataclass
class Boolean(Object):
    value: bool

    def inspect(self) -> str:
        return "true" if value else "false"

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN_OBJ

@dataclass
class Null(Object):
    value: bool

    def inspect(self) -> str:
        return "null"

    def type(self) -> ObjectType:
        return ObjectType.NULL_OBJ

