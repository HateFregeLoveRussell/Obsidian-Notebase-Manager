from pickle import dump, load
from pathlib import Path
from datetime import datetime
from NotesConstructor import construct_note, construct
from pandas import DataFrame
from Config import CACHE_PATH,NOTE_BASE_PATH

def updateNoteFrame():
    # check if cache exists update, otherwise build cache
    if not Path(CACHE_PATH).exists():
        note_dict = construct(NOTE_BASE_PATH)
        store_notes(note_dict, CACHE_PATH)
    else:
        note_dict = updateCache()
    note_data_frame = DataFrame({'note': note_dict.values()}, index=note_dict.keys())
    return note_data_frame

def updateCache():
    notes = extract_notes(CACHE_PATH)
    check_for_updates(notes)
    store_notes(notes, CACHE_PATH)
    return notes


def check_for_updates(noteDict: dict):
    # first find root directory of notebase
    paths = list(noteDict.keys())
    # Get the parts of the first path
    first_parts = paths[0].parts
    # Find the common root by comparing each part of the first path with the other paths
    common_root_parts = []
    for i, part in enumerate(first_parts):
        if all(p.parts[i] == part for p in paths):
            common_root_parts.append(part)
        else:
            break
    common_root = Path(*common_root_parts)
    root_paths = list(common_root.rglob('*.md'))
    # remove dicts no longer present in dir
    for path in paths:
        if path not in root_paths:
            #print(f"deleted note found at {path}")
            noteDict.pop(path)
        elif (path.stat().st_size == 0):
            #print(f'file at {path} now empty, removing from memory...')
            noteDict.pop(path)

    for path_obj in root_paths:
        if (path_obj.stat().st_size == 0):
            continue
        if path_obj in noteDict.keys():
            if datetime.fromtimestamp(path_obj.stat().st_mtime) != noteDict[path_obj].mtime:
                # update entry if edit times don't match
                #print(f"update found in entry: {path_obj}, Discrepancy: {datetime.fromtimestamp(path_obj.stat().st_mtime)}, {noteDict[path_obj].mtime}")
                noteDict[path_obj] = construct_note(path_obj)
                #print(noteDict[path_obj].content)
                #print(path_obj)
                #print(noteDict[path_obj])
        else:  # dir entry not in mem => new note
            #print(f"New entry found at: {path_obj}")
            noteDict[path_obj] = construct_note(path_obj)

    return noteDict


def store_notes(notes, filename: str):
    with open(filename, 'wb') as f:
        dump(notes, f);
    f.close()
    return


def extract_notes(filename: str):
    with open(filename, 'rb') as f:
        notes = load(f)
    f.close()
    return notes


