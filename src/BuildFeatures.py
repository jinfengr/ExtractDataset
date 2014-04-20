'''
Created on Apr 13, 2014

@author: jeffy
'''
import os, re
import numpy
from collections import defaultdict

def ExtractFeatures(paragraph, dataset,features):
    sentences = paragraph.split(' . ')
    for i in range(len(sentences)):
        s = sentences[i]
        nexts = ""
        if i < len(sentences)-1:
            nexts = sentences[i+1]
        words = s.split(' ')
        names = dataset.split(' ')
        flag = True
        for name in names:
            if name not in words:
                flag = False
        if flag == True:
            words.extend(nexts.split(' '))
            for word in words:
                if keywords.has_key(word):
                    dist = abs(words.index(word) - words.index(names[0]))
                    index = keywords.keys().index(word)
                    features[dataset][2*index] += 1
                    features[dataset][2*index+1] += dist
            flag = False
                

def SaveFeatures(features):
    f = open(data_dir+"features.dat","w")
    for dataset in features:
        f.write(dataset+":")
        for index in range(COUNT):
            freq = features[dataset][2*index]
            if freq==0:
                dist = 0
            else:
                dist = features[dataset][2*index+1]/freq
            f.write(str(freq) +","+ str(dist)+",")
        f.write("\n")
    f.close()
         
data_dir = '../data/training_data/'

COUNT = 500
count = 0
keywords = {}
with open(data_dir+'keywords.dat') as f:
    for line in f:
        if count <= COUNT:
            tokens = line.rstrip('\n').split(' ')
            keywords[tokens[0]] = tokens[1]
            count += 1

datasets = {}
features = {}
with open(data_dir+'dataset.dat') as f:
    for line in f:
        sets = line.rstrip('\n').split(',')
        datasets[sets[0]]=sets[1:]

files = os.listdir(data_dir)
for f in files:
    if f.endswith('_dataset.txt'):
        infp = open(data_dir+f,'rb')
        data = datasets[f[0:-12]]
        for dataset in data:
                features[dataset] = defaultdict(int)
        for para in infp:
            [ExtractFeatures(para,dataset,features) for dataset in data]
                    
SaveFeatures(features)                    
                
                