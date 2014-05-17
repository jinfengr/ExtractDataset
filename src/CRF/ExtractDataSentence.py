'''
Created on Apr 29, 2014

@author: jeffy
'''
import re,os
import BuildWordFeatures;

data_dir = '../../data/KDD11/'
dataset_list = BuildWordFeatures.LoadDataset(data_dir)
dataset_sentence = {}

files = os.listdir(data_dir)
for f in files:
    if f.endswith('_dataset.txt'):
        file_name = f.split('_')[0]
        infp = open(data_dir+f,'rb')
        if not dataset_list.has_key(file_name):
            continue
        datasets = dataset_list[file_name]
        dataset_sentence[file_name] = []
        for para in infp:
            for sentence in para.split(' . '):
                for dataset in datasets:
                    if sentence.find(dataset) != -1 and sentence not in dataset_sentence[file_name]:
                        dataset_sentence[file_name].append(sentence)

f = open(data_dir+'sentences.dat','w')
for file in dataset_sentence:
    for sentence in dataset_sentence[file]:
        length = len(sentence.split(' '))
        if length > 5:
            f.write(file+'@'+sentence.rstrip('\n')+' .\n')
f.close()
        