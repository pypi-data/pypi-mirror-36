from ramda.curry import curry
from ramda.map import map


@curry
def for_each(f, xs):
    """
    Execute a function for  each value of an iterable

    :param f: Unary function to execute
    :param xs: Any python iterable
    :return: Returns the original iterable
    """
    map(f, xs)
    return xs
