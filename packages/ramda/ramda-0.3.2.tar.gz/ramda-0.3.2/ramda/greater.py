from ramda.curry import curry


@curry
def greater(a, b):
    return a if a >= b else b
