import unittest
import jsonschema
import jsd


class TestTypes(object):
    expected_schema = None
    valid_input = ()
    invalid_input = ()

    def assert_jsonshema_works(self, value, schema):
        jsonschema.validate(value, schema)

    def test_expected_schema(self):
        self.assertEqual(self._normalize_schema(self.expected_schema),
                         self._normalize_schema(self.schema))

    def test_valid_input(self):
        for input in self.valid_input:
            self.assert_jsonshema_works(input, self.schema)

    def test_invalid_input(self):
        for input in self.invalid_input:
            self.assertRaises(jsonschema.ValidationError,
                              self.assert_jsonshema_works,
                              input,
                              self.schema)

    def _normalize_schema(self, schema):
        """Recursively sort all lists in a schema.

        Since many of the data structures used in jsd are dictionaries we
        can't rely on the lists to be in order.

        """
        for key in list(schema.keys()):
            if isinstance(schema[key], list):
                schema[key].sort(key=str)
            elif isinstance(schema[key], dict):
                self._normalize_schema(schema[key])


class TestStringType(TestTypes, unittest.TestCase):
    schema = jsd.String().json()
    expected_schema = {'type': ['string', 'null']}

    valid_input = ['a string', None]
    invalid_input = [0, .1, [], {}]


class TestStringTypeRequired(TestTypes, unittest.TestCase):
    schema = jsd.String(required=True).json()
    expected_schema = {'type': 'string'}

    valid_input = ['a string']
    invalid_input = [None]


class TestArrayType(TestTypes, unittest.TestCase):
    schema = (jsd.Array(min_items=0, item_type=jsd.String(required=True))
              .json())
    expected_schema = {
        'type': ['array', 'null'],
        'minItems': 0,
        'items': {'type': 'string'},
    }

    valid_input = (
        [],
        ['a string'],
    )
    invalid_input = (
        [0],
        ['a string', 0],
        [None],
    )


class TestArrayTypeWithMinItems(TestTypes, unittest.TestCase):
    schema = (jsd.Array(min_items=5).json())
    expected_schema = {
        'type': ['array', 'null'],
        'minItems': 5,
    }

    valid_input = (
        [0, 1, 2, 3, 4],
    )
    invalid_input = (
        [],
        [0],
    )


class TestObjectType(TestTypes, unittest.TestCase):
    class Stuff(jsd.Object):
        name = jsd.String(required=True)
        email = jsd.String()
        groups = jsd.Array(min_items=1, item_type=jsd.String(required=True))

    schema = Stuff(required=True).json()
    expected_schema = {
        'type': 'object',
        'required': ['name'],
        'properties': {
            'name': {'type': 'string'},
            'email': {'type': ['string', 'null']},
            'groups': {
                'type': ['array', 'null'],
                'minItems': 1,
                'items': {'type': 'string'},
            },
        },
    }

    valid_input = (
        {
            'name': 'my name',
            'email': 'my email',
            'groups': None,
        },
        {
            'name': 'my name',
            'email': None,
            'groups': ['group0'],
        },
    )

    invalid_input = (
        {
            'name': None,  # fail!
            'email': 'my email',
            'groups': None,
        },
        {
            'name': 'my name',
            'email': None,
            'groups': [],  # fail!
        },
        {
            # fail! no name
            'email': None,
            'groups': None,
        },
    )


class TestRequiredObjectType(TestTypes, unittest.TestCase):

    @property
    def schema(self):
        class Inner(jsd.Object):
            s = jsd.String(required=True)

        class Outer(jsd.Object):
            inner = Inner(required=True)

        return Outer().json()

    expected_schema = {
        'type': 'object',
        'required': ['inner'],
        'properties': {
            'inner': {
                'type': 'object',
                'required': ['s'],
                'properties': {
                    's': {'type': 'string'},
                },
            },
        },
    }

    invalid_input = (
        {'inner': {}},
        {'inner': {'s': None}},
    )


class Email(jsd.Object):
    service = jsd.String()
    value = jsd.String()


class NestedStuff(jsd.Object):
    name = jsd.String(required=True)
    email = Email()
    groups = jsd.Array(item_type=jsd.String(), required=True)


class TestNestedObjectTypes(TestTypes, unittest.TestCase):
    schema = NestedStuff(required=True).json()
    expected_schema = {
        'type': 'object',
        'required': ['name', 'groups'],
        'properties': {
            'name': {'type': 'string'},
            'email': {
                'type': ['object', 'null'],
                'properties': {
                    'service': {'type': ['string', 'null']},
                    'value': {'type': ['string', 'null']},
                },
            },
            'groups': {
                'type': 'array',
                'minItems': 0,
                'items': {'type': ['string', 'null']},
            },
        },
    }

    valid_input = (
        {
            'name': 'my name',
            'email': {'value': 'my email'},
            'groups': ['asdf'],
        },
        {
            'name': 'my name',
            'email': None,
            'groups': ['group0'],
        },
    )

    invalid_input = (
        {
            'name': 'my name',
            'email': 'an email',  # fail!
            'groups': [],
        },
        {
            'name': 'my name',
            'email': {'value': 'my email'},
            # fail! no group
        },
        {
            'name': 'my name',
            'email': {'value': 'my email'},
            'group': [0, 1],  # fail!
        },
        None,
        {},
    )


class TestBooleanType(TestTypes, unittest.TestCase):
    schema = jsd.Boolean().json()
    expected_schema = {'type': ['boolean', 'null']}

    valid_input = [True, False, None]
    invalid_input = ['s', 1]


class TestBooleanTypeRequired(TestTypes, unittest.TestCase):
    schema = jsd.Boolean(required=True).json()
    expected_schema = {'type': 'boolean'}

    valid_input = [True, False]
    invalid_input = ['s', 1, None]


class TestOneOf(TestTypes, unittest.TestCase):
    class Example(jsd.Object):
        thing = jsd.OneOf(jsd.String(required=True),
                          jsd.Boolean(required=True))

    schema = Example(require=True).json()
    expected_schema = {
        'type': ['object', 'null'],
        'properties': {
            'thing': {
                'oneOf': [
                    {'type': 'string'},
                    {'type': 'boolean'},
                ],
            },
        },
    }

    valid_input = (
        {'thing': 'string'},
        {'thing': False},
        {},
    )
    invalid_input = (
        {'thing': 1},
        {'thing': None},
    )


class TestOneOfRequired(TestTypes, unittest.TestCase):
    class Example(jsd.Object):
        thing = jsd.OneOf(jsd.String(required=True),
                          jsd.Boolean(required=True),
                          required=True)

    schema = Example(require=True).json()
    expected_schema = {
        'type': ['object', 'null'],
        'required': ['thing'],
        'properties': {
            'thing': {
                'oneOf': [
                    {'type': 'string'},
                    {'type': 'boolean'},
                ],
            },
        },
    }

    valid_input = (
        {'thing': False},
    )
    invalid_input = (
        {'thing': 1},
        {},
    )


class TestOneOfWithNotRequiredTypes(TestTypes, unittest.TestCase):
    class Example(jsd.Object):
        thing = jsd.OneOf(jsd.String(),
                          jsd.Boolean(required=True))

    schema = Example(require=True).json()
    expected_schema = {
        'type': ['object', 'null'],
        'properties': {
            'thing': {
                'oneOf': [
                    {'type': ['string', 'null']},
                    {'type': 'boolean'},
                ],
            },
        },
    }

    valid_input = (
        {'thing': 'string'},
        {'thing': False},
        {'thing': None},
        {},
    )
    invalid_input = (
        {'thing': 1},
    )

def punt():
    pass
