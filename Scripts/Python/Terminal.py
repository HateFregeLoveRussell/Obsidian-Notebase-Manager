from pathlib import Path
from pyomd import Notes, Note
from pyomd.metadata import MetadataType
import NotesConstructor
from NoteBookKeepingUtilities import updateNoteFrame
from  NoteMetadataFuzzymatching import fuzzyMatch
from argparse import ArgumentParser

def TerminalFuzzyMatch():
    parser = ArgumentParser(description='Fuzzy-searches the note base and returns best matching note paths')
    parser.add_argument('field', metavar='field', type=str, nargs=1, help='the metadata field to fuzzymatch '
                                                                          'on - arrays and objects not supported')
    parser.add_argument('value', metavar='value', type= str, nargs=1, help='the value of chosen field to fuzzymatch on')
    parser.add_argument('bounds', metavar='bounds', type=int, nargs=2, help='the bounds of how many entries '
                                                                            'in matched list is returned')
    args = parser.parse_args()
    notes = updateNoteFrame()
    print([args.value, args.field])
    print(fuzzyMatch(notes, args.field[0], args.value[0], args.bounds).to_json(orient='index'))

