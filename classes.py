import numbers


class Expression:
    def __init__(self, string):
        self.string = string

    def __eq__(self, other):
        if other is None:
            return False
        if not issubclass(other.__class__, Expression):
            return False
        return True

    def __str__(self):
        return self.string

    def is_compound(self):
        return isinstance(self, Compound)

    def is_atom(self):
        return issubclass(self.__class__, Atom)

    def is_literal(self):
        return self.is_number() or self.is_string() or self.is_bool()

    def is_identifier(self):
        return issubclass(self.__class__, Identifier)

    def is_number(self):
        return isinstance(self, Number)

    def is_string(self):
        return isinstance(self, String)

    def is_bool(self):
        return isinstance(self, Bool)


class Compound(Expression):
    def __init__(self, string, compound_list):
        super().__init__(string)
        self.compound_list = compound_list

    def __iter__(self):
        return iter(self.compound_list)

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not other.is_compound():
            return False
        return self.compound_list == other.compound_list


class Atom(Expression):
    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not other.is_atom():
            return False
        return self.string == other.string


class Identifier(Atom):
    def __init__(self, string):
        super().__init__(string)


class Number(Atom):
    def __init__(self, string):
        super().__init__(string)
        if '.' in string:
            self.number = float(string)
        else:
            self.number = int(string)

    def __str__(self):
        return str(self.number)

    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            return self.number == other
        return super().__eq__(other)

    def __int__(self):
        return int(self.string)

    def __float__(self):
        return float(self.string)

    def __add__(self, other):
        return self.number + other

    def __radd__(self, other):
        return other + self.number

    def __sub__(self, other):
        return self.number - other

    def __rsub__(self, other):
        return other - self.number

    def __mul__(self, other):
        return self.number * other

    def __rmul__(self, other):
        return other * self.number

    def __truediv__(self, other):
        return self.number / other

    def __rtruediv__(self, other):
        return other / self.number

    def __floordiv__(self, other):
        return self.number // other

    def __rfloordiv__(self, other):
        return other // self.number

    def __lt__(self, other):
        return self.number < other

    def __gt__(self, other):
        return self.number > other


class String(Atom):
    def __init__(self, string):
        super().__init__(string)


class Bool(Atom):
    def __init__(self, string):
        super().__init__(string)

    def __bool__(self):
        return self.string[1] == 't'
