BRACKETS = {'(': ')', '[': ']'}
SYMBOLS = {'!', '$', '%', '&', '*', '/', ':', '<', '=', '>', '?', '_', '~'}
SPECIAL = {'+', '-', '.', '@', '#'}
SIGN = {'+', '-'}


def find_compound_end(string, opening_bracket):
    closing_bracket = BRACKETS[opening_bracket]
    end = 0
    while end >= 0:
        end = string.find(closing_bracket, end + 1)
        if is_compound(string[1:end], opening_bracket):
            return end
    return -1


def is_compound(string, opening_bracket):
    string = remove_strings(string)
    if string is None:
        return False
    closing_bracket = BRACKETS[opening_bracket]
    end = 0
    has_compound = True

    while has_compound:
        start = string.find(opening_bracket, end)
        if start < 0:
            has_compound = False
        else:
            end = string.find(closing_bracket, start)
            if end < 0:
                return False
    return True


def remove_strings(string):
    end = 0
    has_string = True

    while has_string:
        start = string.find('"', end)
        if start < 0:
            has_string = False
        else:
            end = find_string_end(string, start + 1)
            if end < 0:
                return None
            string = string[:start] + string[end + 1:]
    return string


def find_string_end(string, start):
    is_escaped = True
    end = start - 1

    while is_escaped:
        end = string.find('"', end + 1)
        if end < 0:
            return end
        is_escaped = string[end - 1] == "\\"
    return end
