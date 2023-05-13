class Assignments:

    def gen_Rounded(self, node):
        self.src.write('ROUNDED')

    def gen_Truncated(self, node):
        self.src.write('TRUNCATED')

    def assign(self, node, operator, to_from=True):
        exp = node.exp
        receiving_fields = node.receiving_fields
        conversion_type = node.conversion_type
        echo = node.echo

        self.src.newline("%s " % operator)

        self.visit(exp)

        if to_from:
            self.src.write(' TO ')
        else:
            self.src.write(' FROM ')

        for pos, field in enumerate(receiving_fields):
            self.visit(field)
            if pos != len(receiving_fields) - 1:
                self.src.write(", ")

        if conversion_type:
            self.src.write(" ")
            self.visit(conversion_type)

        if echo:
            self.src.write(" ")
            self.visit(echo)

    def gen_Add(self, node):
        self.assign(node, 'ADD')

    def gen_Subtract(self, node):
        self.assign(node, 'SUBTRACT', to_from=False)

    def gen_Move(self, node):
        self.assign(node, 'MOVE')

    def gen_Let(self, node):
        exp = node.exp
        receiving_fields = node.receiving_fields
        conversion_type = node.conversion_type
        echo = node.echo

        self.src.newline("LET ")
        for pos, field in enumerate(receiving_fields):
            self.visit(field)
            if pos != len(receiving_fields) - 1:
                self.src.write(", ")

        if conversion_type:
            self.src.write(" ")
            self.visit(conversion_type)

        if echo:
            self.src.write(" ")
            self.visit(echo)

        self.src.write(' = ')
        self.visit(exp)
