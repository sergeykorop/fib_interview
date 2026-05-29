import unittest
import fib
import itertools


class TestFibonacciBlocks(unittest.TestCase):
    def test_generate(self):
        fb = fib.Blocks()
        self.assertEqual(fb.next_values(1), [0])
        self.assertEqual(fb.next_values(2), [1, 1])
        self.assertEqual(fb.next_values(4), [2, 3, 5, 8])
        self.assertEqual(fb.next_values(1), [13])

class TestFibonacciOldSchool(unittest.TestCase):
    def test_generate(self):
        fo = fib.OldSchool()
        self.assertEqual(fo.next_value(), 0)
        self.assertEqual([fo.next_value(), fo.next_value()], [1, 1])
        self.assertEqual([fo.next_value() for i in range(4)], [2, 3, 5, 8])
        self.assertEqual(fo.next_value(), 13)

class TestFibonacciCallable(unittest.TestCase):
    def test_generate(self):
        fc = fib.Callable()
        self.assertEqual(fc(), 0)
        self.assertEqual([fc(), fc()], [1, 1])
        self.assertEqual([fc() for i in range(4)], [2, 3, 5, 8])
        self.assertEqual(fc(), 13)

class TestFibonacciIterable(unittest.TestCase):
    def test_generate(self):
        fi = iter(fib.Iterable())
        self.assertEqual(next(fi), 0)
        self.assertEqual(list(itertools.islice(fi, 2)), [1, 1])
        self.assertEqual(list(itertools.islice(fi, 4)), [2, 3, 5, 8])
        self.assertEqual(next(fi), 13)

class TestFibSeq(unittest.TestCase):
    def test_generate(self):
        fs = fib.seq()
        self.assertEqual(next(fs), 0)
        self.assertEqual(list(itertools.islice(fs, 2)), [1, 1])
        self.assertEqual(list(itertools.islice(fs, 4)), [2, 3, 5, 8])
        self.assertEqual(next(fs), 13)

class TestFibNthSeq(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual([fib.nth_seq(i) for i in [3, 5, 6, 4]], [2, 5, 8, 3])

class TestFibNthRec(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual([fib.nth_rec(i) for i in [3, 5, 6, 4]], [2, 5, 8, 3])

class TestFibNthMem(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual([fib.nth_mem(i) for i in [3, 5, 6, 4]], [2, 5, 8, 3])

class TestFibNthDec(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual([fib.nth_dec(i) for i in [3, 5, 6, 4]], [2, 5, 8, 3])

class TestFibMul2x2(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual(fib._mul_2x2([[1,2],[3,4]], [[5,6], [7,8]]), [[19, 22], [43, 50]])

class TestFibPow2x2(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual(fib._pow_2x2([[1,2],[3,4]], 17), [[617852597821, 900475124662], [1350712686993, 1968565284814]])

class TestFibNthMtx(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual([fib.nth_mtx(i) for i in [3, 5, 6, 4]], [2, 5, 8, 3])

if __name__ == '__main__':
    unittest.main()
