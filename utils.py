#! /usr/bin/env python3

# pylint: disable=missing-module-docstring,missing-function-docstring

import collections

class Object(dict):
    """
    Object extends the inbuilt dictionary and exposes the keys as class members.
    p = Object({"key1": 11, "key2": 22})
    key1 of p can be accessed by p.key1 as well as p["key1"].
    """

    def __init__(self, *initial_value, **kwargs):
        self.__dict__ = self
        dict.__init__(self, *initial_value, **kwargs)


class FrozenDict(collections.Mapping):
    """Immutable dictionary"""

    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        if self._hash is None:
            hash_ = 0
            for pair in self.iteritems():
                hash_ ^= hash(pair)
            self._hash = hash_
        return self._hash


class FrozenObject(collections.Mapping):
    """
    Immutable object. Usage: Similar to FrozenDict. Keys can be accessed like
    class members. eg:
    x = FrozenObject(a=11, b=12)
    assert x.a ==  11 and x['a'] == 11
    x.a = 11  ,  x['a'] == 11   ,   x['c'] = 11   fails
    """

    def __init__(self, *args, **kwargs):
        # self.__dict__ = self
        self.__dict__.update(*args, **kwargs)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, val):
        assert False


class OrderedSet(collections.MutableSet):
    """Implementation Credit: http://code.activestate.com/recipes/576694/"""

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next_ = self.map.pop(key)
            prev[2] = next_
            next_[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
