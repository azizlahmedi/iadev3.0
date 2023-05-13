from delia_parser import ast


class Comparison:

    def comparison(self, left, right, op):
        self.visit(left)
        self.src.write(" %s " % op)
        self.visit(right)

    def gen_Eq(self, node):
        self.comparison(node.left, node.right, '=')

    def gen_Ge(self, node):
        self.comparison(node.left, node.right, '>=')

    def gen_Gt(self, node):
        self.comparison(node.left, node.right, '>')

    def gen_Le(self, node):
        self.comparison(node.left, node.right, '<=')

    def gen_Lt(self, node):
        self.comparison(node.left, node.right, '<')

    def gen_Ne(self, node):
        self.comparison(node.left, node.right, '#')

    def gen_And(self, node):
        self.comparison(node.left, node.right, 'AND')

    def gen_Or(self, node):
        self.comparison(node.left, node.right, 'OR')

    def gen_Eqv(self, node):
        self.comparison(node.left, node.right, 'EQV')

    def gen_Xor(self, node):
        self.comparison(node.left, node.right, 'XOR')

    def extend_comparison(self, exps, op):
        def gen_comp(exp):
            assert(isinstance(exp, ast.Rel))
            if isinstance(exp, ast.Eq):
                self.src.write(" = ")
            elif isinstance(exp, ast.Ne):
                self.src.write(" # ")
            elif isinstance(exp, ast.Ge):
                self.src.write(" >= ")
            elif isinstance(exp, ast.Gt):
                self.src.write(" > ")
            elif isinstance(exp, ast.Le):
                self.src.write(" <= ")
            elif isinstance(exp, ast.Lt):
                self.src.write(" < ")

        first_exp = None
        for pos, exp in enumerate(exps):
            if pos == 0:
                first_exp = exp
                self.visit(exp.left)
                gen_comp(exp)
            else:
                self.src.write(" ")
                self.src.write(op)

                if type(first_exp) != type(exp):
                    gen_comp(exp)
                else:
                    self.src.write(" ")

            self.visit(exp.right)

    def gen_ExtendedComparisonAnd(self, node):
        self.extend_comparison(node.exps, 'AND')

    def gen_ExtendedComparisonOr(self, node):
        self.extend_comparison(node.exps, 'OR')

    def gen_ExtendedComparisonXor(self, node):
        self.extend_comparison(node.exps, 'XOR')

    def gen_ExtendedComparisonEqv(self, node):
        self.extend_comparison(node.exps, 'EQV')
