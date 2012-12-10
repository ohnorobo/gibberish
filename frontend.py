#!/usr/bin/python
import sys, flask, gibberish

app = flask.Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/index/<lang>")
def index(lang):
    w = gibberish.generate_strings(lang, 5)
    print w
    available_langs = gibberish.get_available_languages()
    return flask.render_template("index.html", words=w, lang=lang, available_languages=available_langs)

@app.route("/")
@app.route("/index")
def indexen():
    return index("en")


if __name__ == "__main__":
    app.debug = True

    port=80    #run on 80 by default
    host="127.0.0.1"

    if sys.argv[1]: #run on port given from heroku
        port=sys.argv[1]
    if sys.argv[2]: #run on host given from heroku
        host = sys.argv[2]

    app.run(host=host, port=int(port))
    #app.run(port=int(port))
