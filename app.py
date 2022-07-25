import io
import json

from flask import Flask, render_template, send_from_directory, jsonify, request
from docx import Document
from flask_cors import CORS
import uuid
import utils.CVTransformer as CVTransformer
import utils.fillTemplate as fillTemplate
import utils.Output as Output
from docx import Document

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*": {'origins': "*"}})
# CORS(app, resources={r'/*':{'origins': 'http://localhost:8080',"allow_headers": "Access-Control-Allow-Origin"}})


cvTransformer = CVTransformer.CVTransformer()


# hello world route
@app.route('/', methods=['GET'])
def greetings():
    return ("ACTIVE")


@app.route('/upload', methods=['POST'])
def uploadFile():
    f = request.files["file"]
    f.save('assets/uploaded.pdf')
    cvTransformer.prepare_and_extract('assets/uploaded.pdf')
    return jsonify(success=True)


@app.route('/solitan', methods=['GET'])
def getSolitan():
    string = json.dumps({"data": cvTransformer.solitan.toDict()})
    return string


@app.route('/render', methods=['POST'])
def renderFile():
    json = request.json
    Output.addExTable('assets/templates/cv_template.docx', 'assets/templates/semi_filled_template.docx', json)
    fillTemplate.argenta('assets/templates/semi_filled_template.docx', 'assets/templates/filled_template.docx', json)

    return send_from_directory(directory='assets/templates', path='filled_template.docx', as_attachment=True,
                               attachment_filename='CV_Transformed.docx')


if __name__ == "__main__":
    app.run(debug=True)
