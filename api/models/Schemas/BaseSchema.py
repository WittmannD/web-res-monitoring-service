from marshmallow import Schema, fields
from webargs.flaskparser import use_args, use_kwargs


class ValidatedSchema(Schema):
    __abstract__ = True

    @classmethod
    def validate_fields(cls, args_type=None, schema_kwargs=None, **kwargs):
        schema_kwargs = schema_kwargs or {}

        def factory(request):
            field = request.args.get('fields', None)
            only = field.split(',') if field else None
            partial = request.method == 'PATCH'

            return cls(
                only=only,
                partial=partial,
                context={'request': request},
                **schema_kwargs
            )

        if args_type == 'use_kwargs':
            return use_kwargs(factory, **kwargs)

        return use_args(factory, **kwargs)


class BaseSchema(ValidatedSchema):
    __abstract__ = True

    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
