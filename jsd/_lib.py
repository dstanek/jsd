# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import six
import os


class _ObjectMeta(type):

    def __new__(meta, name, bases, dct):
        dct.update({
            'properties': {},
            'required_properties': [],
            'required': False,
        })

        for _name, obj in list(dct.items()):
            if isinstance(obj, _Type):
                del dct[_name]
                dct['properties'][_name] = obj
                if obj.required:
                    dct['required_properties'].append(_name)

        return super(_ObjectMeta, meta).__new__(meta, name, bases, dct)


class _Type(object):

    def __init__(self, required=False, **kwargs):
        self.required = required

    def json(self):
        if self.required:
            return {'type': self.type}
        else:
            return {'type': [self.type, 'null']}


@six.add_metaclass(_ObjectMeta)
class Object(_Type):
    additional_properties = False

    def json(self):
        d = {
            'properties': dict((name, obj.json())
                               for name, obj in self.properties.items()),
        }
        if self.required:
            d['type'] = 'object'
        else:
            d['type'] = ['object', 'null']
        if self.required_properties:
            d['required'] = self.required_properties
        return d


class String(_Type):
    type = 'string'
    what = 'yep'


class Array(_Type):
    type = 'array'

    def __init__(self, item_type=None, required=False, min_items=0):
        self.item_type = item_type
        self.required = required
        self.min_items = min_items

    def json(self):
        data = super(Array, self).json()
        data['minItems'] = self.min_items
        if self.item_type:
            data['items'] = create_if_needed(self.item_type).json()
        return data


class Boolean(_Type):
    type = 'boolean'


class OneOf(_Type):
    def __init__(self, *types, **kwargs):
        self.required = kwargs.pop('required', False)
        self.types = [create_if_needed(t) for t in types]

    def json(self):
        return {'oneOf': [t.json() for t in self.types]}
        # FIXME: does type: object also need to be returned?


def create_if_needed(cls_or_obj):
    return cls_or_obj() if isinstance(cls_or_obj, type) else cls_or_obj

class Sweet(object):
    pass
