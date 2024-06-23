import pyomd
from pathlib import Path
from NoteBookKeepingUtilities import updateNoteFrame

def cacheTemplateCache(path: Path):
    notes = updateNoteFrame()
    ObjectNote = notes[path]
