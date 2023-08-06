import time
from collections import deque
from itertools import dropwhile, groupby, islice, takewhile, zip_longest
from typing import (Callable, Collection, Container, ContextManager, Hashable, Iterable, Optional,
                    Type)

__all__ = ["flu", "map_attr", "map_item", "as_flu", "with_iter"]


class Empty: ...


class Fluent:
    """Enables chaining of generator producing functions"""

    def __init__(self, iterable: Iterable) -> None:
        self._iterable = iter(iterable)

    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0:
            return Fluent(islice(self._iterable, key, key + 1))
        elif isinstance(key, slice):
            return Fluent(islice(self._iterable, key.start, key.stop, key.step))
        else:
            raise KeyError(
                "Key must be non-negative integer or slice, not {}".format(key)
            )

    ### Summary ###
    def collect(self, n: int = None, container_type: Type = list):
        """Consume items from the iterable into a container

        Note:
            Fluent.collect terminates a method chaining pipelines

        Args:
            n: the number of items to collect from the iterable
            container_type: class of data structure

        Returns:
            container_type with n elements from the iterable

        """
        return container_type(v for v in self.take(n))

    def sum(self):
        """Sum of elements in the iterable"""
        return sum(self)

    def count(self):
        """Count of elements in the iterable"""
        return sum(1 for _ in self)

    def min(self):
        """Smallest element in the interable"""
        return min(self)

    def max(self):
        """Largest element in the interable"""
        return max(self)

    def first(self, default=Empty()):
        """Return the first item of the iterble. Raise IndexError if empty or default if provided."""
        x = default
        for x in self:
            return x
        if isinstance(x, Empty):
            raise IndexError('Empty iterator')
        return default

    def last(self, default=Empty()):
        """Return the last item of the iterble. Raise IndexError if empty or default if provided."""
        x = default
        for x in self:
            pass
        if isinstance(x, Empty):
            raise IndexError('Empty iterator')
        return x

    def head(self, n: int = 10, container_type: Type = list):
        """Returns a collection of up to n elements, defaults to 10"""
        return self.take(n).collect(container_type=container_type)

    def tail(self, n: int = 10, container_type: Type = list):
        """Return up to last n elements"""

        
        for val in self.window(n, fill_value=Empty()):
            pass
        return container_type([x for x in val if not isinstance(x, Empty)])

    ### End Summary ###

    ### Non-Constant Memory ###
    def sort(self, key: Optional[Callable] = None, reverse=False):
        """Sort iterable by *key* function if provided or identity otherwise

        WARNING: sorting loads the entire iterable into memory
        """
        return Fluent(sorted(self, key=key, reverse=reverse))

    def groupby(self, key=lambda x: x, sort: bool = True):
        """Yield consecutive keys and groups from the iterable. Key defaults to identify function
        Iterable must be sorted on the same key function or *sort* set to True"""
        gen = self.sort(key) if sort else self
        return Fluent(groupby(gen, key)).map(lambda x: (x[0], Fluent(x[1])))

    def unique(self, key=lambda x: x):
        """Yield elements that are unique by a *key*"""
        def impl():
            seen = set()
            for x in self:
                x_hash = key(x)
                if x_hash in seen:
                    continue
                else:
                    seen.add(x_hash)
                    yield x
        return Fluent(impl())
    ### End Non-Constant Memory ###

    ### Side Effect ###
    def rate_limit(self, per_second=100):
        """Restrict consumption of iterable to n *per_second*"""

        def _impl():
            wait_time = 1.0 / per_second
            for val in self:
                start_time = time.time()
                yield val
                call_duration = time.time() - start_time
                time.sleep(max(wait_time - call_duration, 0.0))

        return Fluent(_impl())

    def side_effect(self, func: Callable, before: Optional[Callable] = None, after: Optional[Callable] = None):
        """Invoke *func* for each item in the iterable before yielding the item.
        *func* takes a single argument and the output is discarded
        *before* and *after* are optional functions that take no parameters and are executed once before iteration begins
        and after iteration ends respectively. Each will be called exactly once.

        think logging, progress bars, etc.
        """
        def impl():
            try:
                if before is not None:
                    before()
                
                for x in self:
                    yield func(x)
                
            finally:
                if after is not None:
                    after()

        return Fluent(impl())

    ### End Side Effect ###

    def map(self, func: Callable, *args, **kwargs):
        """Apply *func* to each element of iterable"""

        def __imp():
            for val in self._iterable:
                yield func(val, *args, **kwargs)

        return Fluent(__imp())

    def map_item(self, item):
        """Extracts *item* from every element of the iterable"""
        return self.map(lambda x: x[item])

    def map_attr(self, attr):
        """Extracts the attribute *attr* from each element of the iterable"""
        return self.map(lambda x: getattr(x, attr))

    def filter(self, func: Callable, *args, **kwargs):
        """Yield elements of iterable where *func* returns truthy"""

        def __imp():
            for val in self._iterable:
                if func(val, *args, **kwargs):
                    yield val

        return Fluent(__imp())

    def zip(self, iterable: Iterable):
        """Yields tuples containing the i-th element from the i-th
        argument in the chainable, and the iterable"""
        return Fluent(zip(self, iterable))

    def zip_longest(self, iterable: Iterable, fillvalue=None):
        """Yields tuples containing the i-th element from the i-th
        argument in the chainable, and the iterable
        Iteration continues until the longest iterable is exhaused.
        If iterables are uneven in length, missing values are filled in with fillvalue
        """
        return Fluent(zip_longest(self, iterable, fillvalue=fillvalue))

    def enumerate(self, start: int = 0):
        """Yields tuples from the chainable where the first element
        is a count from initial value *start*."""
        return Fluent(enumerate(self, start=start))

    def take(self, n: Optional[int] = None):
        """Yield first *n* items of the iterable"""

        def __imp():
            return islice(self._iterable, n)

        return Fluent(__imp())

    def takewhile(self, predicate: Callable):
        """Yield elements from the chainable so long as the predicate is true"""
        return Fluent(takewhile(predicate, self._iterable))

    def dropwhile(self, predicate: Callable):
        """Drop elements from the chainable as long as the predicate is true;
        afterwards, return every element"""
        return Fluent(dropwhile(predicate, self._iterable))

    def chunk(self, n: int):
        """Yield lists of elements from iterable in groups of *n*

        if the iterable is not evenly divisiible by *n*, the final list will be shorter
        """

        def __imp():
            while True:
                out = list(self.take(n))
                if out:
                    yield out
                else:
                    return

        return Fluent(__imp())

    def flatten(self, depth: int = 1, base_type: Type = None, iterate_strings=False):
        """Recursively flatten nested iterables (e.g., a list of lists of tuples)
        into non-iterable type or an optional user-defined base_type

        Strings are treated as non-iterable for convenience. set iterate_string=True
        to change that behavior.
        """

        def walk(node, level):
            if (
                ((depth is not None) and (level > depth))
                or (isinstance(node, str) and not iterate_strings)
                or ((base_type is not None) and isinstance(node, base_type))
            ):
                yield node
                return
            try:
                tree = iter(node)
            except TypeError:
                yield node
                return
            else:
                for child in tree:
                    for val in walk(child, level + 1):
                        yield val

        return Fluent(walk(self, level=0))

    def window(self, n: int, step: int = 1, fill_value: object = None):
        """Yield a sliding window of width *n* over the given iterable.

        Each window will advance in increments of *step*:

        If the length of the iterable does not evenly divide by the *step*
        the final output is padded with *fill_value*
        """

        def _imp():
            if n < 0:
                raise ValueError("n must be >= 0")
            if n == 0:
                yield tuple()
                return
            if step < 1:
                raise ValueError("step must be >= 1")

            window = deque([], n)
            append = window.append

            # Initial deque fill
            for _ in range(n):
                append(next(self, fill_value))
            yield tuple(window)

            # Appending new items to the right causes old items to fall off the left
            i = 0
            for item in self:
                append(item)
                i = (i + 1) % step
                if i % step == 0:
                    yield tuple(window)

            # If there are items from the iterable in the window, pad with the given
            # value and emit them.
            if (i % step) and (step - i < n):
                for _ in range(step - i):
                    append(fill_value)
                yield tuple(window)

        return Fluent(_imp())

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iterable)


def flu(iterable: Iterable) -> Fluent:
    return Fluent(iterable)


def map_item(iterable: Iterable, item: Hashable) -> Fluent:
    return Fluent(iterable).map_item(item)


def map_attr(iterable: Iterable, attr: str) -> Fluent:
    return Fluent(iterable).map_attr(attr)


def with_iter(context_manager: ContextManager):
    with context_manager as cm:
        for rec in cm:
            yield rec


def as_flu(func: Callable) -> Callable:
    """Decorates a function to make its output a Fluent instance"""

    def wrapper(*args, **kwargs) -> Fluent:
        return Fluent(func(*args, **kwargs))

    return wrapper
