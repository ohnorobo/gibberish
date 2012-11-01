#!/usr/bin/python

import nltk, sys, re, string, unicodedata, codecs



#####################################


PRINTABLE = set(('Lu', 'Ll', 'Mc', 'Zs'))
#Lu = letter uppercase
#Ll = letter lowercase
#Lt = letter titlecase
#Lm = letter modifier
#Lo = letter other
#Mn = mark nonspacing (mostly combining chars)
#Mc = mark spacing, combining

#Zs = separator space

#only letters and spaces included, 
#no punctuation or numbers

#http://www.sql-und-xml.de/unicode-database/#kategorien


#####################################

def filter_non_printable(s):
    result = []
    ws_last = False
    for c in s:
        c = unicodedata.category(c) in PRINTABLE and c or u'#'
        result.append(c)
    return u''.join(result).replace(u'#', u'')




#####################################
#####Main#####

#pattern = re.compile('([^a-zA-Z]|_)')

filename = sys.argv[1]
#f = file(filename)
f = codecs.open(filename, encoding='utf-8', mode='r')
content = f.read()

newcontent = nltk.clean_html(content)
newcontent = ' '.join(newcontent.split())
#newcontent = pattern.sub('', newcontent)
newcontent = filter_non_printable(newcontent)

print newcontent





#http://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
