#  @Bek Brace [ Twitter - Dev.to - GitHub ]
#  VueJs - Flask Full-Stack Web Application
#  bekbrace.com - info@bekbrace.com
#  Source Code : Michael Hermann [ mjheaO ]
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
    return ("Hello, world!")


@app.route('/shark', methods=['GET'])
def shark():
    return ("Shark🦈!")


GAMES = {'id': uuid.uuid4().hex,
         'title': '2k21',
         'genre': 'sports',
         'played': True,
         }


# The GET and POST route handler
@app.route('/games', methods=['GET', 'POST'])
def all_games():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        GAMES.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'genre': post_data.get('genre'),
            'played': post_data.get('played')})
        response_object['message'] = 'Game Added!'
    else:
        response_object['games'] = GAMES
    return jsonify(response_object)


# The PUT and DELETE route handler
@app.route('/games/<game_id>', methods=['PUT', 'DELETE'])
def single_game(game_id):
    response_object = {'status': 'success'}
    if request.method == "PUT":
        post_data = request.get_json()
        remove_game(game_id)
        GAMES.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'genre': post_data.get('genre'),
            'played': post_data.get('played')
        })
        response_object['message'] = 'Game Updated!'
    if request.method == "DELETE":
        remove_game(game_id)
        response_object['message'] = 'Game removed!'
    return jsonify(response_object)


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


# Removing the game to update / delete
def remove_game(game_id):
    for game in GAMES:
        if game['id'] == game_id:
            GAMES.remove(game)
            return True
    return False


@app.route('/getfile', methods=['GET'])
def index():
    return send_from_directory(directory='assets/templates' ,path='filled_template.docx', as_attachment=True,
                               attachment_filename='report.docx')


if __name__ == "__main__":
    app.run(debug=True)
