from thefuzz.fuzz import partial_ratio, ratio, token_sort_ratio, token_set_ratio
from pandas import DataFrame, concat, Series
from MetadataValidation.ValidationFunctions.NoteMetadataValidatorUtilities import (validate_class_field
                                                                                        , validate_source_field)
from json import loads


def fuzzyMatch(df: DataFrame, field: str, value, indexRange=(0, 5)):
    notes = df['note'].apply(lambda x: x.metadata.get(field)).rename(field)
    notes = notes.dropna(how='any')
    notes = notes.apply(lambda x: x[0])
    notes = concat([notes.apply(lambda x: ratio(x, value)).rename('FuzzyMatch'), notes], axis=1)
    notes = notes.sort_values(by=['FuzzyMatch'], ascending=False)
    return (notes[indexRange[0]:indexRange[1]])


def findfuzzMatchedTemplate(df: DataFrame, value, indexRange=(0, 5)):
    print(value)
    notes = df['note']
    # filter notes based on if they belong to templates library
    boolean_mask = [path.is_relative_to('..\..\Templates') for path in notes.index]
    notes = notes[boolean_mask]

    # filter notes based on if template field present in note metadata
    notes = notes.apply(lambda x: x.metadata.get('template')).rename('template')
    notes = notes.dropna(how='any')

    # filter notes based on if template is a dict containing a 'name' field
    boolean_mask = notes.apply(lambda x: 'name' in x if isinstance(x, dict) else False)
    notes = notes[boolean_mask]

    # fuzzymatch on name (we replace dashes with spaces to improve accuracy)
    notes = (concat([notes.apply(
        lambda x: token_set_ratio(x['name'].replace('-', ' '), value.replace('-', ' '))).rename('FuzzyMatch'),
                     notes.apply(lambda x: x['name']).rename('name'),
                     notes.apply(lambda x: x['version']).rename('version')], axis=1))
    notes = notes.sort_values(by=['FuzzyMatch'], ascending=False)
    # return dataframe based on index
    return (notes[indexRange[0]:indexRange[1]])
    # TODO('recursive fuzzy search')


def findFuzzMatchedClassObjByAlias(df: DataFrame, value, indexRange=(0, 5)):
    # This is done to improve the matching with token_set_ratio
    value = value.replace('-', ' ')

    notes = df['note']

    # drop entries that are from Templates Folder
    boolean_mask = [not path.is_relative_to('..\..\Templates') for path in notes.index]
    notes = notes[boolean_mask]

    # filter notes based on if source field is present
    notes = notes.apply(lambda x: x.metadata.get('class')).rename('class')
    notes = notes.dropna(how='any')

    # drop empty entries
    boolean_mask = [entry != [] and entry != "" for entry in notes]
    notes = notes[boolean_mask]

    # drop entries if they are not valid source fields
    boolean_mask = [validate_class_field(entry) == True for entry in notes]
    notes = notes[boolean_mask]


def findFuzzMatchedSourceObjByAlias(df: DataFrame, value, indexRange=(0, 5)):
    # This is done to improve the matching with token_set_ratio
    value = value.replace('-', ' ')

    notes = df['note']
    # drop entries that are from Templates Folder
    boolean_mask = [not path.is_relative_to('..\..\Templates') for path in notes.index]
    notes = notes[boolean_mask]

    # filter notes based on if source field is present
    notes = notes.apply(lambda x: x.metadata.get('source')).rename('source')
    notes = notes.dropna(how='any')

    # drop empty entries
    boolean_mask = [entry != [] and entry != "" for entry in notes]
    notes = notes[boolean_mask]

    # drop entries if they are not valid source fields
    boolean_mask = [validate_source_field(entry) == True and isinstance(validate_source_field(entry), bool) for entry in notes]

    notes = notes[boolean_mask]

    # linearize series by turning array(n) entries into n entries
    notes = notes.apply(lambda entry: entry if isinstance(entry, list) else [entry])
    notes = notes.explode()

    # dumb parsing quirk turns all entries in frontmatter list into str, we are casting them back to dicts and
    # recombining
    multi_object_entries = notes[[isinstance(entry, str) for entry in notes]]
    multi_object_entries = multi_object_entries.apply(lambda source: loads(source.replace("'", "\"")))

    single_object_entries = notes[[isinstance(entry, dict) for entry in notes]]
    notes = concat([multi_object_entries, single_object_entries])

    # filtering entries based on uniqueness, we will do this by putting the dicts into frozen sets so they can be hashed
    def dict_to_frozenset(d):
        if isinstance(d, dict):
            return frozenset((k, dict_to_frozenset(v)) for k, v in d.items())
        else:
            return d

    frozen_notes = notes.apply(dict_to_frozenset)
    frozen_notes = Series(frozen_notes.unique())

    def frozenset_to_dict(fs):
        if isinstance(fs, frozenset):
            return {key: frozenset_to_dict(value) for key, value in fs}
        else:
            return fs

    notes = frozen_notes.apply(frozenset_to_dict)

    # Fuzzy Matching on Alias
    notes = DataFrame({
        'FuzzyMatch': notes.apply(lambda x: token_set_ratio(x['source-alias'].replace('-', ' '), value)),
        'source-alias': notes.apply(lambda x: x['source-alias']),
        'source': notes})
    notes = notes.sort_values(by=['FuzzyMatch'], ascending=False)

    # Returning specified index range
    return (notes[indexRange[0]:indexRange[1]])
