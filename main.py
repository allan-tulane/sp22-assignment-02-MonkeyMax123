"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time
from math import ceil
import tabulate


class BinaryNumber:
    """ done """

    def __init__(self, n):
        self.decimal_val = n
        self.binary_vec = list('{0:b}'.format(n))

    def __repr__(self):
        return ('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))


def _quadratic_multiply(x, y):
    # x is a BinaryNumber
    # y is a BinaryNumber

    if str(type(x)) == "<class 'int'>":
        xbin = BinaryNumber(x)
    else:
        xbin = BinaryNumber(x.decimal_val)

    if str(type(y)) == "<class 'int'>":
        ybin = BinaryNumber(y)
    else:
        ybin = BinaryNumber(y.decimal_val)

    x_vec = xbin.binary_vec  # type list
    y_vec = ybin.binary_vec  # type list

    x_vec, y_vec = pad(x_vec, y_vec)
    n = len(x_vec)

    if xbin.decimal_val <= 1 and ybin.decimal_val <= 1:
        return BinaryNumber(xbin.decimal_val * ybin.decimal_val)

    else:
        x_left, x_right = split_number(x_vec)  # object type BinaryNumber
        y_left, y_right = split_number(y_vec)  # object type BinaryNumber

        left = (_quadratic_multiply(x_left.decimal_val, y_left.decimal_val))
        left_middle = (_quadratic_multiply(x_left.decimal_val, y_right.decimal_val))
        right_middle = (_quadratic_multiply(x_right.decimal_val, y_left.decimal_val))
        right = (_quadratic_multiply(x_right.decimal_val, y_right.decimal_val))
        middle = BinaryNumber(left_middle.decimal_val + right_middle.decimal_val)

        left = (bit_shift(left, n))
        middle = (bit_shift(middle, (n // 2)))
        result = BinaryNumber(left.decimal_val + middle.decimal_val + right.decimal_val)

        return BinaryNumber(result.decimal_val)


def binary2int(binary_vec):
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))


def split_number(vec):
    return (binary2int(vec[:len(vec) // 2]),
            binary2int(vec[len(vec) // 2:]))


def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)


def pad(x, y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y) - len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x) - len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x, y


def subquadratic_multiply(x, y):
    # x is a BinaryNumber
    # y is a BinaryNumber

    if str(type(x)) == "<class 'int'>":
        xbin = BinaryNumber(x)
    else:
        xbin = BinaryNumber(x.decimal_val)

    if str(type(y)) == "<class 'int'>":
        ybin = BinaryNumber(y)
    else:
        ybin = BinaryNumber(y.decimal_val)

    x_vec = xbin.binary_vec  # type list
    y_vec = ybin.binary_vec  # type list

    x_vec, y_vec = pad(x_vec, y_vec)
    n = len(x_vec)

    if xbin.decimal_val <= 1 and ybin.decimal_val <= 1:
        return BinaryNumber(xbin.decimal_val * ybin.decimal_val)

    else:
        x_left, x_right = split_number(x_vec)  # object type BinaryNumber
        y_left, y_right = split_number(y_vec)  # object type BinaryNumber

        left = (subquadratic_multiply(x_left.decimal_val, y_left.decimal_val))
        right = (subquadratic_multiply(x_right.decimal_val, y_right.decimal_val))

        left_middle = (x_left.decimal_val + x_right.decimal_val)
        right_middle = (y_left.decimal_val + y_right.decimal_val)
        middle_left = (subquadratic_multiply(left_middle, right_middle))
        middle = BinaryNumber(middle_left.decimal_val - left.decimal_val - right.decimal_val)

        left = (bit_shift(left, 2 * ceil(n // 2)))
        middle = (bit_shift(middle, ceil(n // 2)))
        result = BinaryNumber(left.decimal_val + middle.decimal_val + right.decimal_val)

        return BinaryNumber(result.decimal_val)


def test_multiply():
    assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(2)) == BinaryNumber(2 * 2)


def time_multiply(x, y, f):
    start = time.time()
    time.sleep(.1)
    f(x, y)
    end = time.time()
    return (end - start - .1) * 1000


def print_results(results):
    print(tabulate.tabulate(results,
                            headers=['n', 'Sub Quadratic Time', 'Quadratic Time'],
                            floatfmt=".3f",
                            tablefmt="github"))


def compare_multiply(fn_1, fn_2, sizes=[0, 10, 100, 1000, 10000, 100000, 1000000]):
    result = []
    for n in sizes:
        result.append((n, time_multiply(n, n, fn_1), time_multiply(n, n, fn_2)))
    return result


print_results(compare_multiply(subquadratic_multiply, _quadratic_multiply))
