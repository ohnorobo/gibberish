#!/usr/bin/python

import string, pprint, random, re, os, sys, pickle

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
    for i in range(m):
        print generate_string(ngrams, n)
