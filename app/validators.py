from marshmallow import ValidationError


def validate_blank(name):
    def validate(data):
        if data is None or data == "":
            raise ValidationError(name + '_BLANK')

    return validate
