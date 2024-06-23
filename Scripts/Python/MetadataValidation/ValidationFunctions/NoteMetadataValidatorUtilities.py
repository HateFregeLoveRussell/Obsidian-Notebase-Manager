from json import loads
from ..NoteMetaDataValidatorClasses import DictValidatorFactory
from ..ValidationFunctions.AtomicValidationUtilities import (validate_url, validate_expected_value,
                                                             validate_through_list, basic_type_check,
                                                             validate_ISBN, validate_datetime, validate_alias_field,
                                                             validate_list_of_type)


def validate_status_field(value):
    if value is None:
        return ["Field is Empty"]
    if 'template' not in value:
        return ['No Template Field Found']
    template = value['template']
    match (template['name'], template['version']):
        case ('status-obj', 1):
            return True if value['state'] in ['In Progress', 'Completed', 'Stub'] else ["State Value must be either "
                                                                                        "'In Progress', 'Completed', or"
                                                                                        " 'Stub'"]
        case _:
            return ["Status Template Name not recognized by validator"]


def validate_validity_field(value):
    if value is None:
        return ["Field is Empty"]
    if 'template' not in value:
        return ['No Template Field Found']
    template = value['template']
    match (template['name'], template['version']):
        case ('validity-obj', 1):
            return True if type(value['state']) is bool else ["Validity Value must be of Type Bool"]
        case _:
            return ["Validate Template Name not recognized by validator"]


def validate_relationship_field(value):
    if value is None:
        return ["Field is Empty"]
    if 'name' not in value:
        return ['No Template Field Found']
    match (value['name'], value['version']):
        case ('standard-relationship-obj', 1):
            return True
        case ('deliverable-relationship-obj', 1):
            return True
        case _:
            return ["Validate Template Name not recognized by validator"]


def validate_deliverable_field(value):
    if value is None:
        return ["Field is Empty"]
    if 'template' not in value:
        return ['No Template Field Found']
    template = value['template']
    validator = DictValidatorFactory()
    match (template['name'], template['version']):
        case ('deliverable-obj', 1):
            validator = validator.create_validator({
                'type': lambda value: validate_through_list(value,
                                                            ["HW", "Assignment", "Project", "Lab", "Quiz", "Exam"]),
                'grading': lambda value: validate_through_list(value, ["standard", "non-standard"]),
                'weight': lambda value: basic_type_check(value, float),
                'due': lambda value: validate_datetime(value),
                'alias': lambda value: validate_alias_field(value)})
        case ('aggregate-deliverable-obj', 1):
            validator = validator.create_validator({
                'type': lambda value: validate_through_list(value,
                                                            ["HW", "Assignment", "Project", "Lab", "Quiz", "Exam"]),
                'total-grade': lambda value: basic_type_check(value, float),
                'due': lambda value: validate_datetime(value)})
        case _:
            return ["Status Template Name not recognized by validator"]

    result = validator.validate(value)
    return True if isinstance(result, bool) else result[1]


def validate_source_field(value):
    return_messages = []
    if isinstance(value, list) and value != ["<%tp.file.cursor()%>"]:
        for source in value:
            source = source.replace("'", "\"")
            source = loads(source)
            result = validate_single_source_field(source)
            return_messages.append(result)
        if all(entry == True for entry in return_messages):
            return_messages = True
    else:
        return_messages = validate_single_source_field(value)
    return return_messages


def validate_single_source_field(value):
    if value is None or (value == ["<%tp.file.cursor()%>"]):
        return ["Field is Empty"]
    if 'template' not in value:
        return ['No Template Field Found']

    template = value['template']

    validator = DictValidatorFactory()
    match (template['name'], template['version']):
        case ('source-video-obj', 1):
            validator = validator.create_validator({
                'type': lambda value: validate_expected_value(value, ['video']),
                'date-viewed': lambda value: validate_datetime(value),
                'title': lambda value: basic_type_check(value, str),
                'source-alias': lambda value: validate_alias_field(value)})
        case ('source-class-video-obj', 1):
            validator = validator.create_validator({
                'type': lambda value: validate_expected_value(value, ['video']),
                'date-viewed': lambda value: validate_datetime(value),
                'title': lambda value: basic_type_check(value, str),
                'source-alias': lambda value: validate_alias_field(value),
                'class-alias': lambda value: validate_alias_field(value)})
        case ('source-tbsection-obj', 1):
            validator = validator.create_validator({
                'type': lambda value: validate_expected_value(value, ['tbsection']),
                'date': lambda value: validate_datetime(value),
                'number': lambda value: basic_type_check(value, int),
                'source-alias': lambda value: validate_alias_field(value),
                'class-alias': lambda value: validate_alias_field(value)})
        case ('source-lecture-obj', 1):
            validator = validator.create_validator({
                'type': lambda value: validate_expected_value(value, ['lecture']),
                'date': lambda value: validate_datetime(value),
                'number': lambda value: basic_type_check(value, int),
                'source-alias': lambda value: validate_alias_field(value),
                'class-alias': lambda value: validate_alias_field(value)})
        case ('source-non-standard-pyhelp', 1):
            validator = validator.create_validator({
                'type': lambda value: validate_expected_value(value, ['non-standard-pyhelp']),
                'date': lambda value: validate_datetime(value),
                'python-version': lambda value: basic_type_check(value, str),
                'source-alias': lambda value: validate_alias_field(value)})
        case ('source-webarticle-obj', 1):
            validator = validator.create_validator({
                'type': lambda value: validate_expected_value(value, ['web-article']),
                'date-viewed': lambda value: validate_datetime(value),
                'title': lambda value: basic_type_check(value, str),
                'url': lambda value: validate_url(value),
                'source-alias': lambda value: validate_alias_field(value)})
        case _:
            return [f"Template Name not recognized by Source Object got {template['name']}"]

    result = validator.validate(value)
    return True if isinstance(result, bool) else result[1]


def validate_class_field(value):
    if 'template' not in value:
        return ['No Template Field Found']
    template = value['template']
    validator = DictValidatorFactory()
    match (template['name'], template['version']):
        case ('class-obj', 1):
            validator = validator.create_validator({
                'class-name': lambda value: basic_type_check(value, str),
                'author': lambda value: basic_type_check(value, str),
                'medium': lambda value: basic_type_check(value, str),
                'class-alias': lambda value: validate_alias_field(value)
            })
        case ('class-textbook-obj', 1):
            validator = validator.create_validator({
                'class-name': lambda value: basic_type_check(value, str),
                'author': lambda value: validate_list_of_type(value, str),
                'medium': lambda value: validate_expected_value(value, "Textbook"),
                'class-alias': lambda value: validate_alias_field(value),
                'title': lambda value: basic_type_check(value, str),
                'edition': lambda value: basic_type_check(value, str),
                'publisher': lambda value: basic_type_check(value, str),
                'ISBN': lambda value: validate_ISBN(value),
                'length': lambda value: basic_type_check(value, int)
            })
        case ('class-uni-obj', 1):
            validator = validator.create_validator({
                'class-name': lambda value: basic_type_check(value, str),
                'instructor': lambda value: basic_type_check(value, str),
                'medium': lambda value: basic_type_check(value, str),
                'university': lambda value: basic_type_check(value, str),
                'class-alias': lambda value: validate_alias_field(value),
                'start-date': lambda value: validate_datetime(value)
            })
        case ('class-online-course-obj', 1):
            validator = validator.create_validator({
                'class-name': lambda value: basic_type_check(value, str),
                'instructor': lambda value: basic_type_check(value, str),
                'medium': lambda value: basic_type_check(value, str),
                'class-alias': lambda value: validate_alias_field(value),
                'start-date': lambda value: validate_datetime(value),
                'online-platform': lambda value: basic_type_check(value, str),
                'length': lambda value: basic_type_check(value, str)
            })
        case _:
            return ["Template Name Not Recognized"]
    result = validator.validate(value)
    return True if isinstance(result, bool) else result[1]
