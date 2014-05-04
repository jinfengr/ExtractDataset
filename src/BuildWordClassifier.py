'''
Created on Apr 22, 2014

@author: jeffy
'''
import os,re
from collections import defaultdict
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from nltk.tokenize import RegexpTokenizer
import BuildWordFeatures

train_data_dir = '../data/training_data/'
test_data_dir = '../data/testing_data/'

def LoadFeatures(opt,fold,X,Y):
    with open(train_data_dir+'features_'+opt+'.dat') as f:
        for line in f:
            paper = line.rstrip('\n').split('@')[0]
            if not paper.startswith('KDD'+str(fold)):
                feature_str = line.rstrip('\n').split(':')[1]
                features = feature_str.split(',')
                features = [int(feature) for feature in features if feature != '']
                X.append(features)
                if opt == 'pos':
                    Y.append(1)
                else:
                    Y.append(0)

def FindCandidates(paragraph, fig_sentences, file_name, candidate):
    names = pattern.findall(paragraph)
    for name in names:
        if len(name[0].split(' '))>3:
            continue
        if name[0] == 'face':
            debug = True
        if not candidate.has_key(file_name+'@'+name[0]):
            windows = BuildWordFeatures.getWindow(paragraph, name[0], 3)
            BuildWordFeatures.ExtractFeatures(windows, fig_sentences, file_name, name[0], candidate)
    '''CapPattern = re.compile('[A-Z][A-Za-z0-9#-]+')
    names = []
    windows = BuildWordFeatures.getWindow(paragraph, 'dataset', 3)
    windows.extend(BuildWordFeatures.getWindow(paragraph, 'data', 3))
    for window in windows:
        names.extend(CapPattern.findall(window))
    for name in names:
        if not candidate.has_key(name):
            windows = BuildWordFeatures.getWindow(paragraph, name, 3)
            BuildWordFeatures.ExtractFeatures(windows, fig_sentences, file_name, name, candidate)'''
    

regexp = '([a-zA-Z0-9#-]{3,30}) (dataset|data)'
pattern = re.compile(regexp)

dataset_list = BuildWordFeatures.LoadDataset()

FOLD = 4
TP, TN, Total, NumOfDatasets = 0, 0, 0, 0

for fold in range(1, FOLD+1):
    X=[]
    Y=[]
    LoadFeatures('pos',fold,X,Y)
    LoadFeatures('neg',fold,X,Y)        
    #clf = svm.SVC()
    #clf = MultinomialNB()
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(X,Y)
    
    Candidates = []
    Candidates_key = []
    files = os.listdir(train_data_dir)
    for f in files:
        if f.endswith('_dataset.txt') and f.startswith('KDD'+str(fold)):
            candidate = {} # candidate datasets in a paper
            infp = open(train_data_dir+f,'rb')
            file_name = f.split('_')[0]
            figurefp = open(train_data_dir+f.replace('dataset','figure'),'rb')
            fig_sentences = figurefp.read()
            [FindCandidates(paragraph, fig_sentences, file_name, candidate) for paragraph in infp if len(paragraph)>1]
            for key in candidate:
                instance = []
                for feature in candidate[key]:
                    instance.append(feature)
                Candidates.append(instance)    
                Candidates_key.append(key)
    
    predict_results = clf.predict(Candidates)  
    for index in range(len(predict_results)):
        dataset_name = Candidates_key[index].split('@')[1]
        file_name = Candidates_key[index].split('@')[0]
        predict = predict_results[index]
        if predict == 1 and dataset_name in dataset_list[file_name]:
            TP += 1
        if predict ==0 and dataset_name not in dataset_list[file_name]:
            TN += 1
    Total += len(predict_results)
    
    for file_name in dataset_list:
        if file_name.startswith('KDD'+str(fold)):
            NumOfDatasets += len(dataset_list[file_name])
    
    f = open('../data/results.dat','a')
    for i in range(len(predict_results)):
        f.write(Candidates_key[i]+':'+str(predict_results[i])+'    ')
        for feature in Candidates[i]:
            f.write(str(feature)+',')
        f.write('\n')
    f.close()                    

print 'Accuracy:', float((TP+TN))/Total, 'Recall:', float(TP)/NumOfDatasets      
