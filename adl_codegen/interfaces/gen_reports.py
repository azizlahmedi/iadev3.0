from delia_parser import ast
from adl_codegen.convert_type import convert_type


class Report:

    def gen_BottomMargin(self, node):
        self.src.write("BOTTOM.MARGIN ")
        self.visit(node.value)

    def gen_FootingSize(self, node):
        self.src.write("FOOTING.SIZE ")
        self.visit(node.value)

    def gen_HeadingSize(self, node):
        self.src.write("HEADING.SIZE ")
        self.visit(node.value)

    def gen_LineLength(self, node):
        self.src.write("LINE.LENGTH  ")
        self.visit(node.value)

    def gen_LineNum(self, node):
        self.src.write("LINE.NUM ")
        self.visit(node.value)

    def gen_PageDivider(self, node):
        self.src.write("PAGE.DIVIDER ")
        self.visit(node.value)

    def gen_PageNum(self, node):
        self.src.write("PAGE.NUM ")
        self.visit(node.value)

    def gen_PageSize(self, node):
        self.src.write("PAGE.SIZE ")
        self.visit(node.value)

    def gen_PageTop(self, node):
        self.src.write("PAGE.TOP ")
        self.visit(node.value)

    def gen_TopMargin(self, node):
        self.src.write("TOP.MARGIN ")
        self.visit(node.value)

    def gen_ReportCharSetAscii(self, node):
        raise NotImplemented

    def gen_ReportCharSetBinary(self, node):
        raise NotImplemented

    def gen_ReportCharSetKana(self, node):
        raise NotImplemented

    def gen_ReportCharSetDefault(self, node):
        raise NotImplemented

    def gen_ReportHeading(self, node):
        stmts = node.stmts
        self.src.newline("REPORT.HEADING")
        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_ReportFooting(self, node):
        stmts = node.stmts
        self.src.newline("REPORT.FOOTING")
        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_PageHeading(self, node):
        stmts = node.stmts
        self.src.newline("PAGE.HEADING")
        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_PageFooting(self, node):
        stmts = node.stmts
        self.src.newline("PAGE.FOOTING")
        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_GroupHeading(self, node):
        group_name = node.name
        field_name = node.field_name
        stmts = node.stmts
        self.src.newline("GROUP.HEADING ")

        if group_name:
            self.visit(group_name)
            self.src.write(" ")

        self.src.write("ON ")
        self.visit(field_name)

        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_GroupFooting(self, node):
        group_name = node.name
        field_name = node.field_name
        stmts = node.stmts
        self.src.newline("GROUP.FOOTING ")

        if group_name:
            self.visit(group_name)
            self.src.write(" ")

        self.src.write("ON ")
        self.visit(field_name)

        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_Report(self, node):

        report_name = node.name
        append = node.append
        char_set = node.char_set
        report_dest = node.dest
        report_parameters = node.parameters
        report_conditions = node.conditions

        self.src.newline("REPORT ")
        self.visit(report_name)

        if append:
            self.src.write(" APPEND")

        if char_set:
            pass

        self.src.write(" TO ")
        self.visit(report_dest)

        self.src.indent()

        for param in report_parameters:
            self.src.newline()
            self.visit(param)

        for condition in report_conditions:
            self.visit(condition)

        self.src.dedent()

    def gen_WriteReport(self, node):
        report_names = node.report_names
        stmts = node.stmts

        self.src.newline("WRITE REPORT ")

        for pos, report in enumerate(report_names):
            self.visit(report)
            if pos != len(report_names) - 1:
                self.src.write(", ")

        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_Force(self, node):
        report_cond = node.report_cond
        report_name = node.report_name

        self.src.newline("FORCE ")

        if report_name:
            self.src.write("FOR ")
            self.visit(report_name)
            self.src.write(" ")

        if isinstance(report_cond, ast.ReportHeading):
            self.src.write("REPORT.HEADING")
        elif isinstance(report_cond, ast.ReportFooting):
            self.src.write("REPORT.FOOTING")
        elif isinstance(report_cond, ast.PageHeading):
            self.src.write("PAGE.HEADING")
        elif isinstance(report_cond, ast.PageFooting):
            self.src.write("PAGE.FOOTING")
        elif isinstance(report_cond, ast.GroupHeading):
            raise NotImplemented
        elif isinstance(report_cond, ast.GroupFooting):
            raise NotImplemented
        else:
            self.visit(report_cond)

    @convert_type
    def gen_ReportBottomMargin(self, node):
        self.src.write("BOTTOM.MARGIN")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    @convert_type
    def gen_ReportFootingSize(self, node):
        self.src.write("FOOTING.SIZE")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    @convert_type
    def gen_ReportHeadingSize(self, node):
        self.src.write("HEADING.SIZE")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    @convert_type
    def gen_ReportLineLength(self, node):
        self.src.write("LINE.LENGTH")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    @convert_type
    def gen_ReportLineNum(self, node):
        self.src.write("LINE.NUM")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    @convert_type
    def gen_ReportPageDivider(self, node):
        self.src.write("PAGE.DIVIDER")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    @convert_type
    def gen_ReportPageNum(self, node):
        self.src.write("PAGE.NUM")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    @convert_type
    def gen_ReportPageSize(self, node):
        self.src.write("PAGE.SIZE")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    def gen_ReportPageTop(self, node):
        self.src.write("PAGE.TOP")

    @convert_type
    def gen_ReportTopMargin(self, node):
        self.src.write("TOP.MARGIN")
        if node.report_name:
            self.src.write(" OF ")
            self.visit(node.report_name)

    @convert_type
    def gen_CumulativeFunction(self, node):
        func_name = node.name
        parameters = node.parameters

        self.src.write(str(func_name).upper())

        self.src.write("(")
        for pos, param in enumerate(parameters):
            self.visit(param)
            if pos != len(parameters) - 1:
                self.src.write(", ")
        self.src.write(")")

    def gen_ControlClause(self, node):
        group_condition_names = node.group_condition_names

        self.src.newline("CONTROLLED BY ")
        for pos, group_condition in enumerate(group_condition_names):
            self.visit(group_condition)
            if pos != len(group_condition_names) - 1:
                self.src.write(", ")
