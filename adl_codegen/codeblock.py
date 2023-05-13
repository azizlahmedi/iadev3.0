# -*- coding: utf-8 -*-
import logging
from enum import Enum

from delia_commons.singleton import Singleton

logger = logging.getLogger('delia.codegen')


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class CodeBlockNames(AutoNumber):
    SCHEMA = ()
    PROCEDURE = ()


class Token(Singleton):
    pass


class Indent(Token):
    pass


class Dedent(Token):
    pass


class Newline(Token):
    pass


class CodeBlock:

    def __init__(self, tab=4 * " "):
        self.code = []
        self.tab = tab

    def newline(self, string=""):
        self.code.append(Newline())
        self.code.append(string)

    def write(self, string):
        self.code[-1] += string

    def indent(self):
        self.code.append(Indent())

    def dedent(self):
        self.code.append(Dedent())

    def add(self, cb):
        self.code.append(cb)

    def flatten(self, level=0):
        flat = ""
        for line in self.code:
            if isinstance(line, Newline):
                flat += "\n"
            elif isinstance(line, Indent):
                level += 1
            elif isinstance(line, Dedent):
                level -= 1
            elif isinstance(line, str):
                if line != '':
                    flat += level * self.tab + line
            elif isinstance(line, CodeBlock):
                flat += line.flatten(level)
        return flat

    def isEmpty(self):
        return True if self.code == [] else False


if __name__ == "__main__":

    cb = CodeBlock(tab="°")
    cb2 = CodeBlock(tab="°")

    cb.newline("def toto():")
    cb.indent()
    cb.add(cb2)
    cb.dedent()

    cb2.newline("C1 = 0")
    cb2.newline("C2 = 1")
    cb2.newline()
    cb2.write("C3 = ")
    cb2.write("2")
    cb2.newline()
    cb2.write("def hello():")
    cb2.indent()
    cb2.newline("pass")
    cb2.dedent()

    print(cb.flatten())
