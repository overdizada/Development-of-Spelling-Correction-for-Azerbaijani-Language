from norvig import *
import os
from textblob import TextBlob
import typo_model
from utils import generateSentences,loadText
from utils import wrong_words,broken_words,fixed_words


text=open('xeber1.txt',encoding='utf-8').read()

def generateTypos(text):
    return ''.join(list(map(typo_model.generateTypo, text)))

blob = TextBlob(text)
print(len(blob.sentences))

#text=loadText('test.txt')
#print(tt[:1000])

for sentence in blob.sentences:
    correct=str(lower(sentence))
    original=generateTypos(correct)
    while(len(original.split(' '))!=len(correct.split(' '))):
        original=generateTypos(correct)

    edited=duzelt(original)
    '''
    print('original')
    print(original)
    print('edited')
    print(edited)
    print('correct')
    print(correct)
    print(fixed_words(original, edited, correct),broken_words(original, edited,correct),wrong_words(edited, correct))
    break
    '''
    print(len(original.split(' ')),fixed_words(original, edited, correct),broken_words(original, edited,correct),wrong_words(edited, correct))
    
