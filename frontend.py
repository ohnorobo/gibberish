#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, flask, gibberish
import iso_lang_codes

app = flask.Flask(__name__)

@app.route("/index/<lang>")
def index(lang):
    w = gibberish.generate_strings(lang, 5)
    available_langs = gibberish.get_available_languages()
    lang_name = iso_lang_codes.get_language_full_name(lang)

    return flask.render_template("index.html", words=w, lang=lang_name, available_languages=available_langs)

@app.route("/")
@app.route("/index")
def index_en():
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
