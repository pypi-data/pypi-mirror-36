# pylint: skip-file

import types
import inspect
import operator
import time

"""
Copied from Json Pickle: https://github.com/jsonpickle/jsonpickle/blob/master/jsonpickle/util.py
"""

SEQUENCES = (list, set, tuple)
SEQUENCES_SET = set(SEQUENCES)
PRIMITIVES = set((str, bool, float, int, int))


def is_type(obj):
    # use "isinstance" and not "is" to allow for metaclasses
    return isinstance(obj, type)


def has_method(obj, name):
    # false if attribute doesn't exist
    if not hasattr(obj, name):
        return False
    func = getattr(obj, name)

    # builtin descriptors like __getnewargs__
    if isinstance(func, types.BuiltinMethodType):
        return True

    # note that FunctionType has a different meaning in py2/py3
    if not isinstance(func, (types.MethodType, types.FunctionType)):
        return False

    # need to go through __dict__'s since in py3 methods are essentially descriptors
    base_type = obj if is_type(obj) else obj.__class__  # __class__ for old-style classes
    original = None
    for subtype in inspect.getmro(base_type):  # there is no .mro() for old-style classes
        original = vars(subtype).get(name)
        if original is not None:
            break

    # name not found in the mro
    if original is None:
        return False

    # static methods are always fine
    if isinstance(original, staticmethod):
        return True

    # at this point, the method has to be an instancemthod or a classmethod
    self_attr = '__self__'
    if not hasattr(func, self_attr):
        return False
    bound_to = getattr(func, self_attr)

    # class methods
    if isinstance(original, classmethod):
        return issubclass(base_type, bound_to)

    # bound methods
    return isinstance(obj, type(bound_to))


def is_object(obj):
    """Returns True is obj is a reference to an object instance.
    >>> is_object(1)
    True
    >>> is_object(object())
    True
    >>> is_object(lambda x: 1)
    False
    """
    return (isinstance(obj, object) and
            not isinstance(obj, (type, types.FunctionType)))


def is_primitive(obj):
    """Helper method to see if the object is a basic data type. Unicode strings,
    integers, longs, floats, booleans, and None are considered primitive
    and will return True when passed into *is_primitive()*
    >>> is_primitive(3)
    True
    >>> is_primitive([4,4])
    False
    """
    if obj is None:
        return True
    elif type(obj) in PRIMITIVES:
        return True
    return False


def is_dictionary(obj):
    """Helper method for testing if the object is a dictionary.
    >>> is_dictionary({'key':'value'})
    True
    """
    return type(obj) is dict


def is_sequence(obj):
    """Helper method to see if the object is a sequence (list, set, or tuple).
    >>> is_sequence([4])
    True
    """
    return type(obj) in SEQUENCES_SET


def is_list(obj):
    """Helper method to see if the object is a Python list.
    >>> is_list([4])
    True
    """
    return type(obj) is list


def is_set(obj):
    """Helper method to see if the object is a Python set.
    >>> is_set(set())
    True
    """
    return type(obj) is set


def is_bytes(obj):
    """Helper method to see if the object is a bytestring.
    >>> is_bytes(b'foo')
    True
    """
    return type(obj) is bytes


def is_unicode(obj):
    """Helper method to see if the object is a unicode string"""
    return type(obj) is str


def is_tuple(obj):
    """Helper method to see if the object is a Python tuple.
    >>> is_tuple((1,))
    True
    """
    return type(obj) is tuple


def is_dictionary_subclass(obj):
    """Returns True if *obj* is a subclass of the dict type. *obj* must be
    a subclass and not the actual builtin dict.
    >>> class Temp(dict): pass
    >>> is_dictionary_subclass(Temp())
    True
    """
    return (hasattr(obj, '__class__') and
            issubclass(obj.__class__, dict) and not is_dictionary(obj))


def is_sequence_subclass(obj):
    """Returns True if *obj* is a subclass of list, set or tuple.
    *obj* must be a subclass and not the actual builtin, such
    as list, set, tuple, etc..
    >>> class Temp(list): pass
    >>> is_sequence_subclass(Temp())
    True
    """
    return (hasattr(obj, '__class__') and
            (issubclass(obj.__class__, SEQUENCES) or
                is_list_like(obj)) and
            not is_sequence(obj))


def is_list_like(obj):
    return hasattr(obj, '__getitem__') and hasattr(obj, 'append')


def is_noncomplex(obj):
    """Returns True if *obj* is a special (weird) class, that is more complex
    than primitive data types, but is not a full object. Including:
        * :class:`~time.struct_time`
    """
    if type(obj) is time.struct_time:
        return True
    return False


def is_function(obj):
    """Returns true if passed a function
    >>> is_function(lambda x: 1)
    True
    >>> is_function(locals)
    True
    >>> def method(): pass
    >>> is_function(method)
    True
    >>> is_function(1)
    False
    """
    if type(obj) in (types.FunctionType,
                     types.MethodType,
                     types.LambdaType,
                     types.BuiltinFunctionType,
                     types.BuiltinMethodType):
        return True
    if not hasattr(obj, '__class__'):
        return False
    module = translate_module_name(obj.__class__.__module__)
    name = obj.__class__.__name__
    return (module == '__builtin__' and
            name in ('function',
                     'builtin_function_or_method',
                     'instancemethod',
                     'method-wrapper'))


def is_module_function(obj):
    """Return True if `obj` is a module-global function
    >>> import os
    >>> is_module_function(os.path.exists)
    True
    >>> is_module_function(lambda: None)
    False
    """

    return (hasattr(obj, '__class__') and
            isinstance(obj, types.FunctionType) and
            hasattr(obj, '__module__') and
            hasattr(obj, '__name__') and
            obj.__name__ != '<lambda>')


def is_module(obj):
    """Returns True if passed a module
    >>> import os
    >>> is_module(os)
    True
    """
    return isinstance(obj, types.ModuleType)


def translate_module_name(module):
    """Rename builtin modules to a consistent (Python2) module name
    This is used so that references to Python's `builtins` module can
    be loaded in both Python 2 and 3.  We remap to the "__builtin__"
    name and unmap it when importing.
    See untranslate_module_name() for the reverse operation.
    """
    if module == 'builtins' or module == 'exceptions':
        # We map the Python2 `exceptions` module to `__builtin__` because
        # `__builtin__` is a superset and contains everything that is
        # available in `exceptions`, which makes the translation simpler.
        return '__builtin__'
    else:
        return module


def untranslate_module_name(module):
    """Rename module names mention in JSON to names that we can import
    This reverses the translation applied by translate_module_name() to
    a module name available to the current version of Python.
    """
    # remap `__builtin__` and `exceptions` to the `builtins` module
    if module == '__builtin__':
        module = 'builtins'
    elif module == 'exceptions':
        module = 'builtins'
    return module


def importable_name(cls):
    """
    >>> class Example(object):
    ...     pass
    >>> ex = Example()
    >>> importable_name(ex.__class__) == 'jsonpickle.util.Example'
    True
    >>> importable_name(type(25)) == '__builtin__.int'
    True
    >>> importable_name(None.__class__) == '__builtin__.NoneType'
    True
    >>> importable_name(False.__class__) == '__builtin__.bool'
    True
    >>> importable_name(AttributeError) == '__builtin__.AttributeError'
    True
    """
    name = cls.__name__
    module = translate_module_name(cls.__module__)
    return '%s.%s' % (module, name)


def itemgetter(obj, getter=operator.itemgetter(0)):
    return str(getter(obj))
