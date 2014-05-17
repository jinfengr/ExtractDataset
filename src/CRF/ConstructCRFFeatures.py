'''
Created on May 1, 2014

@author: jeffy
'''
import re
import nltk
from nltk.tokenize import RegexpTokenizer
import BuildWordFeatures

data_dir = '../../data/KDD11/'
dataset_list = BuildWordFeatures.LoadDataset(data_dir)
symbol_exp = re.compile('[,.:\(\)?!]')

WORD_FREQ = 3
BEGIN_POS = 3
def GetTags(file, option, figure_list):
    f = open(data_dir+'CRF_'+option+'.dat','w')
    # Preprocessing 
    sentences = {}
    for line in file:
        file_name = line.split('@')[0]
        newline = line.split('@')[1].rstrip('\n')
        if sentences.has_key(file_name):
            sentences[file_name]['LINES'].append(newline)
        else:
            sentences[file_name] = {'LINES':[],'WORDS':{}}
            sentences[file_name]['LINES'].append(newline)
        words = newline.split(' ')
        for word in words:
            if sentences[file_name]['WORDS'].has_key(word):
                sentences[file_name]['WORDS'][word] += 1
            else:
                sentences[file_name]['WORDS'][word] = 1
    # Get Tags Info
    for file_name in sentences:
        fig_sentences = figure_list[file_name]
        datasets = dataset_list[file_name]
        for line in sentences[file_name]['LINES']:
            words = line.split(' ')
            if '' in words: words.remove('')
            tags = nltk.pos_tag(words)
            chunkingTags = []
            for i in range(len(words)):
                word = words[i]
                posTag = tags[i][1]
                flag = False
                for dataset in datasets:
                    terms = dataset.split(' ')
                    for term in terms:
                        regexp = re.compile(term+'[0-9]?')
                        if regexp.match(word):
                            words[i] = term
                            index = terms.index(term)
                            flag = True
                            break
                        
                beginTag = 1 if i<=BEGIN_POS else 0     
                capitolTag = BuildWordFeatures.CapitolForm(words[i])
                mixedTag = BuildWordFeatures.MixedForm(words[i])
                dashTag = BuildWordFeatures.HasDash(words[i])
                figureTag = BuildWordFeatures.InFigure(fig_sentences, words[i])
                freqTag = 1 if sentences[file_name]['WORDS'][word] >= WORD_FREQ else 0
                
                
                if flag == True:
                    if index == 0:
                        chunkingTag = 'B-DATASET'
                    else:
                        chunkingTag = 'I-DATASET'
                else:
                    if symbol_exp.search(word):
                        chunkingTag = 'SYMBOL'
                    elif word in ['the','The','a','an']:
                        chunkingTag = 'THE'
                    elif word in ['dataset', 'datasets', 'data','corpus','corpora','Dataset','Datasets']:
                        chunkingTag = 'DATA' 
                    elif word == '#ITEMLIST#':
                        chunkingTag = 'ITEMLIST'
                    else:
                        chunkingTag = 'OTHER'
                f.write(words[i]+' '+posTag+' '+str(beginTag)+' '+str(capitolTag)+
                        ' '+str(mixedTag)+' '+str(dashTag)+' '+
                        str(figureTag)+' '+str(freqTag)+' '+chunkingTag+'\n')
            f.write('\n')

if __name__ == '__main__':  
    figure_list = BuildWordFeatures.LoadFigureSentence(data_dir)                  
    #f_train = open(data_dir+'sentences_train.dat')
    f_test = open(data_dir+'sentences.dat')
    #GetTags(f_train,'train',figure_list)
    GetTags(f_test,'test',figure_list)

    