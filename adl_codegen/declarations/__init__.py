from delia_parser import ast
from adl_codegen.codeblock import CodeBlockNames


class Declarations:

    def gen_Constant(self, node):
        name = node.name
        value = node.value

        self.visit(name)
        self.src.write(" = ")
        self.visit(value)

    def picture(self, node):
        self.src.write(repr(node).upper())

    def gen_StringPicture(self, node):
        self.picture(node)

    def gen_DatePicture(self, node):
        self.picture(node)

    def gen_DecimalPicture(self, node):
        self.picture(node)

    def gen_IntegerPicture(self, node):
        self.picture(node)

    def gen_FloatPicture(self, node):
        self.picture(node)

    def gen_DoublePicture(self, node):
        self.picture(node)

    def gen_DefaultValue(self, node):
        clause_value = node.clause_value
        self.src.write("DEFAULT ")
        self.visit(clause_value)

    def gen_VerifyClause(self, node):
        clause_value = node.clause_value
        self.src.write("VERIFY ")
        self.visit(clause_value)

    def gen_PromptClause(self, node):
        clause_value = node.clause_value
        self.src.write("PROMPT ")
        self.visit(clause_value)

    def gen_ErrorClause(self, node):
        clause_value = node.clause_value
        self.src.write("ERRORS ")
        self.visit(clause_value)

    def field_attributes(self, field_clauses):
        if not field_clauses:
            return

        self.src.indent()
        previous_is_prompt_or_error = False

        for clause in field_clauses:

            if isinstance(clause, (ast.PromptClause, ast.ErrorClause)):

                if not previous_is_prompt_or_error:
                    self.src.newline("WITH ")
                    self.visit(clause)

                else:
                    self.src.indent()
                    self.src.newline("AND ")
                    self.visit(clause)
                    self.src.dedent()
                previous_is_prompt_or_error = True

            else:
                self.src.newline()
                self.visit(clause)

        self.src.dedent()

    def gen_SameAsAttributes(self, node):
        subject_name = node.subject_name
        field_clauses = node.field_clauses

        self.src.write("SAME AS ")
        self.visit(subject_name)
        self.field_attributes(field_clauses)

    def gen_Attributes(self, node):
        picture = node.picture
        field_clauses = node.field_clauses

        self.src.write("AS ")
        self.visit(picture)
        self.field_attributes(field_clauses)

    def gen_Field(self, node):
        name = node.name
        attributes = node.attributes

        self.visit(name)
        self.src.write(' ')
        self.visit(attributes)

    def gen_ArrayColumns(self, node):
        columns = node.columns
        self.src.newline("DATA ")
        for pos, column in enumerate(columns):
            self.visit(column)
            if pos != len(columns) - 1:
                self.src.write(", ")

    def gen_SameAsArrayColumns(self, node):
        raise NotImplemented

    def gen_Array(self, node):
        array_name = node.name
        lower_bound = node._lower_bound
        upper_bound = node._upper_bound
        check = node.check
        array_columns = node.array_columns

        self.src.newline("ARRAY ")
        self.visit(array_name)
        self.src.write(' [ ')
        self.visit(lower_bound)
        self.src.write(' TO ')
        self.visit(upper_bound)
        self.src.write(' ]')

        self.src.indent()

        if check is not None:
            self.src.newline("CHECK SUBSCRIPTS ")
            if check:
                self.src.write("ON")
            else:
                self.src.write("OFF")

        self.visit(array_columns)

        self.src.dedent()

    def gen_SameAsArray(self, node):
        array_name = node.name
        subject_name = node.subject_name

        self.src.newline("ARRAY ")
        self.visit(array_name)
        self.src.write(" SAME AS ")
        self.visit(subject_name)

    def gen_SameAsRelation(self, node):
        relation_name = node.name
        subject_name = node.subject_name

        self.src.newline("RELATION ")
        self.visit(relation_name)
        self.src.write(" SAME AS ")
        self.visit(subject_name)

    def gen_Relation(self, node):
        relation_name = node.name
        keys = node.keys
        datas = node.datas
        indexes = node.indexes

        self.src.newline("RELATION ")
        self.visit(relation_name)
        self.src.write(" IS")

        self.src.indent()

        self.src.newline("KEY ")
        for pos, key in enumerate(keys):
            self.visit(key)
            if pos != len(keys) - 1:
                self.src.write(", ")

        if datas:
            self.src.newline("DATA ")
            for pos, data in enumerate(datas):
                self.visit(data)
                if pos != len(datas) - 1:
                    self.src.write(", ")

        if indexes:
            self.src.newline("INDEX ON ")
            for pos, idx in enumerate(indexes):
                self.visit(idx)
                if pos != len(indexes) - 1:
                    self.src.write(", ")

        self.src.dedent()

    def gen_Function(self, node):
        func_name = node.name
        receiving_parameters = node.receiving_parameters
        returning_parameters = node.returning_parameters
        attributes = node.attributes
        stmts = node.stmts

        self.src.newline("FUNCTION ")
        self.visit(func_name)

        self.receiving_and_returning_parameters(receiving_parameters, returning_parameters)

        if attributes:
            self.src.write(' ')
            self.visit(attributes)

        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_FLI(self, node):
        func_name = node.name
        receiving_parameters = node.receiving_parameters
        returning_parameters = node.returning_parameters
        attributes = node.attributes
        file_spec = node.file_spec

        self.src.newline("FUNCTION ")
        self.visit(func_name)

        self.receiving_and_returning_parameters(receiving_parameters, returning_parameters)

        if attributes:
            self.src.write(' ')
            self.visit(attributes)

        self.src.indent()
        self.src.newline('IN ')
        self.visit(file_spec)
        self.src.dedent()

    def gen_FunctionStmt(self, node):
        func_name = node.name
        calling_parameters = node.calling_parameters
        accepting_parameters = node.accepting_parameters
        self.src.newline()
        self.visit(func_name)
        self.calling_accepting_params(calling_parameters, accepting_parameters)
