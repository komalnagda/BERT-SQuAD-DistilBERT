from flask import request, jsonify
from flask_cors import CORS, cross_origin
from model import model
import flask
import os


app = flask.Flask(__name__)
CORS(app, support_credentials=True)
app.config["DEBUG"] = False


@app.route('/')
def index():

    if request.args:

        context = request.args["context"]
        question = request.args["question"]

        answer = model.predict(context, question)
        print(answer["answer"])

        return flask.render_template('index.html', question=question, answer=answer["answer"], content=context)
    else:
        return flask.render_template('index.html')


@app.route('/api', methods=['POST'])
@cross_origin(supports_credentials=True)
def root():
    if request.form.get("context", "") and request.form.get("question", ""):

        context = request.form.get("context")
        question = request.form.get("question")

        answer = model.predict(context, question)
        print(answer["answer"])

        return jsonify({"message": dict(question=question, answer=answer["answer"])}), 200
    else:
        return jsonify({"message": "something went wrong"}), 400


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
