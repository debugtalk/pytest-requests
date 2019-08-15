
def equals(expected_value):

    def is_eq(actual_value):
        return actual_value == expected_value

    return is_eq


def greater_than(expected_value):

    def is_gt(actual_value):
        return actual_value > expected_value

    return is_gt


def less_than(expected_value):

    def is_lt(actual_value):
        return actual_value < expected_value

    return is_lt


# alias for validators
eq = equals
gt = greater_than
lt = less_than