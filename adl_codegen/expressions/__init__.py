from adl_codegen.expressions.gen_operations import Operation
from adl_codegen.expressions.gen_comparisons import Comparison
from adl_codegen.convert_type import convert_type
from delia_parser.builtins import builtins


class Expressions(Operation,
                  Comparison,
                  ):

    def gen_Default(self, node):
        self.src.write("DEFAULT")

    def gen_ConstantRef(self, node):
        name = node.name
        self.visit(name)

    @convert_type
    def gen_Id(self, node):
        of_name = node.of_name
        name = node.name
        self.visit(name)
        if of_name:
            self.src.write(" OF ")
            self.visit(of_name)

    @convert_type
    def gen_ReturningFunction(self, node):
        name = node.name
        self.visit(name)

    def gen_AsId(self, node):
        self.visit(node.id)

    def gen_AsPicture(self, node):
        picture = node.picture
        self.visit(picture)

    @convert_type
    def gen_ArrayId(self, node):
        array_name = node.of_name
        row_name = node.name
        index = node.index

        self.visit(row_name)

        self.src.write("[")
        self.visit(index)
        self.src.write("]")

        if array_name:
            self.src.write(" OF ")
            self.visit(array_name)

    def gen_ArrayIndex(self, node):
        index = node.index
        self.visit(index)

    def gen_ArrayIndexAll(self, node):
        self.src.write('ALL')

    def gen_ArrayIndexTo(self, node):
        lower = node.lower
        upper = node.upper
        self.visit(lower)
        self.src.write(' TO ')
        self.visit(upper)

    def gen_Name(self, node):
        self.src.write(str(node.value).lower())

    @convert_type
    def gen_Date(self, node):
        if not node.value:
            self.src.write("DATE")
        else:
            self.src.write("DATE '{value}'".format(value=node.value))

    @convert_type
    def gen_String(self, node):
        if '"' in node.value:
            quote = "'"
        else:
            quote = '"'
        self.src.write("{quote}{value}{quote}".format(quote=quote, value=node.value))

    def gen_ControlCharacter(self, node):
        self.src.write(node.token.upper())

    def gen_ConcatenatedString(self, node):
        for pos, value in enumerate(node.values):
            self.visit(value)
            if pos != len(node.values) - 1:
                self.src.write(' + ')

    @convert_type
    def gen_Integer(self, node):
        self.src.write(repr(node))

    @convert_type
    def gen_Decimal(self, node):
        self.src.write(repr(node))

    @convert_type
    def gen_Float(self, node):
        self.src.write(repr(node))

    @convert_type
    def gen_Double(self, node):
        self.src.write(repr(node))

    def gen_Boolean(self, node):
        if str(node).upper() == 'FALSE':
            self.src.write("FALSE")
        else:
            self.src.write("TRUE")

    def gen_Not(self, node):
        self.src.write("NOT ")
        self.src.write("(")
        self.visit(node.left)
        self.src.write(")")

    @convert_type
    def gen_CallingFunction(self, node):
        func_name = node.name
        parameters = node.parameters

        func = str(func_name).lower()

        if func in builtins:
            self.src.write(func.upper())
        else:
            self.src.write(func)

        if parameters or func not in builtins:
            if not isinstance(parameters, list):
                parameters = [parameters]

            self.src.write("(")
            for pos, param in enumerate(parameters):
                self.visit(param)
                if pos != len(parameters) - 1:
                    self.src.write(", ")
            self.src.write(")")

    def gen_Is(self, node):
        left = node.left
        right = node.right

        self.visit(left)
        self.src.write(" IS ")
        self.visit(right)

    def gen_Monday(self, node):
        self.src.write("MONDAY")

    def gen_Tuesday(self, node):
        self.src.write("TUESDAY")

    def gen_Wednesday(self, node):
        self.src.write("WEDNESDAY")

    def gen_Thursday(self, node):
        self.src.write("THURSDAY")

    def gen_Friday(self, node):
        self.src.write("FRIDAY")

    def gen_Saturday(self, node):
        self.src.write("SATURDAY")

    def gen_Sunday(self, node):
        self.src.write("SUNDAY")
