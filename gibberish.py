#!/usr/bin/python

import string, pprint, random, re, os, sys, pickle


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

def get_nested_element(loc, nested):
    if len(loc) == 1:
        return nested[loc[0]]
    else:
        return get_nested_element(loc[1:], nested[loc[0]])



##########
#generate string

def generate_string(xgrams, x):
    padding = x-1
    string = " "*padding

    while True:
        string = add_likely_char(string, xgrams, x)
        if string[-1:] == " ": #add until space
            break
    return string.strip()


def add_likely_char(string, xgrams, x):
    padding = x-1
    tail = string[-1*padding:]

    char = choose_likely_char(tail, xgrams, x)

    string += char
    return string

def choose_likely_char(tail, xgrams, x):
    probabilities = get_nested_element(tail, xgrams)

    #fill a 'bucket' with elements
    #with number representing the probability of choosing each element
    #then choose one randomly
    bucket = []
    for key in probabilities:
        count = probabilities[key]
        bucket += key*count

    picker = random.randrange(0,len(bucket))
    char = bucket[picker]
    return char
   

##########
#make ngrams from all words
def generate_ngrams(lang, n):

    #read in wordlists from all files in lang/clean
    #TODO actually pull data from wikipedia
    all_wordlist = file_to_wordlist(lang, "2of12inf.txt")

    grams = {}
    for word in all_wordlist:
        add_word_to_xgrams(grams, n, word)

    return grams



def generate_m_strings(m, ngrams, n):
    for i in range(m):
        print generate_string(ngrams, n)



##################
##################
#Administration methods

def learn_ngrams(lang, n, all_ngrams):
    #TODO do we want to be able to store different gram for the ame language?
    # (say store both 4grams and 5grams for russian simultaniously)
    ngrams = generate_ngrams(lang, n)
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
        generate_m_strings(m, ngrams, n)


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


