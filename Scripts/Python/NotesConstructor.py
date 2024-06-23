
from pyomd.metadata import NoteMetadata
from WrapperNoteClasses import WrapperNote
from datetime import datetime
from mmap import mmap,ACCESS_READ
from pathlib import Path
def construct(path: Path):
    root_directory = path
    notes = {}
    for path_obj in root_directory.rglob('*.md'):
        if (path_obj.stat().st_size == 0):
            continue
        file_frontmatter = get_frontmatter_str(path_obj);
        content = get_content_str(path_obj)
        note = WrapperNote(NoteMetadata(file_frontmatter), content, path_obj, datetime.fromtimestamp(path_obj.stat().st_mtime))
        notes[path_obj] = note
    return notes
def construct_note(path: Path):
    if (path.stat().st_size == 0):
        return
    file_frontmatter = get_frontmatter_str(path);
    content = get_content_str(path)
    note = WrapperNote(NoteMetadata(file_frontmatter), content, path, datetime.fromtimestamp(path.stat().st_mtime))
    return note

def get_frontmatter_str(path):
    assert path.exists()
    assert not path.is_dir()
    assert path.suffix == '.md'
    assert not path.stat().st_size == 0
    with path.open(mode='rb') as f:
        with mmap(f.fileno(),0, access=ACCESS_READ) as mmapped_f:
            delimiter = '---'.encode()
            delimiter_length = len(delimiter)
            start = 0
            startpos = mmapped_f.find(delimiter, start)
            if startpos == -1:
                return ''
            endpos = mmapped_f.find(delimiter, startpos + delimiter_length)
            if endpos == -1:
                return ''
            f.seek(startpos)
            content = f.read(endpos + delimiter_length - startpos).decode('utf-8')
            mmapped_f.close()
            print(content)
            return content
def get_content_str(path):
    assert path.exists()
    assert not path.is_dir()
    assert path.suffix == '.md'
    assert not path.stat().st_size == 0
    with path.open(mode='rb') as f:
        with mmap(f.fileno(),0, access=ACCESS_READ) as mmapped_f:
            delimiter = '---'.encode()
            delimiter_length = len(delimiter)
            start = 0
            startpos = mmapped_f.find(delimiter, start)
            if startpos == -1:
                content = f.read().decode('utf-8')
                # print(content)
                return content
            endpos = mmapped_f.find(delimiter, startpos + delimiter_length)
            if endpos == -1:
                # print('funny')
                return ''
            f.seek(endpos + delimiter_length)
            content = f.read().decode('utf-8')
            mmapped_f.close()
            # print(content)
            return content