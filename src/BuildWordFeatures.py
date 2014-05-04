'''
Created on Apr 13, 2014

@author: jeffy
'''
import os, re, math
from collections import defaultdict


def ContainTokens(sentence, tokens):
    words = sentence.split(' ')
    for token in tokens:
        pattern = re.compile(token)
        if pattern.search(sentence)!=None:
            return 1
    return 0

def DistanceToTokens(sentence, dataset, tokens):
    min_dist = 100
    if ContainTokens(sentence, tokens) == 0:
        return min_dist
    words = sentence.split(' ')
    term = dataset.split(' ')[0]
    term_index = words.index(term)
    for token in tokens:
        indices = [i for i, x in enumerate(words) if x.startswith(token)]
        for the_index in indices:
            if abs(min_dist) > abs(term_index - the_index):
                min_dist = term_index - the_index
    return min_dist
    
def CapitolForm(dataset):
    regexp = '^[A-Z]'
    pattern = re.compile(regexp)
    for name_term in dataset.split(' '):
        if pattern.search(name_term) == None:
            return 0
    return 1

def MixedForm(dataset):
    pattern = re.compile('^[a-zA-Z ]+$')
    if pattern.match(dataset) != None:
        return 0
    return 1

def HasDash(dataset):
    pattern = re.compile('-')
    if pattern.search(dataset) != None:
        return 1
    return 0
    
def Index(sentence, dataset):
    first_term = dataset.split(' ')[0]
    return sentence.split(' ').index(first_term)

def LengthOfDataset(dataset):
    return len(dataset)

def WordsOfDataset(dataset):
    pattern = re.compile(' ')
    spaces = pattern.findall(dataset)
    #pattern = re.compile('#')
    #chars = pattern.findall(dataset)
    return len(spaces)+1

def ContainREF(sentence):
    pattern = re.compile('#REF#')
    if pattern.search(sentence) != None:
        return 1
    return 0

def InFigure(fig_sentences, dataset):
    try:
        pattern = re.compile(dataset)
    except Exception as e:
        return 0
    if pattern.search(fig_sentences) != None:
        return 1
    return 0

def ContainNumbers(sentence):
    pattern = re.compile('\d+')
    if pattern.search(sentence) != None:
        return 1
    return 0

def ContainSymbols(sentence):
    pattern = re.compile('\(|\)')
    if pattern.search(sentence) != None:
        return 1
    return 0
    
def ExtractFeatures(paragraph, fig_sentences, file_name, dataset, features):
    feature_capitol = CapitolForm(dataset)
    feature_mixedCase = MixedForm(dataset)
    feature_hasdash = HasDash(dataset)
    feature_length = LengthOfDataset(dataset)
    feature_words = WordsOfDataset(dataset)
    feature_infigure = InFigure(fig_sentences,dataset)
    feature_symbol = 0
    feature_number = 0
    feature_ref = 0
    feature_index = 0
    feature_containThe = 0
    feature_containData = 0
    feature_distThe = 0
    feature_distData = 0
    
    if dataset == 'matrix':
        debug = True
    name_term = dataset.split(' ')
    for sentence in paragraph:
        if ContainSymbols(sentence) == 1:
           feature_symbol = 1
        if ContainNumbers(sentence) == 1:
            feature_number = 1
        if ContainREF(sentence) == 1:
            feature_ref = 1
        if feature_index > Index(sentence, dataset) or feature_index==0:
            feature_index = Index(sentence, dataset)
        if ContainTokens(sentence, ['the','The']) == 1:
            feature_containThe = 1
        if ContainTokens(sentence, ['dataset','data','data set']) == 1:
            feature_containData = 1
        if abs(feature_distThe) > abs(DistanceToTokens(sentence, dataset, ['a','an','the','The'])) or feature_distThe == 0:
            feature_distThe = DistanceToTokens(sentence, dataset, ['a','an','the','The'])
        if abs(feature_distData) > abs(DistanceToTokens(sentence, dataset, ['dataset','data'])) or feature_distData == 0:
            feature_distData = DistanceToTokens(sentence, dataset, ['dataset','data'])
    
    dataset_name = file_name+'@'+dataset
    features[dataset_name] = []
    features[dataset_name].append(feature_capitol)
    features[dataset_name].append(feature_mixedCase)
    features[dataset_name].append(feature_hasdash)
    features[dataset_name].append(feature_length)
    features[dataset_name].append(feature_words)
    features[dataset_name].append(feature_infigure)
    features[dataset_name].append(feature_symbol)
    features[dataset_name].append(feature_number)
    features[dataset_name].append(feature_ref)
    #features[dataset_name].append(feature_index)
    features[dataset_name].append(feature_containThe)
    features[dataset_name].append(feature_containData)
    #features[dataset_name].append(feature_distThe+10)
    #features[dataset_name].append(feature_distData+10)
    
def ExtractNegFeatures(paragraph, fig_sentences, file_name, datasets, features):
    regexp = '(The|the) (.{3,30}?) (dataset|data|set)'
    pattern = re.compile(regexp)
    #regexp2 = '([A-Z][a-z]+) (dataset|data set|data)'
    #pattern2 = re.compile(regexp2)
    names = pattern.findall(para)
    for name in names:
        if name[1] not in datasets:
            if len(name[1].split(' '))>3:
                continue
        windows = getWindow(para, name[1], 5)
        ExtractFeatures(windows, fig_sentences, file_name, name[1], features)
                
def getWindow(para, dataset,window_length):
    words = para.split(' ')
    terms = dataset.split(' ')
    indices = [i for i, x in enumerate(words) if x == terms[0]]
    windows = []
    for index in indices:
        dataset_flag = True
        window = ""
        for pos in range(len(terms)):
            if words[index+pos] != terms[pos]:
                dataset_flag = False
        if dataset_flag == True:
            begin_index = max(0, index-window_length)
            end_index = min(len(words)-1,index+len(terms)+window_length)
            for i in range(begin_index, end_index):
                window += words[i]+' '
            window += words[end_index]
            windows.append(window)
    return windows

def LoadDataset(data_dir):
    CapPattern = re.compile('^[A-Z]')
    dataset_list = {}
    with open(data_dir+'dataset.dat') as f:
        for line in f:
            sets = line.rstrip('\n').split(',')
            file_name = sets[0]
            datasets = []
            for dataset in sets[1:]:
                #new_dataset = ''
                #terms = dataset.split(' ')
                #for index in range(len(terms)-1):
                #    if CapPattern.match(terms[index]) and CapPattern.match(terms[index+1]):
                #        new_dataset += terms[index]+'#'
                #new_dataset += terms[len(terms)-1]
                datasets.append(dataset)
            if sets[1:]!=["NONE"] :
                dataset_list[file_name]=datasets
            else:
                dataset_list[file_name]= []
    return dataset_list

def LoadFigureSentence(data_dir):
    figure_list = {}
    files = os.listdir(data_dir)
    for f in files:
        if f.endswith('_figure.txt'):
            file_name = f.split('_')[0]
            figurefp = open(data_dir+f,'r')
            fig_sentences = figurefp.read()
            figure_list[file_name] = fig_sentences
    return figure_list
    
def SaveFeatures(features,pn):
    f = open(data_dir+"features_"+pn+".dat","w")
    for dataset in features:
        if dataset != "":
            f.write(dataset.replace(':',' ')+":")
            for feature in features[dataset]:
                f.write(str(feature)+',')
            f.write("\n")
    f.close()
         
data_dir = '../data/training_data/'

if __name__ == '__main__':
    
    dataset_list = LoadDataset(data_dir)
    features_pos = {}
    features_neg = {}
    
    
    files = os.listdir(data_dir)
    for f in files:
        if f.endswith('_dataset.txt'):
            file_name = f.split('_')[0]
            infp = open(data_dir+f,'rb')
            figurefp = open(data_dir+f.replace('dataset','figure'),'rb')
            fig_sentences = figurefp.read()
            if dataset_list.has_key(f[0:-12]):
                datasets = dataset_list[f[0:-12]]
            sentences = {}
            for dataset in datasets:
                sentences[dataset] = []
            for para in infp:
                for dataset in datasets:
                    windows = getWindow(para, dataset,5)
                    sentences[dataset].extend(windows) 
                ExtractNegFeatures(para, fig_sentences, file_name, datasets, features_neg)
            for dataset in datasets:
                if sentences[dataset] != []:
                    ExtractFeatures(sentences[dataset], fig_sentences, file_name, dataset, features_pos)   
             
                        
    SaveFeatures(features_pos,"pos")
    SaveFeatures(features_neg,"neg")                 