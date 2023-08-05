#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interfaces describing the events and fields this package uses.

Also utility functions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from zope.deprecation import deprecated

from zope.schema import Text
from zope.schema import TextLine
from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import providedBy
from zope.interface import implementer
from zope.schema import interfaces as sch_interfaces
try:
    from zope.schema._bootstrapfields import BeforeObjectAssignedEvent
except ImportError: # pragma: no cover
    # BWC for older zope.schema.
    from zope.schema._field import BeforeObjectAssignedEvent

__docformat__ = "restructuredtext en"

# pylint:disable=inherit-non-class,no-self-argument

class IBeforeSchemaFieldAssignedEvent(Interface):
    """
    An event sent when certain schema fields will be assigning an
    object to a property of another object.

    The interface
    :class:`zope.schema.interfaces.IBeforeObjectAssignedEvent` is a
    sub-interface of this one once this module is imported.
    """
    object = Attribute(u"The object that is going to be assigned. Subscribers may modify this")

    name = Attribute(u"The name of the attribute under which the object will be assigned.")

    context = Attribute(u"The context object where the object will be assigned to.")

# Make this a base of the zope interface so our handlers
# are compatible
sch_interfaces.IBeforeObjectAssignedEvent.__bases__ = (IBeforeSchemaFieldAssignedEvent,)

@implementer(IBeforeSchemaFieldAssignedEvent)
class BeforeSchemaFieldAssignedEvent(object):

    def __init__(self, obj, name, context):
        self.object = obj
        self.name = name
        self.context = context

class IBeforeTextAssignedEvent(IBeforeSchemaFieldAssignedEvent):
    """
    Event for assigning text.
    """

    object = Text(title=u"The text being assigned.")

class IBeforeTextLineAssignedEvent(IBeforeTextAssignedEvent):  # ITextLine extends IText
    """
    Event for assigning text lines.
    """

    object = TextLine(title=u"The text being assigned.")

class IBeforeContainerAssignedEvent(IBeforeSchemaFieldAssignedEvent):
    """
    Event for assigning containers (__contains__).
    """

class IBeforeIterableAssignedEvent(IBeforeContainerAssignedEvent):
    """
    Event for assigning iterables.
    """

class IBeforeCollectionAssignedEvent(IBeforeIterableAssignedEvent):
    """
    Event for assigning collections.
    """

    object = Attribute(u"The collection being assigned. May or may not be mutable.")

class IBeforeSetAssignedEvent(IBeforeCollectionAssignedEvent):
    """
    Event for assigning sets.
    """

class IBeforeSequenceAssignedEvent(IBeforeCollectionAssignedEvent):
    """
    Event for assigning sequences.
    """

    object = Attribute(u"The sequence being assigned. May or may not be mutable.")

class IBeforeDictAssignedEvent(IBeforeIterableAssignedEvent):
    """
    Event for assigning dicts.
    """

# The hierarchy is IContainer > IIterable > ICollection > ISequence > [ITuple, IList]
# Also:         IContainer > IIterable > IDict
# Also:         IContainer > IIterable > ISet

@implementer(IBeforeTextAssignedEvent)
class BeforeTextAssignedEvent(BeforeSchemaFieldAssignedEvent):
    pass

@implementer(IBeforeTextLineAssignedEvent)
class BeforeTextLineAssignedEvent(BeforeTextAssignedEvent):
    pass


@implementer(IBeforeCollectionAssignedEvent)
class BeforeCollectionAssignedEvent(BeforeSchemaFieldAssignedEvent):
    object = None

@implementer(IBeforeSequenceAssignedEvent)
class BeforeSequenceAssignedEvent(BeforeCollectionAssignedEvent):
    pass

@implementer(IBeforeSetAssignedEvent)
class BeforeSetAssignedEvent(BeforeCollectionAssignedEvent):
    pass

@implementer(IBeforeDictAssignedEvent)
class BeforeDictAssignedEvent(BeforeSchemaFieldAssignedEvent):
    pass

BeforeObjectAssignedEvent = BeforeObjectAssignedEvent

class InvalidValue(sch_interfaces.InvalidValue):
    """
    InvalidValue(*args, field=None, value=None)

    Adds a field specifically to carry the value that is invalid.

    .. deprecated:: 1.4.0
       This is now just a convenience wrapper around
       :class:`zope.schema.interfaces.InvalidValue` that calls
       :meth:`.zope.schema.interfaces.ValidationError.with_field_and_value`
       before returning the exception. You should always catch
       :class:`zope.schema.interfaces.InvalidValue`.
    """
    # We can't write the syntax we want to in Python 2.

    def __init__(self, *args, **kwargs):
        field = kwargs.pop('field', None)
        value = kwargs.pop('value', None)
        if kwargs:
            raise TypeError("Too many kwargs for function InvalidValue")
        super(InvalidValue, self).__init__(*args)
        self.with_field_and_value(field, value)

deprecated('InvalidValue',
           "Use zope.schema.interfaces.InvalidValue.with_field_and_value.")

assert hasattr(sch_interfaces.InvalidValue, 'value')
assert hasattr(sch_interfaces.ValidationError, 'field')


class IFromObject(Interface):
    """
    Something that can convert one type of object to another,
    following validation rules (see :class:`zope.schema.interfaces.IFromUnicode`)
    """

    def fromObject(obj):
        """
        Attempt to convert the object to the required type following
        the rules of this object.  Raises a TypeError or
        :class:`zope.schema.interfaces.ValidationError` if this isn't
        possible.
        """

class IVariant(sch_interfaces.IField, IFromObject):
    """
    Similar to :class:`zope.schema.interfaces.IObject`, but
    representing one of several different types.
    """

class IListOrTuple(sch_interfaces.IList):
    pass

def find_most_derived_interface(ext_self, iface_upper_bound, possibilities=None):
    """
    Search for the most derived version of the interface `iface_upper_bound`
    implemented by `ext_self` and return that. Always returns at least `iface_upper_bound`

    :keyword possibilities: An iterable of schemas to consider. If not given,
        all the interfaces provided by ``ext_self`` will be considered.
    """
    if possibilities is None:
        possibilities = providedBy(ext_self)
    _iface = iface_upper_bound
    for iface in possibilities:
        if iface.isOrExtends(_iface):
            _iface = iface
    return _iface

try:
    from dm.zope.schema.interfaces import ISchemaConfigured as _ISchemaConfigured
except ImportError:
    _ISchemaConfigured = Interface

class ISchemaConfigured(_ISchemaConfigured):
    """
    marker interface for ``SchemaConfigured`` classes.

    Used to facilitate the registration of forms and views.
    """
