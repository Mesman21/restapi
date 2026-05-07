from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    description = fields.Str()
    status = fields.Str(validate=validate.OneOf(["наявні в бібліотеці", "видані комусь"]))
    year = fields.Int(required=True)