#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Schema fields.

These fields produce better validation errors than the standard
:mod:`zope.schema` fields do. All the standard fields are also aliased
to be imported from this module.

.. TODO: This module is big enough it should be factored into a package and sub-modules.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# stdlib imports
import numbers
import re
import sys

try:
    import collections.abc as abcs
except ImportError: # pragma: no cover
    # Python 2
    import collections as abcs

from six import reraise
from six import string_types
from zope import interface
from zope import schema
from zope.deferredimport import deprecatedFrom
from zope.event import notify
import zope.interface.common.idatetime

from zope.schema import Bool
from zope.schema import Choice
from zope.schema import Date
from zope.schema import Datetime
from zope.schema import Decimal
from zope.schema import Dict
from zope.schema import FrozenSet
from zope.schema import Iterable
from zope.schema import List
from zope.schema import Mapping
from zope.schema import MutableMapping
from zope.schema import MutableSequence
from zope.schema import Sequence
from zope.schema import Set
from zope.schema import Text
from zope.schema import TextLine
from zope.schema import Timedelta
from zope.schema import Tuple
from zope.schema import Object as _ObjectBase

from zope.schema import Complex
from zope.schema import Real
from zope.schema import Rational
from zope.schema import Integral

from zope.schema import interfaces as sch_interfaces

from nti.schema import MessageFactory as _
from nti.schema.interfaces import BeforeDictAssignedEvent
from nti.schema.interfaces import BeforeObjectAssignedEvent
from nti.schema.interfaces import BeforeSchemaFieldAssignedEvent
from nti.schema.interfaces import BeforeSequenceAssignedEvent
from nti.schema.interfaces import BeforeSetAssignedEvent
from nti.schema.interfaces import BeforeTextAssignedEvent
from nti.schema.interfaces import BeforeTextLineAssignedEvent
from nti.schema.interfaces import IFromObject
from nti.schema.interfaces import IListOrTuple
from nti.schema.interfaces import IVariant


__docformat__ = "restructuredtext en"

# Re-export some things as part of our public API so we can
# later re-implement them locally if needed
__all__ = [
    'Bool',
    'Choice',
    'Complex',
    'Date',
    'Datetime',
    'Decimal',
    'DecodingValidTextLine',
    'Dict',
    'DictFromObject',
    'FieldValidationMixin',
    'Float',
    'FrozenSet',
    'HTTPURL',
    'IndexedIterable',
    'Int',
    'Integral',
    'Iterable',
    'List',
    'ListOrTuple',
    'ListOrTupleFromObject',
    'Mapping',
    'MutableMapping',
    'MutableSequence',
    'Number',
    'Object',
    'ObjectLen',
    'Rational',
    'Real',
    'Set',
    'Sequence',
    'Text',
    'TextLine',
    'Timedelta',
    'Tuple',
    'TupleFromObject',
    'UniqueIterable',
    'ValidBytes',
    'ValidBytesLine',
    'ValidChoice',
    'ValidDatetime',
    'ValidRegEx',
    'ValidRegularExpression',
    'ValidSet',
    'ValidText',
    'ValidTextLine',
    'ValidURI',
    'Variant',
]

# BWC alias, not in __all__
DateTime = Datetime

deprecatedFrom(
    "Moved to nti.schema.schema",
    "nti.schema.schema",
    'SchemaConfigured',
)


def _do_set(self, context, value, cls, factory):
    try:
        event = factory(value, self.__name__, context)
        notify(event)
        value = event.object
        super(cls, self).set(context, value)
    except sch_interfaces.ValidationError as e: # pragma: no cover
        # This shouldn't happen, set() doesn't typically validate.
        self._reraise_validation_error(e, value) # pylint:disable=protected-access

def __make_set(cls, eventfactory):

    def set(self, context, value): # pylint:disable=redefined-builtin
        return _do_set(self, context, value, cls, eventfactory)

    cls.set = set

def __with_set(eventfactory=BeforeSchemaFieldAssignedEvent):
    def X(cls):
        __make_set(cls, eventfactory)
        return cls
    return X


class FieldValidationMixin(object):
    """
    A field mixin that causes slightly better errors to be created.
    """

    @property
    def __fixup_name__(self):
        """
        The :class:`zope.schema.fieldproperty.FieldPropertyStoredThroughField` class mangles
        the field name; this undoes that mangling.
        """
        if self.__name__ and self.__name__.startswith('__st_') and self.__name__.endswith('_st'):
            return self.__name__[5:-3]
        return self.__name__

    def _fixup_validation_error_args(self, e, value):
        # Called when the exception has one argument, which is usually, though not always,
        # the message
        e.args = (value, e.args[0], self.__fixup_name__)

    def _fixup_validation_error_no_args(self, e, value):
        # Called when there are no arguments
        e.args = (value, str(e), self.__fixup_name__)

    def _reraise_validation_error(self, e, value, _raise=False):
        # This must be called inside a try/except with an active exception.
        assert e.field is not None, "A _validate method failed to use ex.with_field_and_value()"

        if len(e.args) == 1:  # typically the message is the only thing
            self._fixup_validation_error_args(e, value)
        elif not e.args:  # Typically a SchemaNotProvided. Grr.
            self._fixup_validation_error_no_args(e, value)
        elif isinstance(e, sch_interfaces.TooShort) and len(e.args) == 2:
            # Note we're capitalizing the field in the message.
            e.i18n_message = _(
                u'${field} is too short. Please use at least ${minLength} characters.',
                mapping={'field': self.__fixup_name__.capitalize(),
                         'minLength': e.args[1]})
            e.args = (self.__fixup_name__.capitalize() + ' is too short.',
                      self.__fixup_name__,
                      value)
        elif isinstance(e, sch_interfaces.TooLong) and len(e.args) == 2:
            e.i18n_message = _(u'${field} is too long. ${max_size} character limit.',
                               mapping={'field': self.__fixup_name__.capitalize(),
                                        'max_size': e.args[1]})
            e.args = (self.__fixup_name__.capitalize() + ' is too long.',
                      self.__fixup_name__,
                      value)
        if _raise:
            raise e
        raise # pylint:disable=misplaced-bare-raise

    def _validate(self, value):
        try:
            super(FieldValidationMixin, self)._validate(value)
        except sch_interfaces.WrongContainedType:
            raise
        except sch_interfaces.ValidationError as e:
            self._reraise_validation_error(e, value)

@interface.implementer(sch_interfaces.IObject)
class ValidDatetime(FieldValidationMixin, Datetime):
    """
    Unlike the standard datetime, this will check that the
    given object is an instance of IDatetime, and raise
    the same error as object does.
    """

    schema = zope.interface.common.idatetime.IDateTime

    def _validate(self, value):
        try:
            super(ValidDatetime, self)._validate(value)
        except sch_interfaces.WrongType as e:
            raise sch_interfaces.SchemaNotProvided(
                value, e.__doc__,
                self.__fixup_name__, self.schema,
                list(interface.providedBy(value))).with_field_and_value(self, value)

        # schema has to be provided by value
        if not self.schema.providedBy(value):  # pragma: no cover
            raise sch_interfaces.SchemaNotProvided().with_field_and_value(self, value)

def _iteritems(o):
    meth = getattr(o, 'iteritems', None) or getattr(o, 'items')
    return meth()

class Object(FieldValidationMixin, _ObjectBase):
    """
    Improved ``zope.schema.Object``.
    """


@interface.implementer(IVariant)
class Variant(FieldValidationMixin, schema.Field):
    """
    Similar to :class:`zope.schema.Object`, but accepts one of many non-overlapping
    interfaces.
    """

    fields = ()

    def __init__(self, fields, variant_raise_when_schema_provided=False, **kwargs):
        """
        :param fields: A list or tuple of field instances.
        :keyword variant_raise_when_schema_provided: If ``True``, then
            if a value is provided to ``validate`` that implements
            the schema of a particular field, and that field raised
            a validation error, that error will be propagated instead
            of the error raised by the last field, and no additional fields
            will be asked to do validation.

        """
        if not fields or not all((sch_interfaces.IField.providedBy(x) for x in fields)):
            raise sch_interfaces.WrongType()

        # assign our children first so anything we copy to them as a result of the super
        # constructor (__name__) gets set
        self.fields = list(fields)
        for f in self.fields:
            f.__parent__ = self

        self._raise_when_provided = variant_raise_when_schema_provided
        super(Variant, self).__init__(**kwargs)

    def __get_name(self):
        return self.__dict__.get('__name__', '')

    def __set_name(self, name):
        self.__dict__['__name__'] = name
        for field in self.fields:
            field.__name__ = name
    __name__ = property(__get_name, __set_name)

    def getExtraDocLines(self):
        lines = super(Variant, self).getExtraDocLines()
        lines.append(".. rubric:: Possible Values")

        for field in self.fields:
            lines.append(".. rubric:: Option")
            lines.append(field.getDoc())

        return lines

    def bind(self, obj):
        # The fields member really does exist
        # pylint:disable=no-member
        clone = super(Variant, self).bind(obj)
        clone.fields = [x.bind(obj) for x in clone.fields]
        for f in clone.fields:
            f.__parent__ = clone
        return clone

    def _validate(self, value):
        super(Variant, self)._validate(value)
        for field in self.fields:
            try:
                field.validate(value)
                # one of them accepted, yay!
                return
            except sch_interfaces.ValidationError as e:
                if (self._raise_when_provided
                        and hasattr(field, 'schema')
                        and field.schema.providedBy(value)):
                    self._reraise_validation_error(e, value)
                if field is self.fields[-1]:
                    # The last chance raised an exception. Nothing worked,
                    # so bail.
                    self._reraise_validation_error(e, value)
        # We can never get here
        raise AssertionError("This code should never be reached.")

    def fromObject(self, obj):
        """
        Similar to `fromUnicode`, attempts to turn the given object into something
        acceptable and valid for this field. Raises a TypeError, ValueError, or
        schema ValidationError if this cannot be done. Adaptation is attempted in the order
        in which fields were given to the constructor. Some fields cannot be used to adapt.
        """

        exc_info = None

        for field in self.fields:
            try:
                # Three possible ways to convert: adapting the schema of an IObject,
                # using a nested field that is IFromObject, or an IFromUnicode if the object
                # is a string.

                converter = None
                # Most common to least common
                if sch_interfaces.IObject.providedBy(field):
                    converter = field.schema
                elif (sch_interfaces.IFromUnicode.providedBy(field)
                      and isinstance(obj, string_types)):
                    converter = field.fromUnicode
                elif IFromObject.providedBy(field):
                    converter = field.fromObject

                # Try to convert and validate
                adapted = converter(obj)
            except (TypeError, sch_interfaces.ValidationError):
                # Nope, no good
                exc_info = sys.exc_info()
            else:
                # We got one that like the type. Do the validation
                # now, and then return. Don't try to convert with others;
                # this is probably our best error
                try:
                    field.validate(adapted)
                    return adapted
                except sch_interfaces.SchemaNotProvided: # pragma: no cover
                    # Except in one case. Some schema provides adapt to something
                    # that they do not actually want (e.g.,
                    # ISanitizedHTMLContent can adapt as IPlainText
                    # when empty)
                    # so ignore that and keep trying
                    exc_info = sys.exc_info()

        # We get here if nothing worked and re-raise the last exception
        try:
            reraise(*exc_info)
        finally:
            del exc_info

    _EVENT_TYPES = (
        (string_types, BeforeTextAssignedEvent),
        (abcs.Mapping, BeforeDictAssignedEvent),
        (abcs.Sequence, BeforeSequenceAssignedEvent),
        (object, BeforeObjectAssignedEvent)
    )

    def set(self, context, value):
        # Try to determine the most appropriate event to fire
        # Order matters. It would kind of be nice to direct this to the appropriate
        # field itself, but that's sort of hard.
        for kind, factory in self._EVENT_TYPES:
            if isinstance(value, kind):
                _do_set(self, context, value, Variant, factory)
                return

class ObjectLen(FieldValidationMixin, schema.MinMaxLen, _ObjectBase):  # order matters
    """
    Allows specifying a length for arbitrary object fields (though the
    objects themselves must support the `len` function.
    """

    def __init__(self, sch, min_length=0, max_length=None, **kwargs):
        # match the calling sequence of Object, which uses a non-keyword
        # argument for schema.
        # But to work with the superclass, we have to pass it as a keyword arg.
        # it's weird.
        super(ObjectLen, self).__init__(schema=sch,
                                        min_length=min_length,
                                        max_length=max_length,
                                        **kwargs)

class Int(FieldValidationMixin, schema.Int):

    def fromUnicode(self, value):
        # Allow empty strings
        result = super(Int, self).fromUnicode(value) if value else None
        return result

class Float(FieldValidationMixin, schema.Float):

    def fromUnicode(self, value):
        result = super(Float, self).fromUnicode(value) if value else None
        return result

class Number(FieldValidationMixin, schema.Float):
    """
    A field that parses like a float from a string, but accepts any number.

    .. deprecated:: 1.4.0
       Use :class:`zope.schema.Number` if you really want arbitrary
       numbers (including fractions and decimals). You probably want
       :class:`zope.schema.Real` instead, though.
    """
    _type = numbers.Number

@__with_set()
class ValidChoice(FieldValidationMixin, schema.Choice):
    pass

@__with_set()
class ValidBytesLine(FieldValidationMixin, schema.BytesLine):
    pass

@__with_set()
class ValidBytes(FieldValidationMixin, schema.Bytes):
    pass

@__with_set(BeforeTextAssignedEvent)
class ValidText(FieldValidationMixin, schema.Text):
    """
    A text line that produces slightly better error messages. They will all
    have the 'field' property.

    We also fire :class:`IBeforeTextAssignedEvent`, which the normal
    mechanism does not.
    """

@__with_set(BeforeTextLineAssignedEvent)
class ValidTextLine(FieldValidationMixin, schema.TextLine):
    """
    A text line that produces slightly better error messages. They will all
    have the 'field' property.

    We also fire :class:`IBeforeTextLineAssignedEvent`, which the normal
    mechanism does not.
    """

class DecodingValidTextLine(ValidTextLine):
    """
    A text type that will attempt to decode non-unicode
    data as UTF-8.

    This primarily exists for legacy support (tests and persisted data).
    """

    def validate(self, value):
        if isinstance(value, bytes):
            value = value.decode('utf-8')  # let raise UnicodeDecodeError
        super(DecodingValidTextLine, self).validate(value)
        return value # tests

    # fromUnicode calls validate, so no need to duplicate

class ValidRegularExpression(ValidTextLine):

    def __init__(self, pattern, flags=(re.U|re.I|re.M), *args, **kwargs):
        super(ValidRegularExpression, self).__init__(*args, **kwargs)
        self.flags = flags
        self.pattern = pattern
        self.prog = re.compile(pattern, flags)

    def constraint(self, value): # pylint:disable=method-hidden
        # If they pass a 'constraint' kwarg, it will override this.
        return self.prog.match(value) is not None

ValidRegEx = ValidRegularExpression

class ValidURI(FieldValidationMixin, schema.URI):

    def _fixup_validation_error_args(self, e, value):
        if isinstance(e, sch_interfaces.InvalidURI):
            # This class differs by using the value as the argument, not
            # a message
            e.__doc__ = e.__doc__.replace('URI', 'URL')
            e.args = (value, e.__doc__, self.__fixup_name__)
            e.message = e.i18n_message = e.__doc__
        else: # pragma: no cover
            super(ValidURI, self)._fixup_validation_error_args(e, value)

class HTTPURL(ValidURI):
    """
    A URI field that ensures and requires its value to be an absolute
    HTTP/S URL.
    """

    def fromUnicode(self, value):
        # This can wind up producing something invalid if an
        # absolute URI was already given for mailto: for whatever.
        # None of the regexs (zopes or grubers) flag that as invalid.
        # so we try to
        orig_value = value
        if value:
            lower = value.lower()
            if not lower.startswith(u'http://') and not lower.startswith(u'https://'):
                # assume http
                value = u'http://' + value
        result = super(HTTPURL, self).fromUnicode(value)
        if result.count(u':') != 1:
            self._reraise_validation_error(
                sch_interfaces.InvalidURI(orig_value).with_field_and_value(self, orig_value),
                orig_value,
                _raise=True)

        return result

class _ValueTypeAddingDocMixin(object):
    """
    A mixin for fields that wrap a value type field (e.g., Object)
    to copy the nested documentation to the parent so it is visible
    in :mod:`repoze.sphinx.autointerface`.
    """

    def getExtraDocLines(self):
        lines = super(_ValueTypeAddingDocMixin, self).getExtraDocLines()
        accept_types = getattr(self, 'accept_types', None)
        if accept_types:
            # Private helper. If it goes away or changes, making sphinx docs will
            # fail, but we shouldn't have any runtime problems.
            from zope.schema._bootstrapfields import _DocStringHelpers
            lines.append(_DocStringHelpers.make_class_field('Accepted Types', accept_types))
        return lines


@__with_set(BeforeSequenceAssignedEvent)
class IndexedIterable(_ValueTypeAddingDocMixin, FieldValidationMixin, schema.Sequence):
    """
    An arbitrary (indexable) iterable, not necessarily a list or tuple;
    either of those would be acceptable at any time (however, so would a string,
    so be careful. Try ListOrTuple if that's a problem).

    The values may be homogeneous by setting the value_type.

    .. versionchanged:: 1.4.0
       Subclass :class:`zope.schema.Sequence` instead of :class:`zope.schema.List`,
       which adds checking that the value is indeed a sequence.
    """


@interface.implementer(IListOrTuple)
class ListOrTuple(IndexedIterable):
    "Restrict sequence values specifically to list and tuple."
    _type = (list, tuple)

class _SequenceFromObjectMixin(object):
    accept_types = None
    _default_type = list

    def _converter_for(self, field):
        if hasattr(field, 'fromObject'):
            converter = field.fromObject
        elif hasattr(field, 'fromUnicode'):  # here's hoping the values are strings
            converter = field.fromUnicode
        return converter

    def _do_fromObject(self, context):
        converter = self._converter_for(self.value_type)
        result = [converter(x) for x in context]
        return result

    def _do_convert_result(self, result):
        if (isinstance(self._type, type)
                and self._type is not self._default_type):  # single type is a factory
            result = self._type(result)
        return result

    def fromObject(self, context):
        check_type = self.accept_types or self._type
        if check_type is not None and not isinstance(context, check_type):
            raise sch_interfaces.WrongType(context, check_type).with_field_and_value(self, context)

        result = self._do_fromObject(context)
        return self._do_convert_result(result)


@interface.implementer(IFromObject)
class ListOrTupleFromObject(_SequenceFromObjectMixin, ListOrTuple):
    """
    The field_type MUST be a :class:`Variant`, or more generally,
    something supporting :class:`IFromObject` or :class:`IFromUnicode`
    """

    def __init__(self, *args, **kwargs):
        super(ListOrTupleFromObject, self).__init__(*args, **kwargs)
        if not IFromObject.providedBy(self.value_type):
            raise sch_interfaces.WrongType(self.value_type, IFromObject).with_field_and_value(
                self, self.value_type)

@interface.implementer(IFromObject)
class TupleFromObject(_ValueTypeAddingDocMixin,
                      _SequenceFromObjectMixin,
                      FieldValidationMixin,
                      schema.Tuple):
    """
    The field_type MUST be a :class:`Variant`, or more generally,
    something supporting :class:`IFromObject`. When setting through this object,
    we will automatically convert lists and only lists to tuples (for convenience coming
    in through JSON)
    """
    accept_types = (list, tuple)
    def set(self, context, value):
        if isinstance(value, list):
            value = tuple(value)

        _do_set(self, context, value, TupleFromObject, BeforeSequenceAssignedEvent)

    def validate(self, value):
        if isinstance(value, list):
            value = tuple(value)
        super(TupleFromObject, self).validate(value)

@interface.implementer(IFromObject)
@__with_set(BeforeDictAssignedEvent)
class DictFromObject(_ValueTypeAddingDocMixin,
                     _SequenceFromObjectMixin,
                     FieldValidationMixin,
                     schema.Mapping):
    """
    The `key_type` and `value_type` must be supporting
    :class:`IFromObject` or :class:`.IFromUnicode`.

    .. versionchanged:: 1.4.0
       Subclass :class:`zope.schema.Mapping` instead of :class:`zope.schema.Dict`,
       allowing for any mapping (such as BTrees), not just dicts. However, the validated
       value is still a dict.
    """

    def _do_convert_result(self, result):
        assert isinstance(result, dict)
        return result

    def _do_fromObject(self, context):
        key_converter = self._converter_for(self.key_type)
        value_converter = self._converter_for(self.value_type)
        return {key_converter(k): value_converter(v) for k, v in _iteritems(context)}

@__with_set(BeforeSetAssignedEvent)
class ValidSet(_ValueTypeAddingDocMixin, FieldValidationMixin, schema.Set):
    pass

class UniqueIterable(ValidSet):
    """
    An arbitrary iterable, not necessarily an actual :class:`set` object,
    but one whose contents are unique. Use this when you can
    return a :class:`set`, :class:`frozenset` or empty tuple. These should be
    sequences that suport the ``in`` operator.
    """
    _type = None  # Override to not force a set

    def __init__(self, *args, **kwargs):
        # If they do not specify a min_length in the arguments,
        # then change it to None. This way we are compatible with
        # a generator value. Superclass specifies both a class value
        # and a default argument
        no_min_length = False
        if 'min_length' not in kwargs:
            no_min_length = True

        super(UniqueIterable, self).__init__(*args, **kwargs)
        if no_min_length:
            self.min_length = None
