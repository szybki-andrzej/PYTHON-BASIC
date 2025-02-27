"""
Write a function which divides x by y.
If y == 0 it should print "Division by 0" and return None
elif y == 1 it should raise custom Exception with "Deletion on 1 get the same result" text
else it should return the result of division
In all cases it should print "Division finished"
    >>> division(1, 0)
    Division by 0
    Division finished
    >>> division(1, 1)
    Division finished
    DivisionByOneException("Deletion on 1 get the same result")
    >>> division(2, 2)
    1
    Division finished
"""
import typing


class DivisionByOneException(Exception):
    pass


def division(x: int, y: int) -> typing.Union[None, str]:

    try:
        if y == 1:
            raise DivisionByOneException
        else:
            if x // y == x/y:
                return x // y
            else:
                return x/y

    except ZeroDivisionError:
        print("Division by 0")
        return None

    except DivisionByOneException:
        print('DivisionByOneException("Deletion on 1 get the same result")')

    finally:
        print("Division finished")


