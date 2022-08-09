from marshmallow import fields, post_load, post_dump, Schema, ValidationError

from api.models.MonitorModel import MonitorModel
from api.models.Schemas.BaseSchema import ValidatedSchema


class PaginationSchema(ValidatedSchema):
    page = fields.Integer(missing=1)
    per_page = fields.Integer(missing=10, load_only=True)
    sort = fields.List(fields.String, load_only=True)

    items = fields.List(fields.Raw, dump_only=True)
    pages = fields.Integer(dump_only=True)
    total = fields.Integer(dump_only=True)

    @staticmethod
    def validate_sort_parameters(data, child_model):
        try:
            sort = data.get('sort', [])
            for parameter in sort:
                [key, value] = parameter.split(' ')
                if key not in child_model.fields.keys():
                    raise AssertionError()
                if value not in ['desc', 'asc']:
                    raise AssertionError()

        except (AttributeError, ValueError, ValidationError, AssertionError) as err:
            raise ValidationError('Invalid sort parameters.', 'sort')
