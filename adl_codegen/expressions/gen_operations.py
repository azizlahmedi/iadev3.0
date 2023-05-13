from adl_codegen.convert_type import convert_type


class Operation:

    def operation(self, node, operator):
        self.src.write("(")
        self.visit(node.left)
        self.src.write(" %s " % operator)
        self.visit(node.right)
        self.src.write(")")

    @convert_type
    def gen_Mod(self, node):
        self.operation(node, "MOD")

    @convert_type
    def gen_Pow(self, node):
        self.operation(node, "**")

    @convert_type
    def gen_Div(self, node):
        self.operation(node, "/")

    @convert_type
    def gen_Mul(self, node):
        self.operation(node, "*")

    @convert_type
    def gen_Plus(self, node):
        self.operation(node, "+")

    @convert_type
    def gen_Minus(self, node):
        self.operation(node, "-")

    def unary(self, node, op):

        conversion_node_types = node.conversion_types
        conversion_right_types = node.right.conversion_types
        node.right.conversion_types = []

        if conversion_node_types:
            self.src.write("(" * len(conversion_node_types))

        self.src.write(op)

        if conversion_right_types:
            self.src.write("(" * len(conversion_right_types))

        self.visit(node.right)

        for conversion_right in enumerate(conversion_right_types):
            self.src.write(" AS ")
            self.visit(conversion_right)
            self.src.write(")")

        for conversion in enumerate(conversion_node_types):
            self.src.write(")")
            self.src.write(" AS ")
            self.visit(conversion)

    def gen_Uplus(self, node):
        self.unary(node, '+')

    def gen_Uminus(self, node):
        self.unary(node, '-')
