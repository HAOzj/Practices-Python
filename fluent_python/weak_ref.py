# -*- coding:utf-8 -*-
import weakref


class Name(str):
    __slots__ = ('__weakref__',)


class Cheese:
    def __init__(self, kind):
        self.kind = kind


a = weakref.WeakKeyDictionary()
b = weakref.WeakValueDictionary()
c = weakref.WeakSet()
catalog = [Cheese('brie'), Cheese('parmesan'), Cheese('cheddar')]
for peso in catalog:
    a[Name(peso.kind)] = peso
    b[peso.kind] = peso
    c.add(peso)

del catalog
print(list(a.keys()))
print(list(b.keys()))
print(list(c))
