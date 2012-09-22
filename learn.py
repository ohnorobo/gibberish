#!/usr/bin/python

import string, re, os, sys, pprint

##########
#get/clean data

#dict uses found dictionary files
location = "dict"

#clean uses cleaned wikipedia articles (doesn't work)
#location = "clean"

##########

def add_all_files(ngrams, n, language):
    filenames = os.listdir("./data/" + language + "/" + location + "/")

    for filename in filenames:
        add_whole_file_to_ngrams(ngrams, n, language, filename)


def add_whole_file_to_ngrams(ngrams, n, language, filename):
    filepath = "./data/" + language + "/" + location + "/" + filename
    f = open(filepath, "r")

    c = " "
    word = ""

    while c != "": #EOF
        c = f.read(1)

        if c == " " or c == "\n":
            #add word to ngrams
            if len(word) > 0:
                add_word_to_ngrams(ngrams, n, word)
            word = ""
        else:
            word += c
    
##########
#make ngram list

#takes an n-length array [a, b, c]
#and an n-nested array
#changes the element at array[a][b][c]
#nesting must be >= length of loc
#all elements of loc must be < length of nested arrays
def change_nested_element(loc, nested):
    if len(loc) == 1 :
        #print "loc" + str(loc) + "\""
        instantiate_or_increment(loc[0], nested)
        return nested[loc[0]]
    else:
        #print "loc" + str(len(loc)) + str(loc) + "\""
        #print nested
        return change_nested_element(loc[1:], 
                                     instantiate_and_return(loc[0], nested))

def instantiate_or_increment(key, dicti):
    if key in dicti:
        dicti[key] += 1
    else:
        dicti[key] = 1

def instantiate_and_return(key, dicti):
    if not key in dicti:
        dicti[key] = {}
    return dicti[key]


def add_word_to_ngrams(ngrams, n, word):
    padding = n-1
    padded_word = " "*padding+ word + " "*padding

    for i in range( len(word)+padding ):
        gram = padded_word[i:i+n]
        change_nested_element(gram, ngrams)

    return ngrams



#make ngrams from all words
def generate_ngrams(lang, n):

    #read in wordlists from all files in lang/dict
    #TODO actually pull data from wikipedia in lang/clean

    ngrams = {}
    add_all_files(ngrams, n, lang)

    pprint.pprint(ngrams)

    return ngrams
