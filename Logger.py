'''
Logging utility, don't run this file.
'''

INFO = 0
WARNING = 1
ERROR = 2

valid_levels_dict = {
    0: "INFO",
    1: "WARNING",
    2: "ERROR"
}


def log(input_level, function, *text,):
    if input_level in valid_levels_dict.keys():
        level = valid_levels_dict[input_level]
    elif input_level.upper() in valid_levels_dict.values():
        level = input_level.upper()
    else:
        raise SyntaxError("Level given \"" + input_level + "\" does not match the following accepted values: "
                          + str(valid_levels_dict.values()) + " or " + str(valid_levels_dict.keys()))
    print("[" + level + "]", end="")
    print(" (" + function + ")", end="")
    for stuff in text:
        print(" " + str(stuff), end="")
    print()


