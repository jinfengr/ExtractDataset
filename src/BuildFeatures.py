'''
Created on Apr 13, 2014

@author: jeffy
'''
import os, re
import numpy
from collections import defaultdict

def ExtractFeatures(paragraph, dataset,features):
    sentences = paragraph.split(' . ')
    for s in sentences:
        if s.find(dataset)>=0:
            words = s.split(' ')
            for word in words:
                if keywords.has_key(word):
                    dist = abs(words.index(word) - words.index(dataset))
                    index = keywords.keys().index(word)
                    features[dataset] = defaultdict(int)
                    features[dataset][2*index] += 1
                    features[dataset][2*index+1] += dist
    
data_dir = '../data/training_data/'

COUNT = 1000
count = 0
keywords = {}
with open(data_dir+'keywords.txt') as f:
    for line in f:
        if count <= COUNT:
            tokens = line.rstrip('\n').split(' ')
            keywords[tokens[0]] = tokens[1]
            count += 1

datasets = {}
with open(data_dir+'dataset.txt') as f:
    for line in f:
        sets = line.rstrip('\n').split(',')
        datasets[sets[0]]=sets[1:]

files = os.listdir(data_dir)
features = {}
for f in files:
    if f.endswith('_dataset.txt'):
        infp = open(data_dir+f,'rb')
        data = datasets[f[0:-12]]
        for para in infp:
            [ExtractFeatures(para,dataset,features) for dataset in data]
                    
                    
                
                