'''
Created on Apr 10, 2014

@author: jeffy
'''
import os
import re
from stemming.porter2 import stem
from nltk.tokenize import RegexpTokenizer

data_dir = '../data/training_data/'

words_freq = {}
files = os.listdir(data_dir)
tokenizer = RegexpTokenizer("[a-zA-Z-]+", flags=re.UNICODE)
for f in files:
    if f.endswith('_dataset.txt'):
        infp = open(data_dir+f,'rb')
        for line in infp:
            tokens = tokenizer.tokenize(line.encode('UTF_8'))
            tokens = [stem(token.lower()) for token in tokens]
            for word in tokens:
                if words_freq.has_key(word):
                    words_freq[word] += 1
                else:
                    words_freq[word] = 1

words_freq = sorted(words_freq.items(),key=lambda x: x[1], reverse = True)
outfp = file(data_dir+'keywords.txt','w')
for word in words_freq:
    outfp.write(word[0]+' '+str(word[1])+'\n')
outfp.close()