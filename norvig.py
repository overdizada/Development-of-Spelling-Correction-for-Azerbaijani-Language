#https://norvig.com/spell-correct.html
import re
from collections import Counter
import pickle
import pandas as pd
from nltk.tokenize import word_tokenize
from textblob import TextBlob

l ='QÜERTYUİOPÖĞASDFGHJKLIƏZXCVBNMÇŞqüertyuiopöğasdfghjklıəzxcvbnmçş'

def saxta(txt):
    for t in txt:
        if t not in l:
            return True
    return False

def init(fileName='save'):
    global WORDS, words2
    WORDS = pd.read_pickle(fileName+'_1.pickle') 
    words2=pd.read_pickle(fileName+'_2.pickle')

    exclude = True
    if exclude == True:
        extra=['gözəldi','sirrimi']
        manual=['quot','yaxsı','melli','muallim','yasi','gozaldi']
        saxtaw = [word for word, occurrences in WORDS.items() if saxta(word) == True]
        rare = [word for word, occurrences in WORDS.items() if occurrences <= 80 and len(word) < 7]
        rare = rare+ [word for word, occurrences in WORDS.items() if occurrences <= 50]

        silmek=saxtaw+rare+manual
        
        for k in (silmek):
            try:
                del WORDS[k]
            except KeyError:
                pass
        for w in (extra):
            WORDS[w]=100
init()


def lower(text):
    bg='QÜERTYUİOPÖĞASDFGHJKLIƏZXCVBNMÇŞ'
    sm="qüertyuiopöğasdfghjklıəzxcvbnmçş"
    lb={}
    for i in range(len(bg)):
        lb[bg[i]]=sm[i]
        
    for key in lb.keys():
        text = text.replace(key, lb[key])
        
    return text

def words(text): return re.findall(r'\w+', lower(text))


        
def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N+0.0000000000001

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word, closest=True): 
    "Generate possible spelling corrections for word."
    if(closest):
        return (known([word]) or known(edits1(word)) or (known(edits2(word)))   or [word])
    return (known([word]) or known(edits1(word)).union(known(edits2(word)))   or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcçdeəfgğhxıijkqlmnoöprsştuüvyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

from nltk import ngrams

def train(arr, fileName='save'):
    WORDS = Counter()
    words2= Counter()
    for txt in arr:
        print(txt)
        metn=open(txt, encoding='utf-8').read()
        t =  Counter(words(metn))
        twograms = list(ngrams(word_tokenize(lower(metn)), 2))
        tt=Counter(twograms)
        WORDS.update(t)
        words2.update(tt)
    with open(fileName+'_1.pickle', 'wb') as f:
        pickle.dump(WORDS, f)
    with open(fileName+'_2.pickle', 'wb') as f:
        pickle.dump(words2, f)


def corr_sent(cumle):
    cvb=[]
    for w in word_tokenize(cumle):
        cvb.append(correction(w))
    cvb=' '.join(cvb)
    return (cvb)


def calc_p(a,b,ab):
    return a*b*ab

def duzelt(cumle,closest=True):
    #metn basliyan kimi ., sil sonra ver functiona
    res=[]

    tokens=word_tokenize(lower(cumle))
    for i in range(0,len(tokens)-1):
        fl=False

        for ch in tokens[i]:
            if ch not in l:
                res.append(tokens[i])
                fl=True
                break
        if(fl):
            continue
        cond1=list(candidates(tokens[i],closest))
        cond2=list(candidates(tokens[i+1],closest))
        m_prob=-1
        for ii in range(len(cond1)):
            for iii in range(len(cond2)):

                p_c1_c2=calc_p(P2(cond1[ii], cond2[iii]) , P(cond1[ii]),P(cond2[iii]))
                if(p_c1_c2>m_prob):
                    m_prob=p_c1_c2
                    c1=cond1[ii]
        res.append(c1)

    cond1=list(candidates(tokens[len(tokens)-2],closest))
    cond2=list(candidates(tokens[len(tokens)-1],closest))
    m_prob=-1
    for ii in range(len(cond1)):
        for iii in range(len(cond2)):
            p_c1_c2=calc_p(P2(cond1[ii], cond2[iii]) , P(cond1[ii]),P(cond2[iii]))
            if(p_c1_c2>m_prob):
                m_prob=p_c1_c2
                c2=cond2[iii]

    res.append(c2)
    return ' '.join(res)


def P2(w1,w2,N=sum(words2.values())):
     return max(words2[(w1,w2)],words2[(w2,w1)])/N+0.0000000000001
