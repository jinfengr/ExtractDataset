'''
Created on Apr 7, 2014

@author: jeffy
'''
import os
import re
import nltk
from stemming.porter2 import stem
from collections import defaultdict


ExpFlags = [stem('experiment'),stem('result'),stem('evaluation'),stem('analysis'),stem('experimental')]
def ExpSectionFilter(line):
    words = line.split()
    regexp = '[1-9].?$'
    pattern = re.compile(regexp)
    if pattern.match(words[0]) and len(words)<=5:
        for word in words:
            if stem(word) in ExpFlags:
                return True
    return False

def VerifySection(line):
    words = line.split()
    regexp = '[1-9].?$'
    regexp2 = '^[A-Z]'
    if len(words)<=5 and len(words)>1 and re.compile(regexp).match(words[0]) and re.compile(regexp2).match(words[1]) :
        return True
    return False

def FindDataset(line):
    regexp = '.*(dataset|data set).*'
    pattern = re.compile(regexp)
    if pattern.match(line):
        return True
    return False

def ExtractFigure(line):
    regexp = 'figure|Figure|table|Table'
    pattern = re.compile(regexp)
    if pattern.search(line):
        return True
    return False

paper_dir = '../data/training_data/'
files = os.listdir(paper_dir)
for f in files:
    if f.endswith('_refined.txt'):
        print f+" open"
        infp = open(paper_dir+f,'rb')
        outfp = file(paper_dir+f.replace('refined','dataset'), 'w')
        figurefp = file(paper_dir+f.replace('refined','figure'), 'w')
        expSectionNum = -1
        flag = False
        for line in infp:
            # Experiment Section
            if line[0].isdigit() and ExpSectionFilter(line.lower()): 
                print line
                expSectionNum = int(line[0])
                flag = True
            # Next Section
            if line[0].isdigit() and int(line[0]) == expSectionNum + 1 and VerifySection(line):
                expSectionNum = -1
                print line
            # Find Dataset Line in Experiment Section
            if flag==True and expSectionNum!= -1 and FindDataset(line):
                outfp.write(line + '\n')
            for sentence in line.split('.'):
                if ExtractFigure(sentence):
                    figurefp.write(sentence + '\n')
        # No Experiment Section
        if flag==False:
            infp = open(paper_dir+f,'rb')
            for line in infp:
                if FindDataset(line):
                    outfp.write(line + '\n')
        outfp.close()
        figurefp.close()
        print f+" close"
                
                    