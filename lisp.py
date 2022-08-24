from classes import Number, Identifier, String, Bool, Compound
from utils import BRACKETS, SYMBOLS, SIGN, SPECIAL, find_string_end, find_compound_end


def parse(string):
    if len(string) == 0:
        return None
    if len(string) == 1:
        return create_single(string)
    else:
        return create_multi(string)


def create_single(string):
    if string.isdigit():
        return Number(string)
    if string in SIGN or string.isalpha() or string in SYMBOLS:
        return Identifier(string)
    return None


# Go through candidates for non-terminals, validate and create them.
def create_multi(string):
    if string[0] in SIGN and string[1].isdigit() or string[0].isdigit():
        if validate_number(string):
            return Number(string)
    elif string[0] == '"' and string[-1] == '"':
        if validate_string(string[1:-1]):
            return String(string)
    elif string == "#f" or string == "#t":
        return Bool(string)
    elif string[0].isalpha() or string[0] in SYMBOLS:
        if validate_identifier(string[1:]):
            return Identifier(string)
    elif string[0] in BRACKETS and string[-1] == BRACKETS[string[0]]:
        compound_list = create_compound_list(string[1:-1])
        if compound_list is None:
            return None
        if validate_compound_list(compound_list):
            return Compound(string, compound_list)
    return None


def validate_number(string):
    if string[0] == '+' or string[0] == '-':
        string = string[1:]
    dot = string.find('.')
    if dot >= 0:
        if not string[:dot].isdigit():
            return False
        if not string[dot + 1:].isdigit():
            return False
    else:
        if not string.isdigit():
            return False
    return True


def validate_string(string):
    string = string.replace(r'\\', '')
    string = string.replace(r'\"', '')
    return string.find("\\") == -1 and string.find(r'"') == -1


def validate_identifier(string):
    for char in string:
        if char.isalpha():
            continue
        if char in SYMBOLS:
            continue
        if char.isdigit():
            continue
        if char in SPECIAL:
            continue
        return False
    return True


# Create list of non-terminals from string.
def create_compound_list(string):
    if len(string) == 0 or string[0].isspace():
        return None
    exprs = []
    while len(string) > 0:
        string = string.lstrip()
        if string[0] == '"':
            end = find_string_end(string, 1)
            if end < 0:
                return None
        elif string[0] in BRACKETS:
            end = find_compound_end(string, string[0])
            if end < 0:
                return None
        else:
            end = string.find(' ') - 1
            if end < 0:
                end = len(string) - 1
        exprs.append(string[0: end + 1])
        string = string[end + 1:]
    return [parse(expr) for expr in exprs]


def validate_compound_list(compound_list):
    for item in compound_list:
        if item is None:
            return False
    return True
