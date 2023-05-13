from adl_codegen.convert_type import convert_type


class Controls:

    def gen_Wait(self, node):
        self.type(node, "WAIT")

    def gen_Abort(self, node):
        self.type(node, "ABORT")

    def gen_Logout(self, node):
        self.src.newline("LOGOUT")

    def gen_Pause(self, node):
        exp = node.exp

        self.src.newline("PAUSE ")
        self.visit(exp)

    def gen_PauseForInput(self, node):
        exp = node.exp
        then_else_clause = node.then_else_clause
        then_stmts = then_else_clause.then_stmts
        else_stmts = then_else_clause.else_stmts

        self.src.newline('PAUSE.FOR.INPUT ')
        self.visit(exp)

        self.src.newline('THEN')
        self.src.indent()
        self.src.newline('BEGIN')
        self.visit(then_stmts)
        self.src.newline('END')
        self.src.dedent()

        if else_stmts:
            self.src.newline('ELSE')
            self.src.indent()
            self.src.newline('BEGIN')
            self.visit(else_stmts)
            self.src.newline('END')
            self.src.dedent()

    def gen_ProcedureSeparator(self, node):
        self.src.newline("SEPARATOR")
        self.visit(node.value)

    def gen_ProcedureCheckSubscripts(self, node):
        check_subscripts = node.value
        self.src.newline("CHECK SUBSCRIPTS ")
        if check_subscripts:
            self.src.write("ON")
        else:
            self.src.write("OFF")

    def gen_ProcedureVerifyAcceptInput(self, node):
        self.src.newline("VERIFY ACCEPT INPUT")

    def gen_ProcedureNoAcceptTerminator(self, node):
        self.src.newline("NO ACCEPT TERMINATOR")

    def gen_ControlsForProcedure(self, node):
        control_items = node.control_items
        self.src.newline("CONTROLS FOR PROCEDURE")
        self.src.indent()
        self.visit(control_items)
        self.src.dedent()

    def gen_ControlsForLanguage(self, node):
        self.src.newline("CONTROLS FOR LANGUAGE")
        self.src.indent()
        self.visit(node.control_items)
        self.src.dedent()

    def gen_UsersLanguageIdentifier(self, node):
        self.src.newline("USERS ")
        self.visit(node.value)

    def gen_DateLanguageIdentifier(self, node):
        self.src.newline("DATE ")
        self.visit(node.value)

    def gen_DigitSeparatorLanguageIdentifier(self, node):
        self.src.newline("DIGIT SEPARATOR ")
        self.visit(node.value)

    @convert_type
    def gen_UsersLanguage(self, node):
        self.src.write("USERS LANGUAGE")

    @convert_type
    def gen_DateLanguage(self, node):
        self.src.write("DATE LANGUAGE")

    @convert_type
    def gen_DigitSeparator(self, node):
        self.src.write("DIGIT SEPARATOR")
