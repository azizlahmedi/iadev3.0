class Accept:

    def gen_ForClause(self, node):
        field_clauses = node.field_clauses
        field_name = node.field_name

        self.src.write("WITH ")

        for pos, clause in enumerate(field_clauses):
            self.visit(clause)
            if pos != len(field_clauses) - 1:
                self.src.write(" AND ")

        self.src.write(" FOR ")
        self.visit(field_name)

    def gen_AcceptInputId(self, node):
        self.gen_Id(node)
        self.visit(node.input_picture)

    def gen_AcceptInputArrayId(self, node):
        self.gen_ArrayId(node)
        self.visit(node.input_picture)

    def gen_Accept(self, node):
        from_terminal = node.from_terminal
        verify = node.verify
        echo = node.echo
        field_names = node.field_names
        prompt_clauses = node.prompt_clauses

        self.src.newline("ACCEPT ")
        if from_terminal:
            self.src.write("FROM TERMINAL")
            self.src.write(" ")

        if verify:
            self.visit(verify)
            self.src.write(" ")

        if echo:
            self.visit(echo)
            self.src.write(" ")

        for pos, field in enumerate(field_names):
            self.visit(field)
            if pos != len(field_names) - 1:
                self.src.write(", ")

        if prompt_clauses:
            self.src.indent()
            for clause in prompt_clauses:
                self.src.newline()
                self.visit(clause)
            self.src.dedent()
