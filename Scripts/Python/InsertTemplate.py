from pandas import DataFrame, concat, Series
from pathlib import Path
import pyomd
from pyomd import Note
from WrapperNoteClasses import WrapperNote
from NotesConstructor import get_frontmatter_str

def getTermplateContent(df: DataFrame, chosen_template: str):
    notes = df['note']
    target_template = notes[Path(chosen_template)]

    # grab template metadata Dict
    template_dict = target_template.metadata.frontmatter._parse(target_template.metadata.frontmatter.to_string())

    if 'type' in template_dict['template']:
        if target_template.metadata.get('template')['type'] == 'object':
            keys = template_dict.keys()
            for key in keys:
                template_dict[key] = target_template.metadata.get(key)
                if len(template_dict[key]) == 1:
                    template_dict[key] = template_dict[key][0]
            return {'content': str(template_dict), 'type': 'object'}
        else:
            frontmatter = target_template.metadata.frontmatter.to_string()
            content = target_template.content
            return {'content': frontmatter + content, 'type': 'template'}
    else:
        frontmatter = get_frontmatter_str(target_template.path)
        content = target_template.content
        return {'content': frontmatter + content, 'type': 'template'}
