from MetadataValidation.ValidationFunctions.AtomicValidationUtilities import (validate_alias_field, validate_expected_value)
from MetadataValidation.ValidationFunctions.NoteMetadataValidatorUtilities import (validate_deliverable_field,
                                                                                   validate_relationship_field,
                                                                                   validate_class_field,
                                                                                   validate_source_field,
                                                                                   validate_validity_field,
                                                                                   validate_status_field)

from MetadataValidation.NoteMetaDataValidatorClasses import DictValidatorFactory
from pathlib import Path


def validate_template(notes, path):
    path = Path(path)
    note_of_interest = notes['note'][path]
    metadata = note_of_interest.get_metadata_dict()
    print (metadata)
    if 'template' not in metadata:
        return ['No Template Field Found']
    template = metadata['template']
    match (template['name'], template['version']):
        case ('class-note-template', 1):
            validator = class_note_template_validator()
        case ('class-sched-template', 1):
            validator = class_schedule_template_validator()
        case ('class-portal-template', 2):
            validator = class_portal_template_validator()
        case ('class-deliverable-template', 1):
            validator = class_deliverable_template_validator()
        case ('class-display-portal-template', 1):
            validator = class_display_portal_template_validator()
        case ('class-dict-template', 1):
            validator = class_dictionary_template_validator()
        case ('class-bib-template', 1):
            validator = class_bibliography_template_validator()
        case ('class-textbook-practice-problem', 1):
            validator = class_textbook_problem_validator()
        case _:
            return["Template Not Recognized"]

    result = validator.validate(metadata)
    return True if isinstance(result, bool) else result[1]


def class_note_template_validator():
    validator = DictValidatorFactory().create_validator(field_validators=
                                                        {'status': lambda value: validate_status_field(value),
                                                         'validity': lambda value: validate_validity_field(value),
                                                         'alias': lambda value: validate_alias_field(value),
                                                         'type': lambda value: validate_expected_value(value,
                                                                                                       ["Academic"]),
                                                         'source': lambda value: validate_source_field(value),
                                                         'relationship': lambda value: validate_relationship_field(
                                                             value),
                                                         'class': lambda value: validate_class_field(value)})
    return validator


def class_schedule_template_validator():
    validator = DictValidatorFactory().create_validator(field_validators=
                                                        {'tags': lambda value: validate_expected_value(
                                                            [["Querynote", "Reponote"]]),
                                                         'status': lambda value: validate_status_field(value),
                                                         'validity': lambda value: validate_validity_field(value),
                                                         'alias': lambda value: validate_alias_field(value),
                                                         'type': lambda value: validate_expected_value(value,
                                                                                                       ["Academic"]),
                                                         'source': lambda value: validate_source_field(value),
                                                         'relationship': lambda value: validate_relationship_field(
                                                             value),
                                                         'class': lambda value: validate_class_field(value)})
    return validator


def class_portal_template_validator():
    validator = DictValidatorFactory().create_validator(field_validators=
                                                        {'tags': lambda value: validate_expected_value(value,
                                                                                                       ["Entrynote"]),
                                                         'status': lambda value: validate_status_field(value),
                                                         'validity': lambda value: validate_validity_field(value),
                                                         'alias': lambda value: validate_alias_field(value),
                                                         'type': lambda value: validate_expected_value(value,
                                                                                                       ["Academic"]),
                                                         'source': lambda value: validate_source_field(value),
                                                         'relationship': lambda value: validate_relationship_field(
                                                             value),
                                                         'class-status': lambda value: validate_status_field(value),
                                                         'class': lambda value: validate_class_field(value)})
    return validator


def class_deliverable_template_validator():
    validator = DictValidatorFactory().create_validator(field_validators=
                                                        {'status': lambda value: validate_status_field(value),
                                                         'validity': lambda value: validate_validity_field(value),
                                                         'alias': lambda value: validate_alias_field(value),
                                                         'deliverable': lambda value: validate_deliverable_field(value),
                                                         'type': lambda value: validate_expected_value(value,
                                                                                                       ["Academic"]),
                                                         'relationship': lambda value: validate_relationship_field(
                                                             value),
                                                         'class': lambda value: validate_class_field(value)})
    return validator


def class_display_portal_template_validator():
    validator = DictValidatorFactory().create_validator(field_validators=
                                                        {'status': lambda value: validate_status_field(value),
                                                         'validity': lambda value: validate_validity_field(value),
                                                         'alias': lambda value: validate_alias_field(value),
                                                         'tags': lambda value: validate_expected_value(value,
                                                                                                       ["Querynote"]),
                                                         'type': lambda value: validate_expected_value(value,
                                                                                                       ["Academic"]),
                                                         'relationship': lambda value: validate_relationship_field(
                                                             value),
                                                         'class': lambda value: validate_class_field(value)})
    return validator


def class_dictionary_template_validator():
    validator = DictValidatorFactory().create_validator(field_validators=
                                                        {'status': lambda value: validate_status_field(value),
                                                         'validity': lambda value: validate_validity_field(value),
                                                         'alias': lambda value: validate_alias_field(value),
                                                         'tags': lambda value: validate_expected_value(value, [
                                                             ["Dict", "Reponote"]]),
                                                         'type': lambda value: validate_expected_value(value,
                                                                                                       ["Academic"]),
                                                         'relationship': lambda value: validate_relationship_field(
                                                             value),
                                                         'class': lambda value: validate_class_field(value)})
    return validator


def class_bibliography_template_validator():
    validator = DictValidatorFactory().create_validator(field_validators=
                                                        {'status': lambda value: validate_status_field(value),
                                                         'validity': lambda value: validate_validity_field(value),
                                                         'alias': lambda value: validate_alias_field(value),
                                                         'tags': lambda value: validate_expected_value(value, [
                                                             ['Bib', 'Reponote']]),
                                                         'type': lambda value: validate_expected_value(value,
                                                                                                       ["Academic"]),
                                                         'relationship': lambda value: validate_relationship_field(
                                                             value),
                                                         'source': lambda value: validate_source_field(value),
                                                         'class': lambda value: validate_class_field(value)})
    return validator


def class_textbook_problem_validator():
    validator = DictValidatorFactory().create_validator(field_validators=
                                                        {'status': lambda value: validate_status_field(value),
                                                         'validity': lambda value: validate_validity_field(value),
                                                         'alias': lambda value: validate_alias_field(value),
                                                         'tags': lambda value: validate_expected_value(value, [
                                                             'practice']),
                                                         'type': lambda value: validate_expected_value(value,
                                                                                                       ["Academic"]),
                                                         'relationship': lambda value: validate_relationship_field(
                                                             value),
                                                         'class': lambda value: validate_class_field(value)})
    return validator
