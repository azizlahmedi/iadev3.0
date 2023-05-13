from functools import wraps


def convert_type(visitor_func):

    @wraps(visitor_func)
    def wrapper(self, node):

        conversion_types = node.conversion_types

        if conversion_types:

            if len(conversion_types) == 1:
                result = visitor_func(self, node)
                self.src.write(" AS ")
                self.visit(conversion_types[0])
            else:
                self.src.write("(" * (len(conversion_types) - 1))
                result = visitor_func(self, node)
                for pos, conversion in enumerate(conversion_types):
                    if pos != 0:
                        self.src.write(")")
                    self.src.write(" AS ")
                    self.visit(conversion)

        else:
            result = visitor_func(self, node)

        return result
    return wrapper
