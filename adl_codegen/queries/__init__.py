from adl_codegen.convert_type import convert_type


class Queries:

    def gen_Changing(self, node):
        left = node.left
        self.visit(left)
        self.src.write(" CHANGING")

    def gen_NotChanging(self, node):
        left = node.left
        self.visit(left)
        self.src.write(" NOT CHANGING")

    def gen_ViaClause(self, node):
        lkey_value = node.lkey_value
        self.src.write("(")
        for pos, key in enumerate(lkey_value):
            self.visit(key)
            if pos != len(lkey_value) - 1:
                self.src.write(", ")
        self.src.write(")")

    def gen_ViaKeyClause(self, node):
        self.src.write("KEY")

    def gen_WhereClause(self, node):
        clause = node.clause
        self.visit(clause)

    def gen_SortItem(self, node):
        order = node.order
        field_name = node.field_name
        self.visit(order)
        self.src.write(" ")
        self.visit(field_name)

    def gen_SortedClause(self, node):
        direction = node.direction
        self.visit(direction)

    def gen_SortedOnClause(self, node):
        sort_list = node.sort_list
        self.src.write("ON ")
        for pos, sort in enumerate(sort_list):
            self.visit(sort)
            if pos != len(sort_list) - 1:
                self.src.write(", ")

    def gen_Ascending(self, node):
        self.src.write("ASCENDING")

    def gen_Descending(self, node):
        self.src.write("DESCENDING")

    def gen_QualifiedRelationAlias(self, node):
        relation_name = node.relation_name
        alias_name = node.alias_name
        via_clause = node.via_clause
        where_clause = node.where_clause
        sorted_clause = node.sorted_clause

        self.visit(relation_name)

        if alias_name:
            self.src.write(" ALIAS ")
            self.visit(alias_name)

        if via_clause:
            self.src.indent()
            self.src.newline("VIA ")
            self.visit(via_clause)
            self.src.dedent()

        if where_clause:
            self.src.indent()
            self.src.newline("WHERE ")
            self.visit(where_clause)
            self.src.dedent()

        if sorted_clause:
            self.src.indent()
            self.src.newline("SORTED ")
            self.visit(sorted_clause)
            self.src.dedent()

    def gen_Select(self, node):
        qualified_rel_alias = node.qualified_rel_alias
        then_else_clause = node.then_else_clause
        then_stmts = then_else_clause.then_stmts
        else_stmts = then_else_clause.else_stmts

        self.src.newline("SELECT ")
        self.visit(qualified_rel_alias)

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

    def gen_For(self, node):
        qualified_rel_alias = node.qualified_rel_alias
        report_names = node.report_names
        control_clause = node.control_clause
        stmts = node.stmts

        self.src.newline("FOR EACH ")
        self.visit(qualified_rel_alias)

        if report_names:
            self.src.indent()
            self.src.newline("WRITE REPORT ")
            for pos, report in enumerate(report_names):
                self.visit(report)
                if pos != len(report_names) - 1:
                    self.src.write(", ")
            self.src.dedent()

        if control_clause:
            self.src.indent()
            self.visit(control_clause)
            self.src.dedent()

        self.src.newline("DO")
        self.src.indent()
        self.src.newline("BEGIN")
        self.visit(stmts)
        self.src.newline("END")
        self.src.dedent()

    @convert_type
    def gen_ImplicitSelect(self, node):
        field_name = node.field_name
        qualified_rel_alias = node.qualified_rel_alias
        relation_name = qualified_rel_alias.relation_name
        via_clause = qualified_rel_alias.via_clause

        self.visit(field_name)
        self.src.write(" (")
        self.visit(relation_name)
        self.src.write(" VIA ")
        self.visit(via_clause)
        self.src.write(")")

    def gen_Alter(self, node):
        relation_name = node.relation_name
        using_clauses = node.using_clauses

        self.src.newline("ALTER ")
        self.visit(relation_name)

        if using_clauses:
            self.src.indent()
            self.src.newline("USING (")
            for pos, clause in enumerate(using_clauses):
                self.visit(clause)
                if pos != len(using_clauses) - 1:
                    self.src.write(", ")
            self.src.write(")")
            self.src.dedent()

    def gen_DeleteRelation(self, node):
        qualified_rel_alias = node.qualified_rel_alias
        all_ = node.all

        self.src.newline("DELETE FROM ")
        self.visit(qualified_rel_alias)
        if all_:
            self.src.write(" ALL")

    def gen_Insert(self, node):
        relation_name = node.relation_name
        using_clauses = node.using_clauses
        duplicate_clause = node.duplicate_clause

        self.src.newline("INSERT INTO ")
        self.visit(relation_name)

        if using_clauses:
            self.src.indent()
            self.src.newline("USING (")
            for pos, clause in enumerate(using_clauses):
                self.visit(clause)
                if pos != len(using_clauses) - 1:
                    self.src.write(", ")
            self.src.write(")")
            self.src.dedent()

        if duplicate_clause is not None:
            self.src.indent()
            self.src.newline("ON DUPLICATE")
            self.src.newline("BEGIN")
            self.src.indent()
            self.visit(duplicate_clause)
            self.src.dedent()
            self.src.newline("END")
            self.src.dedent()
