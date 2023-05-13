from adl_codegen.interfaces.gen_sources import Source
from adl_codegen.interfaces.gen_reports import Report
from adl_codegen.interfaces.gen_accepts import Accept


class Interfaces(Source,
                 Report,
                 Accept):

    def gen_Text(self, node):
        self.visit(node.value)

    def gen_File(self, node):
        self.src.write("FILE ")
        self.visit(node.value)

    def gen_Terminal(self, node):
        self.src.write("TERMINAL")

    def gen_Verify(self, node):
        self.src.write("VERIFY")

    def gen_NoVerify(self, node):
        self.src.write("NO VERIFY")

    def gen_Echo(self, node):
        self.src.write("ECHO")

    def gen_NoEcho(self, node):
        self.src.write("NO ECHO")

    def gen_DeleteFile(self, node):
        file_spec = node.file_spec
        self.src.newline("DELETE ")
        self.visit(file_spec)

    def gen_FileExists(self, node):
        value = node.left
        self.src.write("FILE ")
        self.visit(value)
        self.src.write(" EXISTING")

    def gen_TextExists(self, node):
        raise NotImplemented

    def type(self, node, kind):
        output_list = node.output_list
        self.src.newline("%s " % kind)
        for pos, output in enumerate(output_list):
            self.visit(output)
            if pos != len(output_list) - 1:
                self.src.write(', ')

    def gen_TypeToMessageArea(self, node):
        self.type(node, "TYPE TO MESSAGE.AREA")

    def gen_Type(self, node):
        self.type(node, "TYPE")

    def gen_TypeToTerminal(self, node):
        self.type(node, "TYPE TO TERMINAL")

    def gen_Print(self, node):
        output_list = node.output_list
        report_name = node.report_name

        self.src.newline("PRINT ")

        if report_name:
            self.src.write("TO ")
            self.visit(report_name)
            self.src.write(" ")

        for pos, output in enumerate(output_list):
            self.visit(output)
            if pos != len(output_list) - 1:
                self.src.write(', ')

    def gen_Tab(self, node):
        self.src.write("@TAB ")
        self.visit(node.value)

    def gen_TabTo(self, node):
        self.src.write("@TAB TO ")
        self.visit(node.value)

    def gen_Skip(self, node):
        self.src.write("@SKIP ")
        self.visit(node.value)

    def gen_SkipTo(self, node):
        self.src.write("@SKIP TO ")
        self.visit(node.value)
