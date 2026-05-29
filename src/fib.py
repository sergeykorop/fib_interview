# -*- coding: utf-8 -*-

import itertools


class OldSchool:
    def __init__(self):
        self._past_item = 1
        self._current_item = 0

    def next_value(self):
        self._past_item, self._current_item = self._current_item, self._past_item + self._current_item

        return self._past_item


class Blocks:
    def __init__(self):
        self._past_item = 1
        self._current_item = 0

    def next_values(self, n=1):
        assert (type(n) is int and n >= 0)

        if n < 0:
            raise ValueError("Block length must be non-negative")

        result = []

        for i in range(n):
            result.append(self._current_item)
            self._past_item, self._current_item = self._current_item, self._past_item + self._current_item

        return result


class Callable(OldSchool):
    def __call__(self):
        return self.next_value()


class Iterable:
    def __iter__(self):
        class FibIter:
            def __init__(self):
                self._seq = OldSchool()

            def __iter__(self):
                return self

            def __next__(self):
                return self._seq.next_value()

        return FibIter()


def seq():
    past_item, current_item = 1, 0

    while True:
        yield current_item
        past_item, current_item = current_item, past_item + current_item


def nth_seq(n):
    assert (type(n) is int and n >= 0)

    if n < 0:
        raise ValueError("Item index must be non-negative")

    return next(itertools.islice(seq(), n, None))


def nth_rec(n):
    assert (type(n) is int and n >= 0)

    if n < 0:
        raise ValueError("Item index must be non-negative")
    elif n == 0:
        return 0
    elif n <= 2:
        return 1
    else:
        return nth_rec(n - 2) + nth_rec(n - 1)


class _NthMem:
    def __init__(self):
        self._nums = {}

    def __call__(self, n):
        assert (type(n) is int and n >= 0)

        if n < 0:
            raise ValueError("Item index must be non-negative")
        elif n == 0:
            return 0
        elif n <= 2:
            return 1
        else:
            f_n = self._nums.get(n, None)

            if f_n is None:
                f_n = self(n - 2) + self(n - 1)
                self._nums[n] = f_n

            return f_n


nth_mem = _NthMem()


def memoize(f):
    class _MemF:
        def __init__(self, f):
            self._vals = {}
            self._f = f

        def __call__(self, x):
            y = self._vals.get(x, None)

            if y is None:
                y = self._f(x)
                self._vals[x] = y

            return y

    return _MemF(f)


@memoize
def nth_dec(n):
    assert (type(n) is int and n >= 0)

    if n < 0:
        raise ValueError("Item index must be non-negative")
    elif n == 0:
        return 0
    elif n <= 2:
        return 1
    else:
        return nth_dec(n - 2) + nth_dec(n - 1)


def _mul_2x2(x, y):
    return [[x[0][0] * y[0][0] + x[0][1] * y[1][0], x[0][0] * y[0][1] + x[0][1] * y[1][1]],
            [x[1][0] * y[0][0] + x[1][1] * y[1][0], x[1][0] * y[0][1] + x[1][1] * y[1][1]]]


def _pow_2x2(x, n):
    res = [[1, 0], [0, 1]]
    sq_i = x

    while n > 0:
        if n & 1 != 0:
            res = _mul_2x2(res, sq_i)
        sq_i = _mul_2x2(sq_i, sq_i)
        n >>= 1

    return res


def _mul_2x2_v(x, y):
    return [x[0][0] * y[0] + x[0][1] * y[1], x[1][0] * y[0] + x[1][1] * y[1]]


def nth_mtx(n):
    assert (type(n) is int and n >= 0)

    if n < 0:
        raise ValueError("Item index must be non-negative")
    else:
        A_n = _pow_2x2([[0, 1], [1, 1]], n)
        st_n = _mul_2x2_v(A_n, [1, 0])
        return st_n[1]
