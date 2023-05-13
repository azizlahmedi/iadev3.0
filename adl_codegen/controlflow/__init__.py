class ControlFlow:

    def gen_Stmts(self, node):
        for stmt in node:
            self.visit(stmt)

    def gen_Nothing(self, node):
        self.src.newline("NOTHING")

    def gen_CompileDirective(self, node):
        cond = node.cond
        case_stmts = node.case_stmts
        else_stmt = node.else_stmt
        self.src.newline("COMPILE CONDITIONALLY ON ")
        self.visit(cond)

        self.src.indent()
        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(case_stmts)
        self.src.dedent()
        self.src.newline("END")
        self.src.dedent()

        if else_stmt is not None:
            self.src.newline("ELSE")
            self.src.indent()
            self.src.newline("BEGIN")
            self.visit(else_stmt)
            self.src.newline("END")
            self.src.dedent()

    def gen_CaseStmt(self, node):
        case_labels = node.case_labels
        stmts = node.stmts
        self.src.newline()
        for pos, label in enumerate(case_labels):
            self.visit(label)
            if pos != len(case_labels) - 1:
                self.src.write(' OR ')
        self.src.write(':')

        self.src.indent()
        self.src.newline("BEGIN")
        self.visit(stmts)
        self.src.newline("END")
        self.src.dedent()

    def gen_Conditional(self, node):
        cond = node.cond
        case_stmts = node.case_stmts
        else_stmt = node.else_stmt
        self.src.newline("CONDITIONAL ON ")
        self.visit(cond)

        self.src.indent()
        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(case_stmts)
        self.src.dedent()
        self.src.newline("END")
        self.src.dedent()

        if else_stmt is not None:
            self.src.newline("ELSE")
            self.src.indent()
            self.src.newline("BEGIN")
            self.visit(else_stmt)
            self.src.newline("END")
            self.src.dedent()

    def gen_DoWhile(self, node):
        stmts = node.stmts
        cond = node.cond

        self.src.newline('DO')
        self.src.indent()
        self.src.newline('BEGIN')
        self.visit(stmts)
        self.src.newline('END')
        self.src.dedent()

        self.src.newline("WHILE ")
        self.visit(cond)

    def gen_WhileDo(self, node):
        stmts = node.stmts
        cond = node.cond

        self.src.newline("WHILE ")
        self.visit(cond)

        self.src.newline('DO')
        self.src.indent()
        self.src.newline('BEGIN')
        self.visit(stmts)
        self.src.newline('END')
        self.src.dedent()

    def gen_If(self, node):
        cond = node.cond
        then_stmts = node.then_else_clause.then_stmts
        else_stmts = node.then_else_clause.else_stmts
        self.src.newline('IF ')
        self.visit(cond)

        self.src.newline('THEN')
        self.src.indent()
        self.src.newline('BEGIN')
        self.visit(then_stmts)
        self.src.newline('END')
        self.src.dedent()

        if else_stmts is not None:
            self.src.newline('ELSE')
            self.src.indent()
            self.src.newline('BEGIN')
            self.visit(else_stmts)
            self.src.newline('END')
            self.src.dedent()

    def gen_Enclosed(self, node):
        self.src.write("(")
        self.visit(node.left)
        self.src.write(")")

    def gen_LabelStmt(self, node):
        label_name = node.label.name
        stmts = node.stmts
        self.src.newline()
        self.visit(label_name)
        self.src.write(":")
        self.src.indent()
        self.src.newline('BEGIN')
        self.visit(stmts)
        self.src.newline('END')
        self.src.dedent()

    def gen_Repeat(self, node):
        label_name = node.label_name
        self.src.newline("REPEAT ")
        self.visit(label_name)

    def gen_Finish(self, node):
        label_name = node.label_name
        self.src.newline("FINISH ")
        self.visit(label_name)
