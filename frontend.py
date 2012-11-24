#!/usr/bin/python
import flask, gibberish

app = flask.Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/")
@app.route("/index")
#@app.route("/index/<lang>")
def index():
    lang = "en"
    w = ["a", "b"]
    w = gibberish.generate_strings(lang, 5)
    return flask.render_template("index.html", words=w, lang=lang)


@app.route("/indexxx")
def index2():
    return flask.render_template("indexxx.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
