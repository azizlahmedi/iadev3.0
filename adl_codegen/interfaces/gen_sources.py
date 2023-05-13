from delia_parser import ast


class Source:

    def gen_SourceInport(self, node):
        raise NotImplemented

    def gen_SourceBinaryForm(self, node):
        raise NotImplemented

    def gen_SourceInvalids(self, node):
        raise NotImplemented

    def gen_SourceFixedForm(self, node):
        self.src.write("FIXED FORM")

    def gen_SourceFreeForm(self, node):
        self.src.write("FREE FORM")

    def gen_SourceLineLength(self, node):
        self.src.write("LINE.LENGTH ")
        self.visit(node.value)

    def gen_SourceSeparator(self, node):
        self.src.write("SEPARATOR ")
        self.visit(node.value)

    def gen_Source(self, node):
        source_name = node.name
        location = node.location
        attributes = node.attributes
        inputs = node.inputs
        prompt = node.prompt

        self.src.newline("SOURCE ")
        self.visit(source_name)
        self.src.write(" FROM ")
        self.visit(location)

        self.src.indent()

        for attr in attributes:
            self.src.newline()
            self.visit(attr)

        self.src.newline("INPUT")
        self.src.indent()
        self.src.newline()

        for pos, source_input in enumerate(inputs):
            if pos != 0 and not isinstance(source_input, ast.SourceConditional):
                self.src.write(" ")
            self.visit(source_input)
            if pos != len(inputs) - 1:
                self.src.write(",")

        self.src.dedent()
        self.src.dedent()

        if prompt:
            raise NotImplemented

    def gen_InputCase(self, node):
        case_labels = node.case_labels
        inputs = node.inputs

        self.src.newline()
        for pos, label in enumerate(case_labels):
            self.visit(label)
            if pos != len(case_labels) - 1:
                self.src.write(' OR ')
        self.src.write(':')

        self.src.indent()
        self.src.newline()
        for pos, source_input in enumerate(inputs):
            if pos != 0 and not isinstance(source_input, ast.SourceConditional):
                self.src.write(" ")
            self.visit(source_input)
            if pos != len(inputs) - 1:
                self.src.write(",")
        self.src.dedent()

    def gen_SourceConditional(self, node):
        cond = node.cond
        input_cases = node.input_cases
        input_else = node.input_else

        self.src.newline()
        self.src.write("CONDITIONAL ON ")
        self.visit(cond)

        self.src.indent()
        self.src.newline("BEGIN")
        self.visit(input_cases)
        self.src.newline("END")
        self.src.dedent()

        if input_else:
            self.src.newline("ELSE")
            self.src.indent()
            self.src.newline("BEGIN")

            self.src.newline()
            for pos, source_input in enumerate(input_else):
                if pos != 0 and not isinstance(source_input, ast.SourceConditional):
                    self.src.write(" ")
                self.visit(source_input)
                if pos != len(input_else) - 1:
                    self.src.write(",")

            self.src.newline("END")
            self.src.dedent()

    def gen_SourceInputId(self, node):
        name = node.name
        input_picture = node.input_picture

        self.visit(name)

        if input_picture:
            self.src.write(" AS ")
            self.visit(input_picture)
