"""Extended abstract base class functions"""
from __future__ import absolute_import
from builtins import object
import abc
import sys

# From http://stackoverflow.com/questions/11217878/python-2-7-combine-abc-abstractmethod-and-classmethod


if sys.version[0] == '2':
    class instancemethodwrapper(object):
        def __init__(self, callable):
            self.callable = callable
            self.__dontcall__ = False

        def __getattr__(self, key):
            return getattr(self.callable, key)

        def __call__(self, *args, **kwargs):
            if self.__dontcall__:
                raise TypeError('Attempted to call abstract method.')
            return self.callable(*args, **kwargs)
    class newclassmethod(classmethod):
        def __init__(self, func):
            super(newclassmethod, self).__init__(func)
            isabstractmethod = getattr(func, '__isabstractmethod__', False)
            if isabstractmethod:
                self.__isabstractmethod__ = isabstractmethod

        def __get__(self, instance, owner):
            result = instancemethodwrapper(
                super(newclassmethod, self).__get__(instance, owner))
            isabstractmethod = getattr(self, '__isabstractmethod__', False)
            if isabstractmethod:
                result.__isabstractmethod__ = isabstractmethod
                abstractmethods = getattr(owner, '__abstractmethods__', None)
                if abstractmethods and result.__name__ in abstractmethods:
                    result.__dontcall__ = True
            return result


    class abstractclassmethod(newclassmethod):
        def __init__(self, func):
            func = abc.abstractmethod(func)
            super(abstractclassmethod, self).__init__(func)
else:
    from abc import abstractclassmethod


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
