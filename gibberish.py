#!/usr/bin/python

import string, pprint, random, re, os, sys, pickle
import learn, make

PICKLE_LOCATION = "./all_ngrams"
all_ngrams = {}

##################
##################
#Administration methods

def learn_ngrams_w_ngrams(lang, n, all_ngrams):
    #TODO do we want to be able to store different gram for the same language?
    # (say store both 4grams and 5grams for russian simultaniously)
    ngrams = learn.generate_ngrams(lang, n)
    all_ngrams[lang] = [n, ngrams]

def generate_strings_w_ngrams(lang, m, all_ngrams):
    if not all_ngrams.has_key(lang):
        print "no ngrams learned for " + lang
        print "current ngrams learned:"
        print all_ngrams.keyset()

    else:
        pair = all_ngrams[lang]
        n = pair[0]
        ngrams = pair[1]
        return make.generate_m_strings(m, ngrams, n)

##################

#get stored ngrams
def load_ngrams():
    if os.path.isfile("./all_ngrams"):
        f = file(PICKLE_LOCATION, "r")
        all_ngrams = pickle.load(f)
    else:
        all_ngrams = {}
    return all_ngrams

#store ngrams
def save_ngrams(all_ngrams):
    f = file(PICKLE_LOCATION, "w")
    pickle.dump(all_ngrams, f)

##################
#Programatic interface

def generate_strings(lang, m):
    return generate_strings_w_ngrams(lang, m, all_ngrams)

def learn_ngrams(lang, n):
    learn_ngrams_w_ngrams(lang, n, all_ngrams)
    save_ngrams(all_ngrams)

def get_available_languages():
    return all_ngrams.keys()

##################
#Command line interface

def print_instructions():
    print '''How to use gibberish:

          ./gibberish lang_code learn n
          finds examples of that language created ngrams
          ex: ./gibberish de learn 4

          ./gibberish lang_code make n
          produces n nonsense words of the given language
          ex: ./gibberish en make 10

          language codes are in ISO 639-1'''

##########

#if there are no command line args run interactivly
if len(sys.argv) < 2:
    all_ngrams = load_ngrams()

else:

    if not(len(sys.argv) == 4):
        print_instructions()
        exit()

    all_ngrams = load_ngrams()

    #get command args
    lang = sys.argv[1]
    operation = sys.argv[2]
    number = sys.argv[3]
    n = int(number)

    #learn about data
    if operation == "learn":
        learn_ngrams(lang, n)
        exit()

    #generate strings
    if operation == "make":
        words = generate_strings(lang, n)
        for word in words:
            print word
        exit()

    else:
        print_instructions()
        exit()

##########

