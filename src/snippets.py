import fib
import itertools
import math

fb = fib.Blocks()

print(fb.next_values(3))
print(fb.next_values(4))

###
fb_1 = fib.Blocks()
fb_2 = fib.Blocks()

print(f'fb_1[:2] = {fb_1.next_values(2)}, fb_2[:3] = {fb_2.next_values(3)}, fb_1[2:6] = {fb_1.next_values(4)}')
print(f'{fb_1.next_values(2)=}, {fb_2.next_values(3)=}, {fb_1.next_values(4)=}')

###

fo = fib.OldSchool()
print([fo.next_value(), fo.next_value(), fo.next_value()])
print([fo.next_value(), fo.next_value()])

fo1 = fib.OldSchool()
fo2 = fib.OldSchool()

print([[fo1.next_value(), fo1.next_value()], [fo2.next_value()], [fo1.next_value()], [fo2.next_value()]])
print([[fo1.next_value()], [fo2.next_value(), fo2.next_value()], [fo1.next_value()], [fo2.next_value()]])

fo = fib.OldSchool()
print([fo.next_value() for i in range(5)])

###

fc = fib.Callable()

print([fc(), fc(), fc()])
print([fc() for i in range(4)])

###

fi = iter(fib.Iterable())

print(next(fi))
print(list(itertools.islice(fi, 2)))
print(list(itertools.islice(fi, 4)))
print(next(fi))

print(sum(itertools.takewhile(lambda x: x < 30, fib.Iterable())))
###

print(sum(itertools.takewhile(lambda x: x < 30, fib.seq())))

###

[fib.nth_seq(i) for i in range(3, 7)]

###

print(list(itertools.islice(fib.seq(), 50)))

print([x for x in itertools.islice(fib.seq(), 50)])

print(next(itertools.islice(fib.seq(), 49, None)))

###

def fib_cnt(n):
    if n < 2:
        return (1, 0)
    else:
        (prev_prev_val, prev_prev_count) = fib_cnt(n - 2)
        (prev_val, prev_count) = fib_cnt(n - 1)
        return (prev_prev_val + prev_val, prev_prev_count + prev_count + 2)


print(fib_cnt(3))
print(fib_cnt(5))
print(fib_cnt(7))

print([(fib_cnt(i)[1], math.pow(math.sqrt(2), i)) for i in range(15)])
print([(fib_cnt(i)[1], math.pow(2, (i // 2))) for i in range(15)])


phi = (1 + math.sqrt(5)) / 2
psi = 1 - phi

print(list(itertools.islice(
    zip(map(lambda i: (i, math.pow(phi, i-1) / math.sqrt(5.0)), itertools.count(0)), fib.seq()),
    10)))


def logF_lb():
    return map(lambda i, F_i: ((i - 1) * math.log(phi) - math.log(math.sqrt(5)), math.log(F_i)),
                itertools.count(1),
                itertools.islice(fib.seq(), 1, None))


print(list(itertools.islice(logF_lb(), 10)))

print(sum(itertools.islice(map(lambda x:x[0], logF_lb()), 10)))

n = 10
print(math.log(phi)/2 * math.pow(n,2) - n * math.log(5*phi)/2)

print(fib.nth_mtx(50))

print([(i, len(str(fib.nth_mtx(i)))) for i in [200, 400, 600]])

print(fib.nth_mtx(1000000) % 1000000)