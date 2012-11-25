#!/usr/bin/python
import flask, gibberish

app = flask.Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/index/<lang>")
def index(lang):
    w = gibberish.generate_strings(lang, 5)
    available_langs = gibberish.get_available_languages()
    return flask.render_template("index.html", words=w, lang=lang, available_languages=available_langs)

@app.route("/")
@app.route("/index")
def indexen():
    return index("en")


if __name__ == "__main__":
    #app.debug = True
    app.run(port=80)
