from dataclasses import dataclass


class DictValidator:
    def __init__(self, field_validators):
        self.field_validators = field_validators

    def validate(self, data):
        error_messages = {}

        for field, validator in self.field_validators.items():
            if field in data:
                validation_result = validator(data[field])
                if validation_result is not True:
                    error_messages[field] = validation_result

        if not error_messages:
            return True
        else:
            return False, error_messages


class DictValidatorFactory:
    def create_validator(self, field_validators):
        return DictValidator(field_validators)


class Correction:
    def __init__(self, correction_type, details):
        self.correction_type = correction_type
        self.details = details

    def to_dict(self):
        return {
            "type": self.correction_type,
            "details": self.details
        }


@dataclass
class Error:
    type: str
    correction: Correction
    message: str

    def __int__(self, given_type: str, given_message: str, given_correction: Correction):
        self.type = given_type
        self.correction = given_correction
        self.message = given_message

    def to_dict(self):
        return {
            "type": self.type,
            "error_message": self.message,
            "correction": self.correction.to_dict()
        }
