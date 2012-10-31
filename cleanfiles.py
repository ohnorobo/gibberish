#!/usr/bin/python

import nltk


filename = args[1]

content = filename.read()

newcontent = ntlk.clean_html(content)

print newcontent
