#!/usr/bin/python

import string, re, os, sys

##########
#get/clean data

#get text
def file_to_wordlist(language, filename):
    filepath = "./data/" + language + "/clean/" + filename
    f = open(filepath, "r")
    content = f.read()
    #content.rstrip()
    #re.sub(r'[a-z\ ]*', '', content)

    #sanitize
    for w in content:
        if not (w.islower() or w == " "):
            w = " "
    return get_wordlist(content)


def get_all_files(language):
    filenames = os.listdir("./data/" + language + "/clean/")
    total_wordlist =[]
    for filename in filenames:
        total_wordlist += file_to_wordlist(language, filename)
    return total_wordlist

#get wordlist
def get_wordlist(clean_text):
    return clean_text.split(" ")

    
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


def add_word_to_xgrams(xgrams, x, word):
    padding = x-1
    padded_word = " "*padding+ word + " "*padding

    for i in range( len(word)+padding ):
        gram = padded_word[i:i+x]
        change_nested_element(gram, xgrams)

    return xgrams



#make ngrams from all words
def generate_ngrams(lang, n):

    #read in wordlists from all files in lang/clean
    #TODO actually pull data from wikipedia
    all_wordlist = get_all_files(lang)
    #file_to_wordlist(lang, "2of12inf.txt")

    grams = {}
    for word in all_wordlist:
        add_word_to_xgrams(grams, n, word)

    return grams
