'''
Created on May 1, 2014

@author: jeffy
'''
import re
import nltk
import BuildWordFeatures

data_dir = '../../data/training_data/'
dataset_list = BuildWordFeatures.LoadDataset(data_dir)
symbol_exp = re.compile('[,.:\(\)?!]')

def GetTags(file, option, figure_list):
    f = open(data_dir+'CRF_'+option+'.dat','w')
    for line in file:
        file_name = line.split('@')[0]
        fig_sentences = figure_list[file_name]
        datasets = dataset_list[file_name]
        newline = line.split('@')[1].rstrip('\n')
        words = newline.split(' ')
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
                    
            capitolTag = BuildWordFeatures.CapitolForm(words[i])
            mixedTag = BuildWordFeatures.MixedForm(words[i])
            dashTag = BuildWordFeatures.HasDash(words[i])
            figureTag = BuildWordFeatures.InFigure(fig_sentences, words[i])
            if i==0: 
                beginTag = 1 
            else:
                beginTag = 0
            
            if flag == True:
                if index == 0:
                    chunkingTag = 'B-DATASET'
                else:
                    chunkingTag = 'I-DATASET'
            else:
                if symbol_exp.search(word):
                    chunkingTag = 'SYMBOL'
                elif word in ['the','The','a']:
                    chunkingTag = 'THE'
                elif word in ['dataset', 'datasets', 'data']:
                    chunkingTag = 'DATA' 
                else:
                    chunkingTag = 'OTHER'
            f.write(words[i]+' '+posTag+' '+str(beginTag)+' '+str(capitolTag)+' '+str(mixedTag)+' '+str(dashTag)+' '+str(figureTag)+' '+chunkingTag+'\n')
        f.write('\n')

if __name__ == '__main__':  
    figure_list = BuildWordFeatures.LoadFigureSentence(data_dir)                  
    f_train = open(data_dir+'sentences_train.dat')
    f_test = open(data_dir+'sentences_test.dat')
    GetTags(f_train,'train',figure_list)
    GetTags(f_test,'test',figure_list)

    