#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from textblob import TextBlob

ALPHABET = 'qüertyuiopöğasdfghjklıəzxcvbnmçş'

def normalize(text):
    letters = []
    for l in text.lower():
        if l in ALPHABET:
            letters.append(l)
        elif l in ".?!":
            letters.append(' ')
            letters.append('.')
            letters.append(' ')
        else:
            letters.append(' ')
    text = ''.join(letters)
    text = ' '.join(text.split())
    return text

assert normalize('AsD?! d!@$%^^ ee   ') == 'asd . . d . ee'

def loadText(fname):
    with codecs.open(fname, 'r', 'utf-8') as f:
        data = f.read()
        return normalize(data).split()

def loadAlphabet(fname):
    global ALPHABET
    with codecs.open(fname, 'r', 'utf-8') as f:
        data = f.read()
        data = data.strip().lower()
        ALPHABET = data

def generateSentences(words):
    sentences = []
    currSent = []
    for w in words:
        if w == '.':
            if currSent:
                sentences.append(currSent)
            currSent = []
        else:
            currSent.append(w)
    if currSent:
        sentences.append(currSent)
    return sentences


       
def fixed_words(original, edited, correct):
    original_text = original
    edited_text = edited
    correct_text = correct
    original_words = TextBlob(original_text).words
    edited_sentence_words = TextBlob(edited_text).words
    correct_words =  TextBlob(correct_text).words
    corrected = 0 
    min_len = min(len(original_words), len(edited_sentence_words), len(correct_words))

    for i in range(min_len):
        if original_words[i] != correct_words[i]:
            if edited_sentence_words[i] != original_words[i] and edited_sentence_words[i] == correct_words[i]:
                corrected += 1
    return corrected
    
def broken_words(original, edited,correct):       
    original_text = original
    edited_text = edited
    correct_text = correct
    original_words = TextBlob(original_text).words
    edited_sentence_words = TextBlob(edited_text).words
    correct_words =  TextBlob(correct_text).words
    incorrect = 0
    min_len = min(len(original_words),len(edited_sentence_words),len(correct_words))

    for i in range(min_len):
        if original_words[i] == correct_words[i]:       
            if edited_sentence_words[i] != original_words[i]:  
                incorrect += 1                                  

    result = incorrect

    return result

def wrong_words(edited, correct):  
        incorrect = 0 
        edited_text = edited
        correct_text = correct
        edited_sentence_words = TextBlob(edited_text).words
        correct_words =  TextBlob(correct_text).words
        min_len = min(len(edited_sentence_words),
                      len(correct_words))

        for i in range(min_len):
            if edited_sentence_words[i] != correct_words[i]:
                incorrect += 1
        result = incorrect
        return result

  


