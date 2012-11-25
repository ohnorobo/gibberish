#!/usr/bin/python
import sys, flask, gibberish

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

    port=80    #run on 80 by default
    if sys.argv[1]: #run on port given from heroku
        port=sys.argv[1]

    app.run(host="0.0.0.0", port=int(port))
