# -*- coding: utf-8 -*-
from delia_tokenizer.ctokenize import (ScannerFromString,
                                       ScannerFromFile)

from delia_preprocessor import scan

from delia_parser.compile_context import CompileContext
from delia_parser.parser import parse, gen_ast
from delia_parser import validate, annotate
from delia_parser.visitor import walk
from delia_parser import types, ast

from delia_commons.exceptions import (SemanticErrors,
                                      SemanticWarnings)

from adl_codegen.codeblock import (CodeBlock,
                                   CodeBlockNames)
from adl_codegen.assignments import Assignments
from adl_codegen.controlflow import ControlFlow
from adl_codegen.controls import Controls
from adl_codegen.declarations import Declarations
from adl_codegen.expressions import Expressions
from adl_codegen.queries import Queries
from adl_codegen.interfaces import Interfaces
from adl_codegen.screens import Screens


def compile_file(filepath, schema_tree=None, compile_ctx=None, callback=None, *args):
    if compile_ctx is None:
        compile_ctx = CompileContext(root=ast.Root())
    else:
        compile_ctx = compile_ctx
    scanner = ScannerFromFile(filepath)
    gen = Procedure(compile_ctx, scanner)
    gen.compile(schema_tree, callback, *args)
    return gen.get_code()


def compile(source, schema_tree=None, callback=None, *args):
    compile_ctx = CompileContext(root=ast.Root())
    scanner = ScannerFromString(source)
    gen = Procedure(compile_ctx, scanner)
    gen.compile(schema_tree, callback, *args)
    return gen.get_code()


def compile_schema_file(filepath, compile_ctx=None):
    if compile_ctx is None:
        compile_ctx = CompileContext(root=ast.Root())
    else:
        compile_ctx = compile_ctx
    scanner = ScannerFromFile(filepath)
    gen = Schema(compile_ctx, scanner)
    return gen.compile()


def compile_schema(source, compile_ctx=None):
    if compile_ctx is None:
        compile_ctx = CompileContext(root=ast.Root())
    else:
        compile_ctx = compile_ctx
    scanner = ScannerFromString(source)
    gen = Schema(compile_ctx, scanner)
    return gen.compile()


def dbg(stmt):
    import inspect
    extern_locals, extern_globals = inspect.currentframe().f_back.f_locals, \
        inspect.currentframe().f_back.f_globals
    print(
        ": ".join((stmt, str(eval(stmt, extern_locals, extern_globals)))))


class AbstractCompileProcedure:

    def __init__(self, compile_ctx, scanner):
        self.compile_ctx = compile_ctx
        self.scanner = scanner
        self.code = None

    def _get_tree(self):
        tokens = scan(
            self.scanner,
            self.scanner.path,
            files=self.compile_ctx.files,
            acros=self.compile_ctx.macros)
        parser = gen_ast.Parser(verbose=False)
        parse(self.compile_ctx, tokens=iter(tokens), parser=parser)
        return self.compile_ctx.ast

    def compile(self, schema_tree=None):
        pass  # implemented by subclass

    def get_code(self):
        return self.code


class Procedure(AbstractCompileProcedure):

    def compile(self, schema_tree=None, callback=None, *args):
        tree = self._get_tree().procedure
        if callback:
            callback(tree, *args)
        gen = ProcedureCodeGenerator(self.compile_ctx)
        gen.run(tree, schema_tree)
        self.code = gen.get_code()


class Schema(AbstractCompileProcedure):

    def compile(self):
        return self._get_tree().schema


class CodeGeneratorBackend(Assignments,
                           Declarations,
                           ControlFlow,
                           Controls,
                           Expressions,
                           Queries,
                           Interfaces,
                           Screens):
    """Defines basic code generator for ADL
    This class is an abstract base class.
    """
    __initialized = None

    def __init__(self, compile_ctx, visit=None):

        self.compile_ctx = compile_ctx
        self.visit = visit
        self.got_schema = False

        if self.__initialized is None:
            self.init_class()
            self.__class__.__initialized = True
        self.check_class()

    def init_class(self):
        """This method is called once for each class"""

    def check_class(self):
        """Verify that class is constructed correctly"""
        pass
#        try:
#            assert hasattr(self, 'set_lineno')
#        except AssertionError, msg:
#            intro = "Bad class construction for %s" % self.__class__.__name__
#            raise AssertionError, intro

    def validate(self, tree):
        if not hasattr(self, "validation_visitor"):
            setattr(
                self,
                "validation_visitor",
                validate.Validator(self.compile_ctx))
        walk(tree, self.validation_visitor)

    def annotate(self, tree):
        if not hasattr(self, "annotation_visitor"):
            setattr(
                self,
                "annotation_visitor",
                annotate.Annotator(self.compile_ctx))
        walk(tree, self.annotation_visitor)

    def annotate_and_validate(self, node):
        return

        self.annotate(node)
        try:
            self.validate(node)
        except SemanticErrors as err:
            raise err
        # Only catch warnings, error shall block the code generation
        except SemanticWarnings as warn:
            # Clean warnings for the next validation
            warn.clear_warn()

    def declarations(self, decls):

        is_last_decl_field = False
        is_last_decl_constant = False

        def walk_declations(decls):

            nonlocal is_last_decl_field, is_last_decl_constant

            if isinstance(decls, (ast.Decls, list)):

                for decl in decls:
                    walk_declations(decl)

            else:

                if isinstance(decls, ast.Constant):

                    if is_last_decl_constant:
                        self.src.newline(", ")
                    else:

                        if is_last_decl_field:
                            self.src.dedent()

                        self.src.newline("CONSTANT")
                        self.src.indent()
                        self.src.newline()

                    is_last_decl_constant = True
                    is_last_decl_field = False
                    self.visit(decls)

                elif isinstance(decls, ast.Field):

                    if is_last_decl_field:
                        self.src.newline(", ")
                    else:
                        if is_last_decl_constant:
                            self.src.dedent()

                        self.src.newline("FIELDS")
                        self.src.indent()
                        self.src.newline()

                    is_last_decl_field = True
                    is_last_decl_constant = False
                    self.visit(decls)

                elif isinstance(decls, ast.Decl):

                    if is_last_decl_constant or is_last_decl_field:
                        self.src.dedent()

                    is_last_decl_field = False
                    is_last_decl_constant = False
                    self.visit(decls)

                else:
                    self.visit(decls)

        walk_declations(decls)

        if is_last_decl_constant or is_last_decl_field:
            self.src.dedent()

    def gen_Procedure(self, node):

        self.annotate_and_validate(node)

        if not self.got_schema:
            self.codeblocks()

        self.src = self.source[CodeBlockNames.PROCEDURE]

        proc_name = node.name
        receiving_parameters = node.receiving_parameters
        returning_parameters = node.returning_parameters
        delcs = node.decls
        stmts = node.stmts

        self.proc_name = proc_name

        self.src.newline("PROCEDURE ")
        self.visit(proc_name)

        if receiving_parameters:
            self.params(receiving_parameters)

        if returning_parameters:
            self.src.indent()
            self.src.newline("RETURNING")
            self.params(returning_parameters)
            self.src.dedent()

        self.src.newline("BEGIN")
        self.src.indent()
        self.declarations(delcs)
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_Schema(self, node):

        self.got_schema = True
        self.codeblocks()

        self.annotate_and_validate(node)

        self.src = self.source[CodeBlockNames.SCHEMA]

        schema_name = node.name
        delcs = node.decls

        self.schema_name = node.name
        self.src.newline("SCHEMA ")
        self.visit(schema_name)
        self.src.newline("BEGIN")
        self.src.indent()
        self.declarations(delcs)
        self.src.dedent()
        self.src.newline("END")

    def codeblocks(self):
        self.source = {}
        for block in CodeBlockNames:
            self.source[block] = CodeBlock()

    def gen_UsingClause(self, node):
        parametre = node.parametre
        data_expression = node.data_expression

        self.visit(data_expression)
        self.src.write(" FOR ")
        self.visit(parametre)

    def gen_Return(self, node):
        using_clauses = node.using_clauses

        self.src.newline("RETURN")

        if using_clauses:
            self.src.indent()
            self.src.newline("USING")
            self.params(using_clauses)
            self.src.dedent()

    def gen_RunStmt(self, node):
        proc_name = node.name
        calling_parameters = node.calling_parameters
        accepting_parameters = node.accepting_parameters

        self.src.newline("RUN ")
        self.visit(proc_name)
        self.calling_accepting_params(calling_parameters, accepting_parameters)

    def params(self, params):
        self.src.write(" (")
        self.src.indent()
        for pos, param in enumerate(params):
            if pos == 0:
                self.src.newline()
            self.visit(param)
            if pos != len(params) - 1:
                self.src.newline(", ")
        self.src.dedent()
        if len(params) == 0:
            self.src.write(")")
        else:
            self.src.newline(")")

    def receiving_and_returning_parameters(self, receiving_parameters, returning_parameters):
        if receiving_parameters:
            self.src.write(" (")
            for pos, param in enumerate(receiving_parameters):
                self.visit(param)
                if pos != len(receiving_parameters) - 1:
                    self.src.write(", ")
            self.src.write(")")

        if returning_parameters:
            self.src.indent()
            self.src.newline("RETURNING")
            self.params(returning_parameters)
            self.src.dedent()

    def calling_accepting_params(self, calling_parameters, accepting_parameters):
        if calling_parameters:
            self.src.write(" (")
            for pos, param in enumerate(calling_parameters):
                self.visit(param)
                if pos != len(calling_parameters) - 1:
                    self.src.write(", ")
            self.src.write(")")

        if accepting_parameters:
            self.src.indent()
            self.src.newline("ACCEPTING")
            self.params(accepting_parameters)
            self.src.dedent()

    def get_code(self):
        code = self.source[CodeBlockNames.SCHEMA].flatten(), self.source[CodeBlockNames.PROCEDURE].flatten()
        return code


class ProcedureCodeGenerator(CodeGeneratorBackend):

    def run(self, tree, schema_tree, verbose=False):
        if schema_tree is not None:
            self.in_schema = True
            walk(schema_tree, self, prefix='gen_', verbose=verbose)
        self.in_schema = False
        walk(tree, self, prefix='gen_', verbose=verbose)
