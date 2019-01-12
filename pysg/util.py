from pysg.error import PyrrTypeError


def pyrr_type_checker(var: object, var_type: type) -> object:
    """ Makes sure that pyrr types are used as input. Tries to cast and raises PyrrTypeError if not possible.

    Args:
        var: Input variable.
        var_type: Type of input variable.

    Returns:
        Variable in correct type. Otherwise raise PyrrTypeError exception.

    """
    if type(var) is not var_type:
        try:
            return var_type(var)
        except Exception as e:
            raise PyrrTypeError(var, "Unsupported type. Expected %s type as input" % var_type)
    return var
