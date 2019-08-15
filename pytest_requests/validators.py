
def equals(expected):

    def is_eq(actual_value):
        return actual_value == expected

    return is_eq


# alias for validators
eq = equals