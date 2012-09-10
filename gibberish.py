#!/usr/bin/python

import string, pprint, random, re, os, sys, pickle
import learn, make


##################
##################
#Administration methods

def learn_ngrams(lang, n, all_ngrams):
    #TODO do we want to be able to store different gram for the ame language?
    # (say store both 4grams and 5grams for russian simultaniously)
    ngrams = learn.generate_ngrams(lang, n)
    all_ngrams[lang] = [n, ngrams]

def generate_strings(lang, m, all_ngrams):
    if not all_ngrams.has_key(lang):
        print "no ngrams learned for " + lang
        print "current ngrams learned:"
        print all_ngrams.keyset()
    
    else:
        pair = all_ngrams[lang]
        n = pair[0]
        ngrams = pair[1]
        #TODO move this method to another file
        make.generate_m_strings(m, ngrams, n)


def print_instructions():
    print "How to use gibberish:"
    print ""
    print "./gibberish lang_code learn n"
    print "finds examples of that language created ngrams"
    print "ex: ./gibberish de learn 4"
    print ""
    print ".gibberish lang_code make n"
    print "produces n nonsense words of the given language"
    print "ex: ./gibberish en make 10"
    print ""
    print "language codes are in ISO 639-1"

##########
#main

if not(len(sys.argv) == 4):
    print_instructions()
    exit()

#get command args
lang = sys.argv[1]
operation = sys.argv[2]
number = sys.argv[3]
n = int(number)

#get stored ngrams
if os.path.isfile("./all_ngrams"):
    f = file("./all_ngrams", "r")
    all_ngrams = pickle.load(f)
else:
    all_ngrams = {}

#learn about data
if operation == "learn":
    #TODO
    learn_ngrams(lang, n, all_ngrams)

    f = file("./all_ngrams", "w")
    pickle.dump(all_ngrams, f) 

    exit()

#generate strings
if operation == "make":
    #TODO
    generate_strings(lang, n, all_ngrams)
    exit()

else:
    print_instructions()
    exit()

##########


