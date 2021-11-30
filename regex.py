import sys
sys.setrecursionlimit(10000)


def match_character(regex: str, character: str) -> bool:
    return regex == "" or regex == "." or regex == character


def following_metacharacter(regex: str) -> str:
    if len(regex) > 1 and regex[1] in {"?", "*", "+"}:
        return regex[1]
    return ""


def match_metacharacter(regex: str, string: str, metacharacter: str) -> bool:
    if metacharacter == "?":
        if match_character(regex[0], string[0]):
            return match_left(regex[2:], string[1:])
        return match_left(regex[2:], string)
    elif metacharacter == "+":
        if regex[0] == ".":
            return match_anywhere(regex[2:], string[1:])
        if match_character(regex[0], string[0]):
            return match_left(regex[2:], string.lstrip(string[0]))
        return False
    else:
        if regex[0] == ".":
            return match_anywhere(regex[2:], string)
        if match_character(regex[0], string[0]):
            return match_left(regex[2:], string.lstrip(string[0]))
        return match_left(regex[2:], string)


def match_left(regex: str, string: str) -> bool:
    if regex and string:
        if regex[0] == "\\":
            return match_left(regex[1:], string)
        metacharacter_follows = following_metacharacter(regex)
        if metacharacter_follows:
            return match_metacharacter(regex, string, metacharacter_follows)
        elif match_character(regex[0], string[0]):
            return match_left(regex[1:], string[1:])
        return False
    return not regex


def match_right(regex: str, string: str) -> bool:
    if regex and string:
        if regex[1:2] == "\\":
            if regex[0] == string[0]:
                return match_right(regex[2:], string[1:])
            return False
        if regex[0] in {"?", "*", "+"} and len(regex) > 1:
            if regex[0] == "?":
                if match_character(regex[1], string[0]):
                    return match_right(regex[2:], string[1:])
                return match_right(regex[2:], string)
            elif regex[0] == "+":
                if match_character(regex[1], string[0]):
                    return match_right(regex[2:], string.lstrip(string[0]))
                return False
            else:
                if match_character(regex[1], string[0]):
                    return match_right(regex[2:], string.lstrip(string[0]))
                return match_right(regex[2:], string)
        elif match_character(regex[0], string[0]):
            return match_right(regex[1:], string[1:])
        return False
    return not regex


def match_anywhere(regex: str, text: str) -> bool:
    if regex and text:
        if match_left(regex, text):
            return True
        return match_anywhere(regex, text[1:])
    return not regex


def validate(regex: str, string: str) -> bool:
    if regex.startswith("^") and regex.endswith("\\$"):
        return match_left(regex[1:], string)
    if regex.startswith("^") and regex.endswith("$"):
        return match_left(regex[1:-1], string) and \
               match_right(regex[-2:0:-1], string[-1::-1])
    if regex.startswith("^"):
        return match_left(regex[1:], string)
    if regex.endswith("\\$"):
        return match_anywhere(regex, string)
    if regex.endswith("$"):
        return match_right(regex[-2:0:-1], string[-1::-1])
    return match_anywhere(regex, string)


def main():
    print(validate(*input().split("|")))


if __name__ == "__main__":
    main()
