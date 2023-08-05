"""Main module."""
import collections
import json

from marshmallow import Schema, fields, validate
from marshmallowjson import ValidationError


DEFAULT_FIELDS = {
    'raw': fields.Raw,
    'dict': fields.Dict,
    'string': fields.String,
    'uuid': fields.UUID,
    'number': fields.Number,
    'integer': fields.Integer,
    'decimal': fields.Decimal,
    'boolean': fields.Boolean,
    'float': fields.Float,
    'datetime': fields.DateTime,
    'time': fields.Time,
    'date': fields.Date,
    'url': fields.Url,
    'email': fields.Email,
}

DEFAULT_VALIDATORS = {
    'containsonly': validate.ContainsOnly,
    'email': validate.Email,
    'length': validate.Length,
    'noneof': validate.NoneOf,
    'oneof': validate.OneOf,
    'range': validate.Range,
    'regexp': validate.Regexp,
    'url': validate.URL,
}


def fail_field(kind, field, name):
    """Fail field."""
    raise ValidationError(
        '{kind} is not a known kind in {name}.{field}'.format(
            kind=kind,
            field=field,
            name=name
        )
    )


class Definition:
    def __init__(self, types=None, fields=None):
        self.fields = fields or DEFAULT_FIELDS
        self.schemas = collections.OrderedDict()
        self.dict_schemas = collections.OrderedDict()
        if types is not None:
            self.import_types(types)

    def extend(self, name, definition):
        marshmallow_fields = {}
        marshmallow_fields_dict = {}
        for field, schema in definition.items():
            kind = schema.get('kind')
            required = schema.get('required', False)
            if kind == 'list':
                items = schema.get('items')
                if items in self.fields:
                    marshmallow_fields[field] = fields.List(
                        self.fields[items],
                        required=required,
                    )
                    marshmallow_fields_dict[field] = {
                        "type": kind,
                        "required": required
                    }
                else:
                    marshmallow_fields[field] = fields.Nested(
                        self.schemas[items],
                        required=required,
                    )
                    marshmallow_fields_dict[field] = {
                        "fields": self.dict_schemas[items],
                        "required": required
                    }
                continue
            if kind in self.fields:
                marshmallow_fields_dict[field] = {
                    "type": kind,
                    "required": required
                }
                validate = schema.get('validate')
                if kind in DEFAULT_FIELDS and validate:
                    validator_type = validate.get('type')
                    validator_params = dict(validate.get('params'))
                    # TODO: check if params effectively is correct params
                    # for the selected validator
                    validator = DEFAULT_VALIDATORS.get(validator_type)
                    if not validator:
                        # TODO: raise validator not found
                        pass
                    marshmallow_fields[field] = self.fields[kind](
                        required=required,
                        validate=validator(**validator_params)
                    )
                    marshmallow_fields_dict[field].update({
                        'validate': {
                            'type': validator_type,
                            'params': validator_params
                        }
                    })
                    continue
                elif validate:
                    # TODO: raise error -"field can not supports validation"
                    pass
                marshmallow_fields[field] = self.fields[kind](
                    required=required
                )
            else:
                marshmallow_fields[field] = fields.Nested(
                    self.schemas[kind],
                    required=required
                )
                marshmallow_fields_dict[field] = {
                    "fields": self.dict_schemas[kind],
                    "required": required
                }
        self.dict_schemas[name] = marshmallow_fields_dict
        self.schemas[name] = type(name, (Schema,), marshmallow_fields)

    def validate(self, types):
        """Validate a json definition schema."""
        known = set(self.fields.keys())
        for name, definition in types.items():
            for field, schema in definition.items():
                field_kind = schema.get('kind')
                if field_kind == 'list':
                    items = schema.get('items')
                    if not items:
                        raise(ValidationError(
                            'items is not found in {name}.{field}'.format(
                                name=name, field=field
                            )
                        ))
                    if items not in known:
                        fail_field(items, field, name)
                    continue
                if field_kind not in known:
                    fail_field(field_kind, field, name)
            known.add(name)
        return types

    def import_types(self, types):
        self.validate(types)
        for name, definition in types.items():
            self.extend(name, definition)

    @classmethod
    def from_file(cls, definition, fields=None):
        types = json.load(
            definition,
            object_pairs_hook=collections.OrderedDict
        )
        return cls(fields=fields, types=types)

    def to_full_nested(self):
        key = next(reversed(self.dict_schemas))
        return self.dict_schemas[key]

    def top(self):
        key = next(reversed(self.schemas))
        return self.schemas[key]()
