from flask import Flask, request, jsonify

from NoteBookKeepingUtilities import updateNoteFrame
from NoteMetadataFuzzymatching import findfuzzMatchedTemplate, findFuzzMatchedSourceObjByAlias, fuzzyMatch
from InsertTemplate import getTermplateContent
from MetadataValidation.NoteMetadataValidator import validate_template
from pyomd import Notes
from pathlib import Path

app = Flask(__name__)


@app.route('/fuzzyMatch', methods=['POST'])
def fuzzy():
    try:
        data = request.json
        notes = updateNoteFrame()
        rtrn_json = fuzzyMatch(notes, data['field'], data['value'], data['bounds']).to_json(orient='index')

        return rtrn_json
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/fuzzyMatch/SearchSourcesByAlias', methods = ['POST'])
def fuzzyMatchSourceOnAlias():
    try:
        data = request.json
        notes = updateNoteFrame()
        rtrn_json = findFuzzMatchedSourceObjByAlias(notes, data['value'], data['bounds']).to_json(orient='index')
        print(rtrn_json)
        return rtrn_json
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/fuzzyMatch/templateSearch', methods=['POST'])
def fuzzyTemplateSearch():
    try:
        data = request.json
        notes = updateNoteFrame()
        rtrn_json = findfuzzMatchedTemplate(notes, data['value'], data['bounds']).to_json(orient='index')
        print(rtrn_json)
        return rtrn_json
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/getTemplateContent', methods=['POST'])
def getTemplateContent():
    try:
        data = request.json
        notes = updateNoteFrame()
        rtrn_dict = getTermplateContent(notes, data['path'])
        return jsonify(rtrn_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/validateNote', methods=['POST'])
def validateNote():
    try:
        data = request.json
        notes = updateNoteFrame()
        print("Notes Constructed, Validating...")
        print(f"Path {data['path']}")
        rtrn_dict = validate_template(notes, data['path'])
        return jsonify(rtrn_dict)
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
