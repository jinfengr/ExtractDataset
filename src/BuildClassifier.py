'''
Created on Apr 22, 2014

@author: jeffy
'''
import os,re
from collections import defaultdict
from sklearn import svm
from nltk.tokenize import RegexpTokenizer

train_data_dir = '../data/training_data/'
test_data_dir = '../data/testing_data/'

def LoadFeatures(opt,X,Y):
    with open(train_data_dir+'features_'+opt+'.dat') as f:
        for line in f:
            feature_str = line.rstrip('\n').split(':')[1]
            features = feature_str.split(',')
            features = [int(feature) for feature in features if feature != '']
            X.append(features)
            if opt == 'pos':
                Y.append(1)
            else:
                Y.append(0)

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

def FindCandidates(paragraph, candidate):
    sentences = paragraph.split(' . ')
    for i in range(len(sentences)):
        s = sentences[i]
        names = pattern.findall(s)
        for name in names:
            if not candidate.has_key(name):
                candidate[name] = defaultdict(int)
            nexts = ""
            if i < len(sentences)-1:
                nexts = sentences[i+1]
            words = tokenizer.tokenize(s)
            words.extend(tokenizer.tokenize(nexts))
            for word in words:
                if keywords.has_key(word):
                    dist = abs(words.index(word) - words.index(name[0]))
                    index = keywords.keys().index(word)
                    candidate[name][2*index] += 1
                    candidate[name][2*index+1] += dist    

COUNT = 200
keywords = LoadKeywords()

X=[]
Y=[]
LoadFeatures('pos',X,Y)
LoadFeatures('neg',X,Y)        
clf = svm.SVC()
clf.fit(X,Y)

regexp = '(The|the) (.{1,30}?) (dataset|data)'
pattern = re.compile(regexp)
tokenizer = RegexpTokenizer("[a-zA-Z-]+", flags=re.UNICODE)

Candidates = []
Candidates_key = []
files = os.listdir(test_data_dir)
for f in files:
    if f.endswith('_dataset.txt'):
        candidate = {} # candidate datasets in a paper
        infp = open(test_data_dir+f,'rb')
        [FindCandidates(paragraph, candidate) for paragraph in infp]
        for key in candidate:
            instance = []
            for i in range(COUNT):
                instance.append(candidate[key][2*i])
                instance.append(candidate[key][2*i+1])
            Candidates.append(instance)    
            newkey = f.split('_')[0]+','+key[1]
            Candidates_key.append(newkey)
            
results = clf.predict(Candidates)    

f = open('../data/results.dat','w')
for i in range(len(results)):
    f.write(Candidates_key[i]+':'+str(results[i])+'\n')
f.close()                    
        