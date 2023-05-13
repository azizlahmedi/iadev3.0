from adl_codegen.codeblock import CodeBlockNames
from delia_parser import ast


class Screens:

    def gen_ClearFrame(self, node):
        frame_names = node.frame_names

        self.src.newline("CLEAR FRAME ")
        for pos, frame in enumerate(frame_names):
            self.visit(frame)
            if pos != len(frame_names) - 1:
                self.src.write(", ")

    def gen_Restore(self, node):
        frame_names = node.frame_names

        self.src.newline("RESTORE FRAME ")
        for pos, frame in enumerate(frame_names):
            self.visit(frame)
            if pos != len(frame_names) - 1:
                self.src.write(", ")

    def gen_SetCursor(self, node):
        after = node.after
        field = node.field

        self.src.newline("SET.CURSOR ")
        if after:
            self.src.write("AFTER ")
        self.visit(field)

    def gen_FrameFormat(self, node):
        frame_format_name = node.name
        frame_format_def = node.frame_format_def

        self.src.newline("FRAME.FORMAT ")
        self.visit(frame_format_name)
        self.src.indent()
        for line in frame_format_def:
            self.src.newline()
            self.visit(line)
        self.src.dedent()

    def gen_FrameArea(self, node):
        first_line = node.first_line
        last_line = node.last_line

        self.src.write("FRAME.AREA ")
        self.visit(first_line)
        self.src.write(" TO ")
        self.visit(last_line)

    def gen_FrameDataInfo(self, node):
        character1 = node.character1
        character2 = node.character2

        self.src.write("DATA ")
        self.visit(character1)
        if character2:
            self.src.write(" OR ")
            self.visit(character2)

    def gen_FrameControlledField(self, node):
        fields_ref = node.fields_ref
        control_items = node.control_items

        self.src.newline("FIELD.CONTROL ")
        if len(fields_ref) > 1:
            self.src.write('(')
            for pos, field in enumerate(fields_ref):
                self.visit(field)
                if pos != len(fields_ref) - 1:
                    self.src.write(', ')
            self.src.write(')')

        else:
            self.visit(fields_ref[0])

        self.src.indent()

        self.src.newline()
        for pos, control in enumerate(control_items):
            self.visit(control)
            if pos != len(control_items) - 1:
                self.src.newline()

        self.src.dedent()

    def frame_control_item(self, node):
        form = node.form
        values = node.value

        self.src.write(form)

        if values:
            self.src.write(" ")
            for pos, value in enumerate(values):
                self.visit(value)
                if pos != len(values) - 1:
                    self.src.write(", ")

    def gen_FrameControlBlank(self, node):
        self.frame_control_item(node)

    def gen_FrameControlBlink(self, node):
        self.frame_control_item(node)

    def gen_FrameControlBold(self, node):
        self.frame_control_item(node)

    def gen_FrameControlColor(self, node):
        self.frame_control_item(node)

    def gen_FrameControlDim(self, node):
        self.frame_control_item(node)

    def gen_FrameControlHelp(self, node):
        self.frame_control_item(node)

    def gen_FrameControlInitial(self, node):
        self.frame_control_item(node)

    def gen_FrameControlMinimumLength(self, node):
        self.frame_control_item(node)

    def gen_FrameControlOpaque(self, node):
        self.frame_control_item(node)

    def gen_FrameControlProtected(self, node):
        self.frame_control_item(node)

    def gen_FrameControlRequired(self, node):
        self.frame_control_item(node)

    def gen_FrameControlReverse(self, node):
        self.frame_control_item(node)

    def gen_FrameControlTerminateField(self, node):
        self.frame_control_item(node)

    def gen_FrameControlUnderline(self, node):
        self.frame_control_item(node)

    def gen_Frame(self, node):
        frame_format_location = node.frame_format_location
        border = node.border
        frame_area = node.frame_area
        frame_data_info = node.frame_data_info
        frame_data_names = node.frame_data_names
        controlled_field_list = node.controlled_field_list
        frame_name = node.name

        self.src.newline("FRAME ")
        self.visit(frame_name)

        if frame_format_location:
            self.src.write(" FROM ")
            self.visit(frame_format_location)

        self.src.indent()

        if frame_area:
            self.src.newline()
            self.visit(frame_area)

        if frame_data_info:
            self.src.newline()
            self.visit(frame_data_info)

        self.src.newline("DATA.NAMES ")
        for pos, data in enumerate(frame_data_names):
            self.visit(data)
            if pos != len(frame_data_names) - 1:
                self.src.write(', ')

        if controlled_field_list:
            for control in controlled_field_list:
                self.visit(control)

        if border:
            raise NotImplemented

        self.src.dedent()

    def flag_reference(self, field, flag):
        self.src.write(flag)
        self.src.write(" FLAG.OF ")
        self.visit(field)

    def gen_FlagBlank(self, node):
        self.flag_reference(node.name, "BLANK")

    def gen_FlagBlink(self, node):
        self.flag_reference(node.name, "BLINK")

    def gen_FlagBold(self, node):
        self.flag_reference(node.name, "BOLD")

    def gen_FlagRequired(self, node):
        self.flag_reference(node.name, "REQUIRED")

    def gen_FlagReverse(self, node):
        self.flag_reference(node.name, "REVERSE")

    def gen_FlagTerminate(self, node):
        self.flag_reference(node.name, "TERMINATE.FIELD")

    def gen_FlagUnderline(self, node):
        self.flag_reference(node.name, "UNDERLINE")

    def gen_FlagDim(self, node):
        raise NotImplemented

    def gen_FlagEntered(self, node):
        raise NotImplemented

    def gen_FlagInitial(self, node):
        raise NotImplemented

    def gen_FlagLow(self, node):
        raise NotImplemented

    def gen_FlagMinimun(self, node):
        raise NotImplemented

    def gen_FlagOpaque(self, node):
        raise NotImplemented

    def gen_FlagProtected(self, node):
        raise NotImplemented

    def gen_FlagValue(self, node):
        raise NotImplemented

    def gen_FlagVerify(self, node):
        raise NotImplemented

    def gen_Display(self, node):
        frame_names = node.frame_names
        function_key_names = node.function_key_names
        stmts = node.stmts

        self.src.newline("DISPLAY ")
        for pos, frame in enumerate(frame_names):
            self.visit(frame)
            if pos != len(frame_names) - 1:
                self.src.write(", ")

        if function_key_names:
            self.src.indent()
            self.src.newline("USING ")
            for pos, function_key in enumerate(function_key_names):
                self.visit(function_key)
                if pos != len(function_key_names) - 1:
                    self.src.write(", ")
            self.src.dedent()

        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_FunctionKey(self, node):
        name = node.name
        is_globally = node.is_globally
        sequence = node.sequence
        stmts = node.stmts

        self.src.newline("FUNCTION.KEY ")
        self.visit(name)
        self.src.write(" IS ")
        self.visit(sequence)

        if is_globally:
            self.src.write(" GLOBALLY")

        self.src.newline("BEGIN")
        self.src.indent()
        self.visit(stmts)
        self.src.dedent()
        self.src.newline("END")

    def gen_Input(self, node):
        field_names = node.field_names
        function_key_names = node.function_key_names
        echo = node.echo
        verify = node.verify

        self.src.newline("INPUT ")

        if verify:
            self.visit(verify)
            self.src.write(" ")

        if echo:
            self.visit(echo)
            self.src.write(" ")

        for pos, field in enumerate(field_names):
            self.visit(field)
            if pos != len(field_names) - 1:
                self.write(", ")

        if function_key_names:
            self.src.indent()
            self.src.newline("USING ")
            for pos, function_key in enumerate(function_key_names):
                self.visit(function_key)
                if pos != len(function_key_names) - 1:
                    self.src.write(", ")
            self.src.dedent()

    def gen_Screen(self, node):
        attributes = node.attributes

        self.src.newline("SCREEN")
        self.src.indent()
        for attr in attributes:
            if not isinstance(attr, ast.ScreenAttribute):
                raise NotImplemented
            self.src.newline()
            self.visit(attr)
        self.src.dedent()

    def gen_ScreenMessageArea(self, node):
        first_line = node.first_line
        last_line = node.last_line

        self.src.write("MESSAGE.AREA ")
        self.visit(first_line)
        if last_line:
            self.src.write(" TO ")
            self.visit(last_line)

    def gen_ScreenSize(self, node):
        size = node.size

        self.src.write("SCREEN.SIZE ")
        self.visit(size)

    def gen_ScreenFunctionLength(self, node):
        length = node.length

        self.src.write("FUNCTION.LENGTH ")
        self.visit(length)

    def gen_ScreenFunctionSeparator(self, node):
        separator = node.separator

        self.src.write("FUNCTION.SEPARATOR ")
        self.visit(separator)

    def gen_ScreenAbortProcedure(self, node):
        value = node.value

        self.src.write("ABORT.PROCEDURE ")
        self.visit(value)

    def gen_ScreenBackupCharacter(self, node):
        value = node.value

        self.src.write("BACKUP.CHARACTER ")
        self.visit(value)

    def gen_ScreenBackupField(self, node):
        value = node.value

        self.src.write("BACKUP.FIELD ")
        self.visit(value)

    def gen_ScreenFieldFiller(self, node):
        value = node.value

        self.src.write("FIELD.FILLER ")
        self.visit(value)

    def gen_ScreenGetHelp(self, node):
        value = node.value

        self.src.write("GET.HELP ")
        self.visit(value)

    def gen_ScreenLineLength(self, node):
        size = node.size

        self.src.write("LINE.LENGTH ")
        self.visit(size)

    def gen_ScreenSkipField(self, node):
        value = node.value

        self.src.write("SKIP.FIELD ")
        self.visit(value)

    def gen_ScreenTerminateField(self, node):
        value = node.value

        self.src.write("TERMINATE.FIELD ")
        self.visit(value)
