#!/usr/bin/python

import string, pprint, random

#get arguments
# gibbrish generate [language-code] 
# gibberish save [language-code]
# gibbrish makeword [language-code]
# codes are in ISO 639-1



#get text

#clean text

#get wordlist
def get_wordlist(clean_text):
    return clean_text.split(" ")

#make Xgrams(wordlist, x)
    


def add_word_to_xgrams(xgrams, x, word):
    padding = x-1
    padded_word = " "*padding+ word + " "*padding

    for i in range( len(word)+padding ):
        gram = padded_word[i:i+x]
        print gram
        
        gram = list(gram)
        loc_gram = map(convert_char_to_int, gram)
        #for g in gram:
        #    g = convert_char_to_int(g)
        print loc_gram

        change_nested_element(loc_gram, xgrams, lambda x: x+1)

    return xgrams

#takes an n-length array [a, b, c]
#and an n-nested array
#changes the element at array[a][b][c]
#nesting must be >= length of loc
#all elements of loc must be < length of nested arrays
#funct is a function from x -> y
def change_nested_element(loc, nested, funct):
    if len(loc) == 1 :
        nested[loc[0]] = funct(nested[loc[0]])
        return nested[loc[0]]
    else:
        return change_nested_element(loc[1:], nested[loc[0]], funct)


def x_nested_array(nesting, length):
    if nesting == 1:
        return [0] * length
    else:
        return [x_nested_array(nesting-1, length) for x in range(length)]


def convert_char_to_int(c):
    if c == " ":
        return 0
    if c in string.lowercase:
        return ord(c) - 96
    else:
        print "invalid char : " + c + " " + ord(c)

def convert_int_to_char(i):
    if i == 0 :
        return " "
        #if 96 <= i <= 122 :
    else:
        return chr(i+96)
    #else:
    #    print "invalid int: " + str(i) + " " + chr(i)





#generate string
def generate_string(xgrams, x):
    padding = x-1
    string = " "*padding

    while True:
        string = add_likely_char(string, xgrams, x)
        if string[-1*padding:] == " "*padding: #add m more
            break
    return string.strip()


def add_likely_char(string, xgrams, x):
    padding = x-1
    #print "adding char to : \"" + string + "\""
    loc_string = map(convert_char_to_int, string[-1*padding:])
    #print loc_string
    probabilities = change_nested_element(loc_string, xgrams, lambda x: x)

    #print probabilities

    index = choose_random_index(probabilities)
    #print "index " + str(index)
    char = convert_int_to_char(index)
    #print "char " + char

    string += char
    #print string
    return string


#takes a list of numbers [a,b,c,d]
#returns the index of one of those numbers
#with a probability number/list_sum
def choose_random_index(probabilities):
    #best = max(probabilities)
    #print "best " + str(best) #TODO randomness
    #index = probabilities.index(best)
    #return index
    list_sum = sum(probabilities)
    
    if list_sum == 0 : #if we've never seen this ngram before
        return random.randrange(0, len(probabilities))
    #is this what we want to do here?
    #or should we try to avoid this situation?

    height = random.randrange(0, list_sum)
    climb = 0
    for i in range(len(probabilities)):
        if climb >= height :
            return i
        else:
            climb += probabilities[i]
        

#tests
def tests():
    pprint.pprint( convert_char_to_int(" ") )
    pprint.pprint( convert_char_to_int("a") )
    pprint.pprint( convert_char_to_int("z") )

    print( x_nested_array(3, 2) )
    print( x_nested_array(2, 3) )

    address = "four score and seven years ago our fathers brought forth on this continent a new nation conceived in liberty and dedicated to the proposition that all men are created equal now we are engaged in a great civil war testing whether that nation or any nation so conceived and so dedicated can long endure we are met on a great battle field of that war we have come to dedicate a portion of that field as a final resting place for those who here gave their lives that that nation might live it is altogether fitting and proper that we should do this but in a larger sense we can not dedicate we can not consecrate we can not hallow this ground the brave men living and dead who struggled here have consecrated it far above our poor power to add or detract the world will little note nor long remember what we say here but it can never forget what they did here it is for us the living rather to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced it is rather for us to be here dedicated to the great task remaining before us that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion that we here highly resolve that these dead shall not have died in vain that this nation under god shall have a new birth of freedom and that government of the people by the people for the people shall not perish from the earth"
    address_words = get_wordlist(address)
    print address_words

    bigrams = x_nested_array(2, 27)
    for word in address_words:
        add_word_to_xgrams(bigrams, 2, word)
    print bigrams

    for i in range(10):
        print generate_string(bigrams, 2)


#main
tests()
