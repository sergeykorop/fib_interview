<!-- -*- coding: utf-8 -*- -->

# Coding Interview with Fibonacci Numbers: Down the Rabbit Hole

Imaginary coding interview using Fibonacci numbers as single showcase
for a surprising variety of programmers' skills.

Published: 2026-05-30.

Originally published at [Code Project](https://web.archive.org/web/20250820155905/https://www.codeproject.com/Articles/5374743/Coding-Interview-with-Fibonacci-Numbers-Down-the-R), 2023-12-27. 

[[Source Code](https://github.com/sergeykorop/fib_interview/)]

## Introduction

What could software developers say about Fibonacci numbers and coding
interviews? While most of us would likely agree that interview is
aimed to expose the best of our knowledge and experience, Fibonacci
numbers probably have a reputation of coding exercise for
beginners. Is it possible, however, to blend these two notions into
something useful?

Thinking a bit more about this subject, I came to quite an unexpected
conclusion: despite the&nbsp; seeming simplicity of Fibonacci numbers,
we can use them to develop several code snippets using a plethora of
programming techniques. We can also perform some decent asymptotic
complexity analysis without diving into the math too deeply.

Putting it all together, I could imagine a proof-of-concept scenario
of such interview session. This scenario is definitely artificial: the
interviewer always asks the question expected by the candidate, who is
ready to answer. In order to make things more close to reality of
junior-grade interview, I used a programming language which is not
completely familiar to me and performed all the math without looking
at the textbooks (except for one beautiful formula) trading,
therefore, rigor for simplicity. I should also notice that code and
math used in this article are in no way something new so I would never
claim for authorship. Finally, you will surely notice that I've
written much more text than code. _Mea culpa._ I'm a fond of
these words written by E. W. Dijkstra about 50 years ago
[[1](#ref.1), p. 39]:

> ... it is hard to claim that you know what you are doing unless you
  can present your act as a deliberate choice out of a possible set of
  things you could have done as well.

Nevertheless, I hope someone could find my writing at least amusing or
even learn something useful.

## Background and Conventions

The intended audience of this article are&nbsp;beginning software
developers and/or students learning the basics of the computer
science. Seasoned developers are welcome but they will unlikely see
anything new for them.

Code snippets are written using Python (v3.10 from Anaconda 2023.03)
so intermediate knowledge of this language is needed.

The text below uses some typesetting conventions to separate different parts of the dialogue:

* Plain text (like this) is used for the candidate speech which comprises most of the text below.

* Interviewer questions look like quotations:
  > **Interviewer:**  
    Could you tell us more about this topic, please?
    
* Comments which are expected to be useful to the reader but
  inappropriate to be said aloud during the real interview are like
  this:
  > **Note:**  
  Note the use of assignment statement.

## Level 0: A Variety of Implementations

> **Interviewer:**  
Ok, let's begin. How would you like to implement a program calculating
a Fibonacci numeric sequence?

> **Note:**  
Our imaginary interviewer prefers the &ldquo;open&rdquo; questions,
leaving much of the initiative to the candidate.


I would start from the definition of this sequence. Let's specify it
with following recurrent rule:

$$
F_0 = 0,\; F_1 = 1, \; F_i = F_{i-1} + F_{i-2} \; \mbox{for $i \ge 2$}.
$$

> **Note:**  
This &ldquo;user requirement&rdquo; seems to be too obvious to
clarify it explicitly, but software developers should always make sure
they understand their client properly. Despite the Fibonacci sequence
looking too simple to make a mistake, some textbooks define it
differently, omitting $F_0$. I've also seen a programming exercise
where Fibonacci sequence had been extended towards $-\infty$, that is,
$F_{-1}=1$, $F_{-2}=-1$, $F_{-3}=2$ and so on.


Assuming that we could present our solution with printing the first
$n$ Fibonacci numbers, this piece of code seems be sufficient to begin
a discussion:

```python
n = int(input("Enter series length: "))

assert(n >= 1)

past_item, current_item = 1, 0

for i in range(n):
    print(current_item)
    past_item, current_item = current_item, past_item + current_item
```

> **Note:**  
Note the use of so called "parallel assignment" statement which
often allows avoiding temporary variables.
>
> Also, this code takes me back to my high school years, except that I
would use Pascal or even BASIC that time.


> **Interviewer:**  
Looks good for beginning. Now, do you see any way to improve your solution?

User requirements are the top priority for improvement, but since we
currently have no new ones, we can devote our attention to making our
code better according to software engineering best practices.

Our current implementation doesn't meet two important criteria: the
code is neither _reusable_ nor _maintainable_. Indeed, we can see two
interspersed activities: calculating Fibonacci numbers and performing
input/output operations. We can't, therefore, easily use these
calculations for some other purpose or modify them without
understanding the output part and vice versa.

> **Note:**
Talking about &ldquo;problems&rdquo; with reusability and maintainability of
this simple peace of code is, surely, exaggerated. However, it could
be very important to show that you are aware of these concepts and
value them.

Therefore, we should separate Fibonacci numbers calculation from output.

> **Interviewer:**  
Agree. Given that our time is limited, let's omit the I/O details and
discuss the computation of our numbers only.

Current implementation uses global variables to keep the current and
the past produced numbers (or the computation _state_). This,
for example, makes it impossible to produce multiple number series at
once. In order to improve that, we should store our state into some
appropriate _data structure_. In our case, any data structure
capable of storing two integer numbers is sufficient (e.g., pair,
two-element array or list, whatever) but the most convenient choice
would be an _object_ in a sense of object-oriented programming
paradigm because this makes it easier to integrate our solution with
other code in our language of choice which encourages using this
approach.

> **Note:**  
> Despite of elements of
[functional programming](https://en.wikipedia.org/wiki/Functional_programming)
becoming more and more popular, Python, in my opinion, remains more
object-oriented than functional.

Next design decision we must take right now is even more important
than the previous one: how should we produce our numbers? Different
problems may require different &ldquo;access patterns&rdquo;: sometimes, it is
convenient to produce numbers in sequence, one by one or in blocks of
some size, but sometimes we need only a subset of those numbers in
random order.

> **Interviewer:**  
Why do you think this decision is so important?

Because our choice directly determines the lifetime of our code. Most
of the programs are not carved in stone, so we must modify them as
time goes. Properly chosen abstraction can withstand these changes
longer. However, we must also understand that given new and new
requirements to our software, we will eventually overcome the reserve
of flexibility of the original design choices and should be ready to
take a step forward and review them, sometimes completely.

> **Note:**  
Frederick Brooks [said](https://en.wikiquote.org/wiki/Fred_Brooks)
&ldquo;plan to throw one away&rdquo; meaning the prototype version of some
software system. I feel, this is also true regarding any other code as
well.

So far, let's begin from one possible solution written in pretty
old-school object-oriented style which could also suit well for other
languages than Python:

```python
class OldSchool:
    def __init__(self):
        self._past_item = 1
        self._current_item = 0

    def next_value(self):
        self._past_item, self._current_item = self._current_item, self._past_item + self._current_item

        return self._past_item
```

Putting this code to separate source file, say, `fib.py`, we create a
[module](https://docs.python.org/3/reference/import.html) which could
be used in multiple programs.

In order to produce a sequence of Fibonacci numbers, we should now
create an instance of `OldSchool` class and call `next_value` as many
times as needed to retrieve one more item of this sequence:

```python
import fib

fo = fib.OldSchool()

print([fo.next_value(), fo.next_value(), fo.next_value()])
print([fo.next_value(), fo.next_value()])
```

The output is:

```text
[0, 1, 1]
[2, 3]
```

> **Note:**  
Naming conventions in the code for this article came from my habit of
using fully qualified names of imported entities (possibly introducing
some short alias for long module name) whenever possible. Your
preferences may vary.

Even more, we can create multiple objects and produce many sequences simultaneously:
```python
fo1 = fib.OldSchool()
fo2 = fib.OldSchool()
print([[fo1.next_value(), fo1.next_value()], [fo2.next_value()], [fo1.next_value()], [fo2.next_value()]])
print([[fo1.next_value()], [fo2.next_value(), fo2.next_value()], [fo1.next_value()], [fo2.next_value()]])
```

The output is:
```text
[[0, 1], [0], [1], [1]]
[[2], [1, 2], [3], [3]]
```

Given the code snippets above, we can conclude that our current
implementation can be reused in various ways (either in different
programs or producing multiple sequences within one program). Also,
since the implementation details are hidden and can be changed without
a need to rework the &ldquo;client&rdquo; code, we have also achieved some
better degree of maintainability.

Automated [unit tests](https://en.wikipedia.org/wiki/Unit_testing)
could be even more important for maintainability since they provide
early diagnostics of errors inevitable when code is changed. Making
code reusable is, in turn, absolutely necessary for unit testsing.

> **Interviewer:**  
Ok. I'm agree about the importance of unit tests but let's postpone
discussing them for a time being. You have mentioned above that an
alternative implementation is possible which generates blocks of
numbers. Do you have any arguments to prefer producing the same
sequence one item by one?

Yes, we could possibly change our implementation to something like this:
```python
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
```

This could greatly simplify our current task:
```python
fb = fib.Blocks()

print(fb.next_values(3))
print(fb.next_values(4))
```

The output is:
```text
[0, 1, 1]
[2, 3, 5, 8]
```

However, thinking out of the box, we can foresee an unwanted
consequence of block-oriented approach: we generate all numbers in
advance even if we consume them later item by item. Given that block
size could be large, the unnecessary memory consumption and
performance loss due to adding items to the list could be
noticeable. So, it seems to be preferable to produce our sequence item
by item which we can always pack to the list when needed using, for
example,
[list comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions):
```python
fo = fib.OldSchool()
print([fo.next_value() for i in range(5)])

[0, 1, 1, 2, 3]
```

> **Note:**  
While problem with producing too large data blocks looks a bit
exaggerated regarding Fibonacci numbers, this could be actual for
other sequential data in the real life. Don't miss your chance to show
that you are aware of it.

> **Interviewer:**  
You have mentioned that your approach is somewhat old school and
applicable to other languages. Can you show us some more improvements
of your code which are specific to Python?

One possible way would be using
[special method](https://docs.python.org/3/reference/datamodel.html#specialnames)
named `__call__` to make our code more concise.  This kind of
[syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar)
doesn't change neither memory consumption nor execution speed but
improves, so to say, our visual experience.

```python
class Callable(OldSchool):
    def __call__(self):
        return self.next_value()
```
Note we reused our existing code one more time via
[inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance).

```python
fc = fib.Callable()
print([fc(), fc(), fc()])
print([fc() for i in range(4)])
```

The output is:
```text
[0, 1, 1]
[2, 3, 5, 8]
```

> **Note:**  
For the purposes of the interview, using special methods also allows
you to show that you are aware of some less known language
features.

Another improvement could be making our class
[iterable](https://docs.python.org/3/glossary.html#term-iterable):
```python
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
```

This class looks completely different but it also reuses `OldSchool`,
this time via aggregation.

While our former improvement with making object &ldquo;callable&rdquo; has been
only cosmetic, the latter one has much greater impact: this way, we
integrate our code into a generic language infrastructure using so
called &ldquo;[iterator protocol](https://docs.python.org/3/library/stdtypes.html#iterator-types)&rdquo;:

```python
import itertools

fi = iter(fib.Iterable())

print(next(fi))
print(list(itertools.islice(fi, 2)))
print(list(itertools.islice(fi, 4)))
print(next(fi))
```

The output is:
```text
0
[1, 1]
[2, 3, 5, 8]
13
```

Note that [`itertools`](https://docs.python.org/3/library/itertools.html#module-itertools)
module allows us doing much more than simply collecting data from iterable object:
```python
print(sum(itertools.takewhile(lambda x: x < 30, fib.Iterable())))
```

The output is:
```text
54
```

This expression takes first items from the Fibonacci sequence until
their value exceeds 30 and calculates their sum, all in one line of
code.

> **Note:**  
Although this style of programming could look quite confusing for
beginners, I would strongly advice to learn it.

> **Interviewer:**  
Indeed, this programming style is very concise and expressive. Can you
tell me, please, a bit more about its strong and weak
points?

Putting aside expressive power, I could also say this approach does
quite efficiently: the code implementing iterable simply produces one
item by one as long as they are consumed by caller but no more.

Regarding its weakness, it is naturally applicable to one-pass
algorithms consuming sequence items more or less in order of their
appearance (one by one or by limited-size chunks), other item access
patterns could require other abstractions. Also, as we could see,
implementing iterator protocol requires some boilerplate code and
could be non-intuitive.

> **Interviewer:**  
Any ideas how to improve it?

The boilerplate code could be produced automatically if we rewrite our iterable as
[generator](https://docs.python.org/3/reference/datamodel.html#generator-functions)
function:
```python
def seq():
    past_item, current_item = 1, 0

    while True:
        yield current_item
        past_item, current_item = current_item, past_item + current_item
```

This special function (note the use of `yield`) being called
effectively returns an iterable similar to our `fib.Iterable` but with
all the needed machinery created automatically under the hood. It can
be used exactly as above:
```python
print(sum(itertools.takewhile(lambda x: x < 30, fib.seq())))
```

The output is:
```text
54
```

> **Interviewer:**  
So, can generators be considered as ultimate solution for making sequences?

It depends. In most cases, they are indeed more than enough but
sometimes we could need an additional control over iteration. For
example, some algorithms (e.g., parsers) could require an ability to
&ldquo;look ahead&rdquo; or inspect the incoming item without consuming
it. Similarly, some problems could require saving the current state of
the iterator and restoring it back. In all these cases, custom
iterable object could provide the needed methods.

## Level 1: Fighting with Complexity

> **Interviewer:**  
Well, let's now consider another usecase: we need to produce a subset
of Fibonacci sequence referring to its items by index, in random
order. Could we probably reuse some code we have recently
discussed?

No, unfortunately, we can't. This time, we have got exactly that
problem I mentioned before: every decision has its limits. We could
try to reuse our existing code like this:
```python
def nth_seq(n):
    assert (type(n) is int and n >= 0)

    if n < 0:
        raise ValueError("Item index must be non-negative")

    return next(itertools.islice(seq(), n, None))
```

At first glance, this works as expected and looks nice:
```python
print([fib.nth_seq(i) for i in [3, 5, 6, 4]])
```

The output is:
```text
[2, 5, 8, 3]
```

However, the performance of this solution is unfeasible. Indeed,
producing number given index $n$ we re-generate the entire subsequence
$F_0$, $\ldots$, $F_n$ under the hood. Using
[big $O$ notation](https://en.wikipedia.org/wiki/Big_O_notation),
the complexity of `nth_seq(n)` is $O(n)$.

This complexity may look acceptable when we produce a single number
but if we need, say, $m$ numbers, these $O(n)$s are accumulated.

> **Interviewer:**  
Can you provide some better estimate, please?

Better estimate requires some additional knowledge about $n$ which
could be different for every $m$. For example, if we try to generate a
sequence of randomly shuffled first $m$ Fibonacci numbers from a set
of pre-shuffled indices, we could call `nth_seq` $m$ times, once for
each value of $0 \le i < m$, at random order. In this case, we
produce $i+1$ Fibonacci numbers for each $i$ (remember, we index our
sequence from zero) and the total number of produced items is

$$
\sum_{i=0}^{m-1}(i+1) = \sum_{i=1}^m i = (1 + m) \frac{m}{2}
$$

which, in turn, corresponds to complexity $O(m^2)$.

> **Note:**  
In real life, I would propose to produce a sequence of Fibonacci
numbers first and then shuffle them, if possible, but restricting our
problem setting with pre-shuffled indices allows us to showcase this
estimate.

> **Interviewer:**  
What about using recursive formula mentioned at the beginning of our
conversation?

Putting this formula directly to the code, we could get quite an
elegant function:
```python
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
```

Unfortunately, this function has significantly worse performance estimation.
Indeed, if we expand our formula:

$$
F_i = F_{i-2} + F_{i-1} = F_{i-2} + (F_{i-2} + F_{i-3}),
$$

we can see that $F_{i-2}$ is calculated twice. Therefore, the amount
of work needed to calculate the $i\mbox{-th}$ number is _at least_
twice more than for its pre-predecessor. Since this doubling, in turn,
occurs for the $(i-2)\mbox{-th}$ item as well and so on, we can
conclude that the _lower boundary_ of our complexity estimate
would be

$$
\Omega(2^{\lfloor \frac{n}{2}\rfloor}).
$$

Note this boundary is overly optimistic: we don't take into account
the amount of work needed to calculate $F_{i-3}$.

Looking at this function, we can conclude that it is stepwise,
non-decreasing and grows at even values of $n$:

$$
2^{\lfloor \frac{n}{2}\rfloor} = 2^{\frac{n}{2}} = (\sqrt{2})^{n} \approx 1.414214^{n} \quad \mbox{for even $n$}.
$$

This quick check leads us to unfortunate conclusion: our `nth_rec` has
exponential complexity which is even worse than our initial attempt.

> **Note:**  
This estimation in fact sweeps too much under the carpet. Those who
would like to see more detailed and precise reasoning could probably
find it [here](https://www.geeksforgeeks.org/time-complexity-recursive-fibonacci-program).

> **Interviewer:**  
Any ideas for further improvement?

Yes, we can get rid of the combinatory explosion occurring in this
function with technique known as
&ldquo;[memoization](https://en.wikipedia.org/wiki/Memoization)&rdquo;:
```python
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
```

The basic idea of this approach: each Fibonacci number being
calculated for the first time is saved to the map using number index
as a key. When it is needed later, we get it from the map and reuse
instead of recalculating from scratch.

This improvement, looking so simple, has drastic effect:
```python
print(fib.nth_mem(50))
```

outputs
```text
12586269025
```

Recursive implementation will unlikely be able to produce this result
in a reasonable amount of time.

> **Interviewer:**  
Yes, this optimization does real magic. What is the time complexity of
memoized implementation?

Let's calculate the cost of $m$ calls of `nth_mem` where $n_{max}$ is
the largest Fibonacci number index used within those $m$ calls. Given
that we have a decent dictionary implementation providing us a
constant amortized cost of individual add/lookup operations, we can
say that the cost of filling the table of $n_{max}$ Fibonacci numbers
is $O(n_{max})$. Indeed, calculating each next number from known
predecessors would require a constant amount of work (getting two
numbers from dictionary and storing their sum). After all those
$n_{max}$ numbers are calculated, all subsequent calls of `fib_mem`
also require constant time (getting the precalculated number from
dictionary).

Therefore, we have two cases: when $n_{max}$ dominates over $m$, the
overall time complexity is $O(n_{max})$, otherwise we have
$O(m)$. Putting it all together, we can write the resulting estimate
as $O(\max(n_{max}, m))$ or $O(n_{max} + m)$.

By the way, this estimate particularly means that if we use `nth_mem`
to produce a sequence of Fibonacci numbers calling it with index
growing from $0$ up to some $n$ the entire time complexity of this
process would also be $O(n)$, the same as we could get using some of
our sequential implementations, say, `seq`.

> **Interviewer:**  
Looks great! From initial quadratic through exponential, we could
finally get linear time! I should notice, however, that `fib_mem`
contains code related to our application domain (calculating Fibonacci
numbers) together with implementation details of memoization making it
less clear. Can we do better?

Following our initial goal of making our code reusable, we can
separate the implementation of table lookup from some specific
calculations using Python feature known as
[decorator](https://docs.python.org/3/glossary.html#term-decorator):
```python
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
```

As we can see, function `nth_dec` keeps the definition of Fibonacci
number free from implementation details, while its performance is
comparable to `nth_mem`. Meanwhile, the `memoize` decorator can also
be used to add memoization to other functions with no efforts.

## Level 2: Curiouser and Curiouser

> **Interviewer:**  
Coming back to that you said earlier, can we use some of memoized
implementations, `nth_mem` or `nth_dec`, as a replacement of our
sequence-oriented code given they both have an $O(n)$ time complexity
when it comes to produce the first $n$ Fibonacci numbers?

I wouldn't recommend making such a decision because this estimation is
asymptotic and includes a hidden coefficient which could make a
substantial difference in realistic scenarios. Putting it simpler, the
sequential generator simply calculates the next number updating a pair
of state variables while our memoized recursive function ends up with
maintaining a dictionary requiring therefore more efforts. Besides
that, we should also take into account memory consumption.

> **Interviewer:**  
By the way, can we possibly estimate memory complexity of memoization
as well?

Unlike time complexity, where we can usually analyze the performance
of some data structure putting aside the nature of stored objects,
memory complexity inherently depends from the nature of data, so we
can't make any statements in general.

Fibonacci numbers, however, allows us to do something better. In order
to make things simpler, we won't take into account the cost of
bookkeeping, that is, the amount of memory needed to store a
dictionary with $n$ entries (this amount greatly depends on the
implementation of this dictionary) and try to estimate the memory
needed to store these numbers themselves.

Let's begin from simple fact that memory needed to store some number
$x$ can be estimated by its logarithm $\log x$ (for asymptotic
analysis, the logarithm base can be arbitrary).

Can we estimate a logarithm of some Fibonacci number? Fortunately, we
can do that using the so called
[Binet's formula](https://en.wikipedia.org/wiki/Fibonacci_sequence#Closed-form_expression):

$$
F_i = \frac{\varphi^i - \psi^i}{\sqrt 5},
$$

where

$$
\varphi = \frac{1 + \sqrt 5}{2} \approx 1.618034, \quad \psi = 1 - \varphi = \frac{1 - \sqrt 5}{2} \approx -0.618034.
$$

Let's try to estimate the lower boundary for this expression. For
beginning, we can notice that $\psi^i < 0$ for odd values of
$i$. Therefore, we can state that

$$
F_i > \frac{\varphi^i}{\sqrt 5} \qquad \mbox{for odd $i$}.
$$

For even values of $i$, we can use the fact that $F_{i+1} > F_{i}$, therefore

$$
F_i > F_{i-1} > \frac{\varphi^{i-1}}{\sqrt 5} \qquad \mbox{for even $i$}.
$$

The latter boundary for even indices is also applicable to odd indices
as well, although it would be less accurate. However, it allows us to
get a common estimate:

$$
F_i > \frac{\varphi^{i-1}}{\sqrt 5},
$$

therefore

$$
F_i = \Omega(\varphi^i).
$$

The same approach is applicable to logarithm of $F_i$:

$$
\log F_i > \log \frac{\varphi^{i-1}}{\sqrt 5} = (i - 1) \log\varphi - \log\sqrt{5},
$$

so

$$
\log F_i = \Omega(i).
$$

> **Interviewer:**  
Looks very impressive! I've never had an idea of this relationship
between Fibonacci number and its index. Can we possibly get some
evidence these estimations are correct?

We can try to calculate this lower boundary for some part of the
sequence and see how it looks like. By the way, this would be a good
opportunity to see how our sequence generator works together with some
tools from standard library:
```python
phi = (1 + math.sqrt(5)) / 2

logF_lb = map(lambda i, F_i: ((i - 1) * math.log(phi) - math.log(math.sqrt(5)), math.log(F_i)), 
              itertools.count(1),
              itertools.islice(fib.seq(), 1, None))

print(list(itertools.islice(logF_lb, 10)))
```

This code snippet is written in functional style. We process two
infinite lists using built-in
[`map`](https://docs.python.org/3/library/functions.html#map)
function: the first is just a stream of indices and the second is a
sequence of Fibonacci numbers. Starting zero item of the sequence is
omitted to avoid `ValueError` raised by `math.log`. The lambda
expression passed to `map` calculates both the lower boundary estimate
and effective logarithm of Fibonacci number returning them as a pair.

Note that the real computations occur only when resulting sequence is
effectively consumed, that is, when we extract the first 10 items from
`logF_lb` converting them to list and printing.

The produced output is (split by lines for better readability):
```text
[(-0.8047189562170503, 0.0), (-0.3235071311574468, 0.0), 
 (0.1577046939021567, 0.6931471805599453), (0.6389165189617603, 1.0986122886681098), 
 (1.1201283440213636, 1.6094379124341003), (1.601340169080967, 2.0794415416798357), 
 (2.082551994140571, 2.5649493574615367), (2.563763819200174, 3.044522437723423), 
 (3.0449756442597775, 3.5263605246161616), (3.5261874693193813, 4.007333185232471)]
```

As we can see, each lower boundary estimate (the first item) is indeed
less than the corresponding logarithm value (the second item).

> **Interviewer:**  
So, how can we use these estimates to get memory complexity?

As I've said earlier, amount of memory needed to store some number is
proportional to its logarithm. Let's assume that we have produced some
Fibonacci numbers whose indices are less or equal to $n$. In this
case, the amount of memory needed to store memoized values can be
estimated as

$$
\sum_{i=1}^{n} \log F_i.
$$

Note that we ignore $F_0=0$ since its logarithm is undefined. Dropping
fixed amount of items at the beginning of sequence is allowed when we
do asymptotic analysis.

The lower boundary of this sum:

$$
\sum_{i=1}^{n} \log F_i > \sum_{i=1}^{n} \left( (i - 1) \log\varphi - \log\sqrt{5} \right).
$$

The right part of this inequality can in turn be transformed as

$$
\begin{align*}
\sum_{i=1}^{n} \left( (i - 1) \log\varphi - \log\sqrt{5} \right) & = \log\varphi \sum_{i=1}^{n} (i - 1) - n \log\sqrt{5} \\
                                                                 & = \log\varphi\, (n+1) \frac{n}{2} - n \left(\log\varphi+\log\sqrt{5}\right)\\
								 & = \frac{\log\varphi}{2} n^2 - \frac{\log\left(5\varphi\right)}{2} n.
\end{align*}
$$

Putting it all together, we have

$$
\sum_{i=1}^{n} \log F_i = \Omega(n^2).
$$

> **Interviewer:**  
> So, looks like we are doomed either to spend time calculating each
Fibonacci number from the beginning or need a plenty of memory to use
memoization. Both alternatives look painful when it comes to working
with reasonably large numbers.
>
> Is there any way to escape from this whack-a-mole situation? Could we
possibly use the Binet's formula to calculate the needed Fibonacci
number directly?

I wouldn't recommend doing this because using Binet's formula assumes
working with irrational numbers which can't be represented at full
precision. Also, the built-in support for real numbers usually
implements floating-point arithmetics following the ubiquitous
[IEEE 754 Standard](https://en.wikipedia.org/wiki/IEEE_754).
Assuming we use double-precision data format, we
can't expect that integers greater than $2^{53}$ can always be
represented without a loss of accuracy. Even worse, we can get
inaccurate results even well below this upper boundary due to various
subtle roundoffs and other pitfalls of floating-point computations.

Fortunately, Fibonacci numbers have some mathematical properties which
allow us to propose one very elegant solution. Let's recall our
sequential implementation: it has been based on saving two last items
of Fibonacci sequence and updating them on each step. This process can
be expressed using vector notation:

$$
\left\langle F_{i-1}, F_i \right\rangle = f(\left\langle F_{i-2}, F_{i-1}\right\rangle),
$$

where $f$ --- some transformation. Fibonacci sequence belongs to the
class of so called linear recurrencies and this transformation can be
represented as matrix multiplication:

$$
\begin{pmatrix}
  0 & 1 \\
  1 & 1 \\
\end{pmatrix}
\cdot \begin{pmatrix}
  F_{i-2} \\
  F_{i-1} \\
\end{pmatrix}
= \begin{pmatrix}
  0 \cdot F_{i-2} + 1 \cdot F_{i-1} \\
  1 \cdot F_{i-2} + 1 \cdot F_{i-1} \\
\end{pmatrix}
= \begin{pmatrix}
  F_{i-1} \\
  F_i \\
\end{pmatrix}.
$$

Note that we used this matrix product to transform current state of
our sequential Fibonacci sequence generator into the next state, that
is, to calculate next sequence item which is always kept at the second
item of state vector. Doing the next step requires one more matrix
product:

$$
\begin{pmatrix}
  0 & 1 \\
  1 & 1 \\
\end{pmatrix}
\cdot \begin{pmatrix}
  F_{i-1} \\
  F_{i} \\
\end{pmatrix}
= \begin{pmatrix}
  F_{i} \\
  F_{i+1} \\
\end{pmatrix}.
$$

Substituting our previous matrix product, we can see the pattern:

$$
\begin{pmatrix}
  0 & 1 \\
  1 & 1 \\
\end{pmatrix}
\cdot \begin{pmatrix}
  0 & 1 \\
  1 & 1 \\
\end{pmatrix}
\cdot \begin{pmatrix}
  F_{i-2} \\
  F_{i-1} \\
\end{pmatrix}
= \begin{pmatrix}
  0 & 1 \\
  1 & 1 \\
\end{pmatrix}^2
\cdot \begin{pmatrix}
  F_{i-2} \\
  F_{i-1} \\
\end{pmatrix}
= \begin{pmatrix}
  F_{i} \\
  F_{i+1} \\
\end{pmatrix}.
$$

That is, if we like to advance our current generator state by $n$
steps forward, we can do that immediately by multiplying this state by
our matrix raised to the power of $n$. And here comes the magic:
_we can calculate this power in logarithmic time_! The magic potion used
to do that is known as
[exponentiation by squaring](https://en.wikipedia.org/wiki/Exponentiation_by_squaring).

So, we can replace the Binet's formula with this one:

$$
\begin{pmatrix}
  F_{n-1} \\
  F_n \\
\end{pmatrix}
= \begin{pmatrix}
  0 & 1 \\
  1 & 1 \\
\end{pmatrix}^n
\cdot \begin{pmatrix}
  1 \\
  0 \\
\end{pmatrix},
$$

getting $F_n$ in $O(\log n)$ time (with $F_{n-1}$ coming as a free bonus).

The implementation of this algorithm is as follows:
```python
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
```

Let's try it:
```python
print([(i, len(str(fib.nth_mtx(i)))) for i in [200, 400, 600]])
```

As you can see, the number of decimal digits in produced Fibonacci numbers indeed grows linearly:
```text
[(200, 42), (400, 84), (600, 126)]
```

And finally, this statement is executed instantly:
```python
print(fib.nth_mtx(1000000) % 1000000)
```
producing:
```text
546875
```

I should also notice that if you have a pair of consecutive Fibonacci
numbers, say $\left\langle F_{i-1}, F_i \right\rangle$, you can use
the same approach to calculate the $n$-th number relatively to $i$,
that is, $\left\langle F_{i+n-1}, F_{i+n} \right\rangle$. Similarly,
we can step back, this time using another matrix. In case of Fibonacci
sequence this matrix can also be written down with minimum effort.

> **Interviewer:**  
Looks great! However, is there any real-life application of this
formula or it is nothing more than a salon trick only capable of
entertaining me and all those curious people who had the patience to
read our conversation till this point?

This approach can be used for any linear recurrence if you know the
corresponding matrix. Particularly, many popular pseudo-random number
generators are based on linear recurrence of some kind and this theory
allows us to split them on a number of independent &ldquo;streams&rdquo;. These
streams, in turn, are very useful when you need to parallelize or
distribute your calculations. (More about this interesting problem
could be read
[here](https://web.archive.org/web/20250820155905/https://www.codeproject.com/Articles/1239297/System-Random-and-Infinite-Monkey-Theorem).)

> **Interviewer:**  
That's enough for today. Thank you for the opportunity to look at the
Fibonacci numbers from this unusual point of view!

## Conclusion

Our imaginary interview came to its end. Our imaginary candidate got
his imaginary &ldquo;Yes&rdquo; from no less imaginary interviewer. Coming back
to the real world, what aspects of software engineering and Python
skills could we expose? Let's list them in order of appearance:

* A good habit of clarifying all the details of the task before coding it.

* Basic programming skills, like using the I/O and loops.

* Understanding the difference between simply solving the problem and
  creating reusable and maintainable code --- very important for
  software engineers, but sometimes missed by people who came to
  software development from academia.

* Understanding the fact that software design is a path to a proper
  balance between various possible solutions and, more importantly,
  that such balance is not carved in stone and will eventually require
  making some breaking changes.

* Using object-oriented approach to improve our initial solution.

* Using list comprehensions.

* Making our code more readable with Python special methods.

* Integrating our solution with the standard libraries provided by
  Python via iterator protocol.

* Reusing code either by inheritance or by aggregation.

* Doing elements of &ldquo;functional-like&rdquo; programming with `itertools`.

* Making our solution even more clear with Python generator.

* Performing some basic complexity analysis with &ldquo;big-$O$ notation&rdquo;.

* Using recursion.

* Improving recursive solution speed with memoization.

* Implementing reusable memoization with Python decorator.

* Using math to solve a problem which looked hopeless from purely
  engineering point of view (a quite rare stroke of luck in the real
  life, but in my opinion, a software engineer should be aware of this
  possibility and look for it whenever possible).

Looks not so bad for a &ldquo;freshmen-grade exercise&rdquo;, doesn't it? Is
this set of skills really enough to pass the interview? Different
roles require different blend of design, math and mere coding, so
there is no single answer. From my personal point of view, being aware
about the discussed topics should give you at least some additional
points and shouldn't harm.

Regarding my own takeaway experience gained from this article, I would
consider it positive: while I knew some things in advance before
starting it, quite a plenty of others were explored just in
progress. Hope you learned something useful to you as well.

## References

<span id="ref.1">[1]</span>
Edsger W. Dijkstra. Notes on structured programming. In _Structured Programming_, pages 1-82.
Academic Press Ltd., London and New York, 1972.
(Available [online](https://dl.acm.org/doi/10.5555/1243380.1243381).)

## History
* 27th December, 2023: Initial version
