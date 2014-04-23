'''
Created on Apr 13, 2014

@author: jeffy
'''
import os, re
from collections import defaultdict

def ExtractPosFeatures(paragraph, dataset, features):
    name_term = dataset.split(' ')
    sentences = paragraph.split(' . ')
    for i in range(len(sentences)):
        s = sentences[i]
        nexts = ""
        if i < len(sentences)-1:
            nexts = sentences[i+1]
        words = s.split(' ')
        flag = True
        for name_word in name_term:
            if name_word not in words:
                flag = False
        if flag == True:
            words.extend(nexts.split(' '))
            for word in words:
                if keywords.has_key(word):
                    dist = abs(words.index(word) - words.index(name_term[0]))
                    index = keywords.keys().index(word)
                    features[dataset][2*index] += 1
                    features[dataset][2*index+1] += dist
            
def ExtractNegFeatures(paragraph, datasets, features):
    regexp = '(The|the) (.{1,30}?) (dataset|data|set)'
    pattern = re.compile(regexp)
    sentences = paragraph.split(' . ')
    for i in range(len(sentences)):
        s = sentences[i]
        names = pattern.findall(s)
        for name in names:
            if name[1] not in datasets:
                name_index = len(s[0:s.index(name[1])].strip().split(' '))
                nexts = ""
                if i < len(sentences)-1:
                    nexts = sentences[i+1]
                words = s.split(' ')
                words.extend(nexts.split(' '))
                for word in words:
                    if keywords.has_key(word):
                        dist = abs(words.index(word) - name_index)
                        index = keywords.keys().index(word)
                        if not features.has_key(name[1]):
                            features[name[1]] = defaultdict(int)
                        features[name[1]][2*index] += 1
                        features[name[1]][2*index+1] += dist
                

def SaveFeatures(features,pn):
    f = open(data_dir+"features_"+pn+".dat","w")
    for dataset in features:
        if dataset != "":
            f.write(dataset.replace(':',' ')+":")
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

def LoadKeywords():
    count = 0
    keywords = {}
    with open('../data/training_data/keywords.dat') as f:
        for line in f:
            if count <= COUNT:
                tokens = line.rstrip('\n').split(' ')
                keywords[tokens[0]] = tokens[1]
                count += 1
    return keywords

COUNT = 200
keywords = LoadKeywords()

dataset_list = {}
features_pos = {}
features_neg = defaultdict(defaultdict)

with open(data_dir+'dataset.dat') as f:
    for line in f:
        sets = line.rstrip('\n').split(',')
        if sets[1:]!=["NONE"] :
            dataset_list[sets[0]]=sets[1:]

files = os.listdir(data_dir)
for f in files:
    if f.endswith('_dataset.txt'):
        infp = open(data_dir+f,'rb')
        if dataset_list.has_key(f[0:-12]):
            datasets = dataset_list[f[0:-12]]
        for dataset in datasets:
                features_pos[dataset] = defaultdict(int)
        for para in infp:
            [ExtractPosFeatures(para,dataset,features_pos) for dataset in datasets]
            ExtractNegFeatures(para,datasets,features_neg)
                    
SaveFeatures(features_pos,"pos")
SaveFeatures(features_neg,"neg")                 
                
                