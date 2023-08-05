#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for field.py
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# stdlib imports
import unittest
import warnings


from zope.component import eventtesting

from zope.interface.common import interfaces as cmn_interfaces
from zope.schema import Dict
from zope.schema.interfaces import InvalidURI
from zope.schema.interfaces import SchemaNotProvided
from zope.schema.interfaces import TooLong
from zope.schema.interfaces import TooShort
from zope.schema.interfaces import WrongType


from nti.schema.field import HTTPURL
from nti.schema.field import DecodingValidTextLine
from nti.schema.field import FieldValidationMixin
from nti.schema.field import Float
from nti.schema.field import IndexedIterable
from nti.schema.field import Int
from nti.schema.field import ListOrTuple
from nti.schema.field import ListOrTupleFromObject
from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import ObjectLen
from nti.schema.field import TupleFromObject
from nti.schema.field import UniqueIterable
from nti.schema.field import ValidDatetime
from nti.schema.field import ValidRegularExpression
from nti.schema.field import Variant
from nti.schema.field import ValidTextLine as TextLine
from nti.schema.interfaces import IBeforeDictAssignedEvent
from nti.schema.interfaces import IBeforeSequenceAssignedEvent
from nti.schema.interfaces import IVariant
# Import from the BWC location

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from nti.schema.testing import validated_by # pylint:disable=no-name-in-module
    from nti.schema.testing import verifiably_provides # pylint:disable=no-name-in-module
    from nti.schema.testing import not_validated_by # pylint:disable=no-name-in-module


from . import IUnicode
from . import SchemaLayer

from hamcrest import assert_that
from hamcrest import calling
from hamcrest import contains
from hamcrest import contains_string
from hamcrest import has_length
from hamcrest import has_property
from hamcrest import is_
from hamcrest import is_not
from hamcrest import none
from hamcrest import raises

__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#disable: accessing protected members, too many methods
#pylint: disable=W0212,R0904,blacklisted-name


class TestObjectLen(unittest.TestCase):


    def test_objectlen(self):
        # If we have the inheritance messed up, we will have problems
        # creating, or we will have problems validating one part or the other.

        olen = ObjectLen(IUnicode, max_length=5)  # default val for min_length

        olen.validate(u'a')
        olen.validate(u'')

        assert_that(calling(olen.validate).with_args(object()),
                    raises(SchemaNotProvided))

        assert_that(calling(olen.validate).with_args(u'abcdef'),
                    raises(TooLong))

    def test_objectlen_short(self):
        olen = ObjectLen(IUnicode, min_length=5)

        assert_that(calling(olen.validate).with_args(u'abc'),
                    raises(TooShort))

class TestHTTPUrl(unittest.TestCase):

    def test_http_url(self):

        http = HTTPURL(__name__='foo')

        assert_that(http.fromUnicode('www.google.com'),
                    is_('http://www.google.com'))

        assert_that(http.fromUnicode('https://www.yahoo.com'),
                    is_('https://www.yahoo.com'))

        with self.assertRaises(InvalidURI) as exc:
            http.fromUnicode('mailto:jason@nextthought.com')

        exception = exc.exception
        assert_that(exception, has_property('field', http))
        assert_that(exception, has_property('value', 'mailto:jason@nextthought.com'))
        assert_that(exception, has_property('message', 'The specified URL is not valid.'))

class TestVariant(unittest.TestCase):

    def test_variant(self):

        syntax_or_lookup = Variant((Object(cmn_interfaces.ISyntaxError),
                                    Object(cmn_interfaces.ILookupError),
                                    Object(IUnicode)))

        assert_that(syntax_or_lookup, verifiably_provides(IVariant))

        # validates
        assert_that(SyntaxError(), validated_by(syntax_or_lookup))
        assert_that(LookupError(), validated_by(syntax_or_lookup))

        # doesn't validate
        assert_that(b'foo', not_validated_by(syntax_or_lookup))

        assert_that(syntax_or_lookup.fromObject(u'foo'), is_(u'foo'))

        assert_that(calling(syntax_or_lookup.fromObject).with_args(object()),
                    raises(TypeError))

    def test_getDoc(self):
        syntax_or_lookup = Variant((Object(cmn_interfaces.ISyntaxError),
                                    Object(cmn_interfaces.ILookupError),
                                    Object(IUnicode)))

        doc = syntax_or_lookup.getDoc()
        assert_that(doc, contains_string('.. rubric:: Possible Values'))
        assert_that(doc, contains_string('.. rubric:: Option'))

    def test_complex_variant(self):

        dict_field = Dict(key_type=TextLine(), value_type=TextLine())
        string_field = Object(IUnicode)
        list_of_numbers_field = ListOrTuple(value_type=Number())

        variant = Variant((dict_field, string_field, list_of_numbers_field))
        variant.getDoc()  # cover
        # It takes all these things
        for d in {u'k': u'v'}, u'foo', [1, 2, 3]:
            assert_that(d, validated_by(variant))

        # It rejects these
        for d in {u'k': 1}, b'foo', [1, 2, u'b']:
            assert_that(d, not_validated_by(variant))

        # A name set now is reflected down the line
        variant.__name__ = 'baz'
        for f in variant.fields:
            assert_that(f, has_property('__name__', 'baz'))

        # and in clones
        clone = variant.bind(object())
        for f in clone.fields:
            assert_that(f, has_property('__name__', 'baz'))

        # which doesn't change the original
        clone.__name__ = 'biz'
        for f in clone.fields:
            assert_that(f, has_property('__name__', 'biz'))

        for f in variant.fields:
            assert_that(f, has_property('__name__', 'baz'))

        # new objects work too
        new = Variant(variant.fields, __name__='boo')
        for f in new.fields:
            assert_that(f, has_property('__name__', 'boo'))

    def test_variant_from_object(self):
        field = Variant((TupleFromObject(HTTPURL()),))

        res = field.fromObject(['http://example.com'])
        assert_that(res, is_(('http://example.com',)))

    def test_converts_but_not_valid(self):
        # If the schema accepts the input, but the validation refuses,
        # keep going.
        class WeirdField(Object):
            schema = IUnicode

            def validate(self, value):
                raise SchemaNotProvided().with_field_and_value(self, value)
        weird_field = WeirdField(IUnicode)
        accept_field = Number()

        field = Variant((weird_field, accept_field),
                        variant_raise_when_schema_provided=True)
        assert_that(field.fromObject("1.0"),
                    is_(1.0))

        assert_that(calling(field.validate).with_args(u'1.0'),
                    raises(SchemaNotProvided))

    def test_invalid_construct(self):
        assert_that(calling(Variant).with_args(()),
                    raises(WrongType))

class TestConfiguredVariant(unittest.TestCase):

    layer = SchemaLayer

    def test_nested_variants(self):
        # Use case: Chat messages are either a Dict, or a N
        # ote-like body, which itself is a list of variants

        dict_field = Dict(key_type=TextLine(), value_type=TextLine())

        string_field = Object(IUnicode)
        number_field = Number()
        list_of_strings_or_numbers = ListOrTuple(value_type=Variant((string_field, number_field)))

        assert_that([1, u'2'], validated_by(list_of_strings_or_numbers))
        assert_that({u'k': u'v'}, validated_by(dict_field))

        dict_or_list = Variant((dict_field, list_of_strings_or_numbers))

        assert_that([1, u'2'], validated_by(dict_or_list))
        assert_that({u'k': u'v'}, validated_by(dict_or_list))

        class X(object):
            pass

        x = X()
        dict_or_list.set(x, [1, u'2'])

        events = eventtesting.getEvents(IBeforeSequenceAssignedEvent)
        assert_that(events, has_length(1))
        assert_that(events, contains(has_property('object', [1, '2'])))

        eventtesting.clearEvents()

        dict_or_list.set(x, {u'k': u'v'})
        events = eventtesting.getEvents(IBeforeDictAssignedEvent)
        assert_that(events, has_length(1))
        assert_that(events, contains(has_property('object', {'k': 'v'})))

class TestUniqueIterable(unittest.TestCase):

    def test_min_length(self):
        field = UniqueIterable(__name__='foo')
        assert_that(field, has_property('min_length', none()))

        class Thing(object):
            foo = None
        thing = Thing()
        field.set(thing, ())

        assert_that(thing, has_property('foo', ()))

class TestTupleFromObject(unittest.TestCase):

    def test_set(self):
        field = TupleFromObject(__name__='foo')

        class Thing(object):
            foo = None

        thing = Thing()
        field.validate([1, 2])
        field.set(thing, [1, 2])
        assert_that(thing, has_property('foo', (1, 2)))

        # But arbitrary iterables not validated...
        assert_that(calling(field.validate).with_args('abc'),
                    raises(WrongType))

        # Although they can be set...
        field.set(thing, 'abc')

    def test_wrong_type_from_object(self):
        field = TupleFromObject()
        assert_that(calling(field.fromObject).with_args('abc'),
                    raises(WrongType))

    def test_valid_type_from_object_unicode(self):
        field = TupleFromObject(HTTPURL())
        res = field.fromObject(['http://example.com'])
        assert_that(res, is_(('http://example.com',)))

    def test_valid_type_from_object_object(self):
        # Nested layers of fromObject and fromUnicode
        field = TupleFromObject(Variant((HTTPURL(),)))
        res = field.fromObject(['http://example.com'])
        assert_that(res, is_(('http://example.com',)))

class TestListOrTupleFromObject(unittest.TestCase):

    def test_invalid_construct(self):
        assert_that(calling(ListOrTupleFromObject).with_args(Object(IUnicode)),
                    raises(WrongType))

class TestIndexedIterable(unittest.TestCase):

    def test_accepts_str(self):
        field = IndexedIterable(__name__='foo')
        class Thing(object):
            foo = None

        thing = Thing()
        field.set(thing, 'abc')
        assert_that(thing, has_property('foo', 'abc'))

class TestDecodingValidTextLine(unittest.TestCase):

    def test_decode(self):
        field = DecodingValidTextLine()
        res = field.validate(b'abc')
        assert_that(res, is_(u'abc'))

class TestNumber(unittest.TestCase):

    def test_allow_empty(self):
        assert_that(Float().fromUnicode(''), is_(none()))
        assert_that(Int().fromUnicode(''), is_(none()))

class TestDatetime(unittest.TestCase):

    def test_validate_wrong_type(self):
        field = ValidDatetime()
        assert_that(calling(field.validate).with_args(''),
                    raises(SchemaNotProvided))

class TestFieldValidationMixin(unittest.TestCase):

    def test_one_arg(self):
        field = FieldValidationMixin()
        field.__name__ = 'foo'

        ex = SchemaNotProvided('msg').with_field_and_value(field, 'value')
        # zope.schema 4.7 automatically fills in args
        assert_that(ex.args, is_(('msg', None)))
        assert_that(ex.schema, is_('msg'))
        ex.args = ('msg',)
        try:
            field._reraise_validation_error(ex, 'value', _raise=True)
        except SchemaNotProvided:
            assert_that(ex.args, is_(('value', 'msg', 'foo')))

    def test_no_arg(self):
        field = FieldValidationMixin()
        field.__name__ = 'foo'

        ex = SchemaNotProvided().with_field_and_value(field, 'value')
        # zope.schema 4.7 automatically fills in args
        assert_that(ex.args, is_((None, None)))
        ex.args = ()
        try:
            field._reraise_validation_error(ex, 'value', _raise=True)
        except SchemaNotProvided:
            assert_that(ex.args, is_(('value', '', 'foo')))

    def test_oob(self):
        from zope.schema import Integral
        from zope.schema.interfaces import OutOfBounds
        class Field(FieldValidationMixin, Integral):
            pass

        field = Field(min=1)
        with self.assertRaises(OutOfBounds):
            field.validate(0)

    def test_random_validation_error(self):
        from zope.schema.interfaces import ValidationError

        class Field(object):
            __name__ = ''
            def _validate(self, v):
                raise ValidationError().with_field_and_value(self, v)

        class Field2(FieldValidationMixin, Field):
            pass

        field = Field2()
        with self.assertRaises(ValidationError) as exc:
            field._validate(42)

        ex = exc.exception
        assert_that(ex.args, is_((42, '', '')))


class TestRegex(unittest.TestCase):

    def test_regex(self):
        field = ValidRegularExpression('[bankai|shikai]', flags=0)
        assert_that(field.constraint("bankai"), is_(True))
        assert_that(field.constraint("shikai"), is_(True))
        assert_that(field.constraint("Shikai"), is_(False))
        assert_that(field.constraint("foo"), is_(False))
        field = ValidRegularExpression('[bankai|shikai]')
        assert_that(field.constraint("Shikai"), is_(True))
        assert_that(field.constraint("banKAI"), is_(True))


class TestValueTypeAddingDocMixin(unittest.TestCase):

    def _getTargetClass(self):
        from nti.schema.field import _ValueTypeAddingDocMixin
        return _ValueTypeAddingDocMixin

    def test_getDoc(self):

        from zope.schema import Field

        class MyField(self._getTargetClass(), Field):
            _type = object
            accept_types = (list, tuple)

        doc = MyField().getDoc()

        assert_that(doc, contains_string(':Allowed Type: :class:`object`'))
        assert_that(doc, contains_string(':Accepted Types: :class:`list`, :class:`tuple`'))


class TestDictFromObject(unittest.TestCase):

    def _getTargetClass(self):
        from nti.schema.field import DictFromObject
        return DictFromObject

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_accepts_mapping(self):
        from six.moves import UserDict
        from nti.schema.field import abcs

        # On Python 2, UserDict is not registered as a Mapping.
        if not issubclass(UserDict, abcs.Mapping): # pragma: no cover
            abcs.Mapping.register(UserDict)

        field = self._makeOne(key_type=Int(), value_type=Float())

        value = UserDict({'1': '42'})
        assert_that(value, is_(abcs.Mapping))
        assert_that(value, is_not(dict))

        result = field.fromObject(value)
        assert_that(result, is_(dict))
        assert_that(result, is_({1: 42.0}))

    def test_getDoc(self):
        field = self._makeOne(key_type=Int(), value_type=Float())
        doc = field.getDoc()

        assert_that(doc, contains_string('.. rubric:: Value Type'))
        assert_that(doc, contains_string('.. rubric:: Key Type'))
