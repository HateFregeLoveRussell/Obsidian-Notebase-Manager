from pyomd import Note, Notes
from pyomd.metadata import NoteMetadata
from pathlib import Path


class WrapperNote(Note):
    def __init__(self, Metadata: NoteMetadata, Content: str, path: Path, mTime):
        self.metadata = Metadata
        self.content = Content
        self.path = path
        self.mtime = mTime

    def print(self):
        print(self.metadata.frontmatter)

    def get_metadata_dict(self):
        dict_keys = self.metadata.frontmatter._parse(self.metadata.frontmatter.to_string())

        def treat_dict(key):
            if len(self.metadata.get(key)) == 1:
                return self.metadata.get(key)[0]
            elif len(self.metadata.get(key)) == 0:
                return None
            else:
                return self.metadata.get(key)

        return dict((key, treat_dict(key)) for key in dict_keys)


class WrapperNotes(Notes):
    def __init__(self):
        self.metadata = None
        self.notes = []

    def append(self, note: Note):
        self.notes.append(note)
