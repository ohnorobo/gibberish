#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, pprint, random, re, os, sys, pickle

##################
##################
#ISO

iso_codes = {
 "om" : "Oromo",
 "ab" : "Abkhazian",
 "aa" : "Afar",
 "af" : "Afrikaans",
 "sq" : "Albanian",
 "am" : "Amharic",
 "ar" : "Arabic",
 "hy" : "Armenian",
 "as" : "Assamese",
 "ay" : "Aymara",
 "az" : "Azerbaijani",
 "ba" : "Bashkir",
 "eu" : "Basque",
 "bn" : "Bengali",
 "dz" : "Bhutani",
 "bh" : "Bihari",
 "bi" : "Bislama",
 "br" : "Breton",
 "bg" : "Bulgarian",
 "my" : "Burmese",
 "be" : "Byelorussian",
 "km" : "Cambodian",
 "ca" : "Catalan",
 "zh" : "Chinese",
 "co" : "Corsican",
 "hr" : "Croatian",
 "cs" : "Czech",
 "da" : "Danish",
 "nl" : "Dutch",
 "en" : "English",
 "eo" : "Esperanto",
 "et" : "Estonian",
 "fo" : "Faeroese",
 "fj" : "Fiji",
 "fi" : "Finnish",
 "fr" : "French",
 "fy" : "Frisian",
 "gl" : "Galician",
 "ka" : "Georgian",
 "de" : "German",
 "el" : "Greek",
 "kl" : "Greenlandic",
 "gn" : "Guarani",
 "gu" : "Gujarati",
 "ha" : "Hausa",
 "he" : "Hebrew",
 "hi" : "Hindi",
 "hu" : "Hungarian",
 "is" : "Icelandic",
 "id" : "Indonesian",
 "ia" : "Interlingua",
 "ie" : "Interlingue",
 "ik" : "Inupiak",
 "iu" : "Inuktitut",
 "ga" : "Irish",
 "it" : "Italian",
 "ja" : "Japanese",
 "jw" : "Javanese",
 "kn" : "Kannada",
 "ks" : "Kashmiri",
 "kk" : "Kazakh",
 "rw" : "Kinyarwanda",
 "ky" : "Kirghiz",
 "rn" : "Kirundi",
 "ko" : "Korean",
 "ku" : "Kurdish",
 "lo" : "Laothian",
 "la" : "Latin",
 "lv" : "LatvianLettish",
 "ln" : "Lingala",
 "lt" : "Lithuanian",
 "mk" : "Macedonian",
 "mg" : "Malagasy",
 "ms" : "Malay",
 "ml" : "Malayalam",
 "mt" : "Maltese",
 "mi" : "Maori",
 "mr" : "Marathi",
 "mo" : "Moldavian",
 "mn" : "Mongolian",
 "na" : "Nauru",
 "ne" : "Nepali",
 "no" : "Norwegian",
 "oc" : "Occitan",
 "or" : "Oriya",
 "ps" : "PashtoPushto",
 "fa" : "Persian",
 "pl" : "Polish",
 "pt" : "Portuguese",
 "pa" : "Punjabi",
 "qu" : "Quechua",
 "rm" : "RhaetoRomance",
 "ro" : "Romanian",
 "ru" : "Russian",
 "sm" : "Samoan",
 "sg" : "Sangro",
 "sa" : "Sanskrit",
 "gd" : "Scots Gaelic",
 "sr" : "Serbian",
 "sh" : "SerboCroatian",
 "st" : "Sesotho",
 "tn" : "Setswana",
 "sn" : "Shona",
 "sd" : "Sindhi",
 "si" : "Singhalese",
 "ss" : "Siswati",
 "sk" : "Slovak",
 "sl" : "Slovenian",
 "so" : "Somali",
 "es" : "Spanish",
 "su" : "Sudanese",
 "sw" : "Swahili",
 "sv" : "Swedish",
 "tl" : "Tagalog",
 "tg" : "Tajik",
 "ta" : "Tamil",
 "tt" : "Tatar",
 "te" : "Tegulu",
 "th" : "Thai",
 "bo" : "Tibetan",
 "ti" : "Tigrinya",
 "to" : "Tonga",
 "ts" : "Tsonga",
 "tr" : "Turkish",
 "tk" : "Turkmen",
 "tw" : "Twi",
 "ug" : "Uigur",
 "uk" : "Ukrainian",
 "ur" : "Urdu",
 "uz" : "Uzbek",
 "vi" : "Vietnamese",
 "vo" : "Volapuk",
 "cy" : "Welch",
 "wo" : "Wolof",
 "xh" : "Xhosa",
 "yi" : "Yiddish",
 "yo" : "Yoruba",
 "za" : "Zhuang",
 "zu" : "Zulu"
}



def get_language_full_name(code):
    global iso_codes

    if (code in iso_codes):
        return iso_codes[code]
    else:
        return code


##################
##################
#train


import codecs

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
    errors = 0
    filepath = "./data/" + language + "/" + location + "/" + filename

    #for some reason my french/russian dictionaries are utf-16
    #f = codecs.open(filepath, encoding ='utf-16', mode="r")
    f = codecs.open(filepath, encoding ='utf-16-be', mode="r")

    # greek - iso8859-7

    #for ascii files (needed?)
    #f = open(filepath, "r")

    #for utf8 files, with replace for errors
    f = codecs.open(filepath, encoding='utf-8', mode='r', errors='replace')

    c = u" "
    word = u""

    while c != u"": #EOF
        c = f.read(1)

        if c == u" " or c == u"\n":
            #add word to ngrams
            if len(word) > 0:
                if not u"\ufffd" in word:
                    #skip words with error codes
                    errors += 1
                print word
                add_word_to_ngrams(ngrams, n, word)
            word = u""
        else:
            word += c

    print "errors", errors

##########
#make ngram list

#takes an n-length array [a, b, c]
#and an n-nested array
#changes the element at array[a][b][c]
#nesting must be >= length of loc
#all elements of loc must be < length of nested arrays
def change_nested_element(loc, nested):
    if len(loc) == 1 :
        instantiate_or_increment(loc[0], nested)
        return nested[loc[0]]
    else:
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
    padded_word = u" "*padding+ word + u" "*padding

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



##################
##################
#make

import string

##########
#generate string

def generate_string(xgrams, x):
    padding = x-1
    string = u" "*padding

    while True:
        string = add_likely_char(string, xgrams, x)
        if string[-1:] == " ": #add until space
            break
    return string.strip()

def get_nested_element(loc, nested):
    if len(loc) == 1:
        return nested[loc[0]]
    else:
        return get_nested_element(loc[1:], nested[loc[0]])


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


def generate_m_strings(m, ngrams, n):
    strings = []
    for i in range(m):
        strings.append(generate_string(ngrams, n))
        #print string #.encode('unicode')
            #encoding for non-english chars
    return strings

##################
##################
#Administration methods

PICKLE_LOCATION = "./all_ngrams"
all_ngrams = {}


def train_ngrams_w_ngrams(lang, n, all_ngrams):
    #TODO do we want to be able to store different gram for the same language?
    # (say store both 4grams and 5grams for russian simultaniously)
    ngrams = generate_ngrams(lang, n)
    all_ngrams[lang] = [n, ngrams]

def generate_strings_w_ngrams(lang, m, all_ngrams):

    if not all_ngrams.has_key(lang):
        print "no ngrams trained for " + lang
        print "current ngrams trained:"
        print all_ngrams.keys()

    else:
        pair = all_ngrams[lang]
        n = pair[0]
        ngrams = pair[1]
        return generate_m_strings(m, ngrams, n)

##################

#get stored ngrams
def load_ngrams():
    global all_ngrams
    if os.path.isfile("./all_ngrams"):
        f = file(PICKLE_LOCATION, "r")
        all_ngrams = pickle.load(f)
    else:
        print "couldn't find file, starting from scratch"
        all_ngrams = {}

#store ngrams
def save_ngrams(all_ngrams):
    f = file(PICKLE_LOCATION, "w")
    pickle.dump(all_ngrams, f)

##################
#Programatic interface

def generate_strings(lang, m):
    return generate_strings_w_ngrams(lang, m, all_ngrams)

def train_ngrams(lang, n):
    train_ngrams_w_ngrams(lang, n, all_ngrams)
    save_ngrams(all_ngrams)

def get_available_languages():
    return all_ngrams.keys()

##################
#Command line interface

def print_instructions():
    print '''How to use gibberish:

          ./gibberish lang_code train n
          finds examples of that language created ngrams
          ex: ./gibberish de train 4

          ./gibberish lang_code make n
          produces n nonsense words of the given language
          ex: ./gibberish en make 10

          language codes are in ISO 639-1'''

##########

def run_interactivly():
    load_ngrams()

def run_on_command_line():
    if not(len(sys.argv) == 4):
        print_instructions()
        exit()

    load_ngrams()

    #get command args
    lang = sys.argv[1]
    operation = sys.argv[2]
    number = sys.argv[3]
    n = int(number)

    #train about data
    if operation == "train":
        train_ngrams(lang, n)
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

if __name__ == "__main__": #i.e. run directly
    run_on_command_line()
else:
    run_interactivly()
