'''
Created on Apr 29, 2014

@author: jeffy
'''
import re

data_dir = '../../data/training_data/'

vocabulory = {}
count = 0
numberexp = re.compile(' [-0-9][0-9,.]* ')
itemexp = re.compile('\( [a-g] \)')
f_train = open(data_dir+'sentences_train.dat','w')
f_test = open(data_dir+'sentences_test.dat','w')
f_seq = open(data_dir+'sentences_seq.dat','w')
linecount = 0
wordcount = 0
with open(data_dir+'sentences.dat') as f:
    for line in f:
        file_name = line.split('@')[0]
        if file_name == 'KDD9':
            debug = True
        #line = line.split('@')[1]
        linecount += 1
        for i in range(2):
            if numberexp.search(line):
                numbers = numberexp.findall(line)
                for number in numbers:
                    line = line.replace(number,' #number# ')
        if itemexp.search(line):
            items = itemexp.findall(line)
            for item in items:
                line = line.replace(item,'#itemlist#')
        words = line.rstrip('\n').split(' ')

        if linecount <= 270:
            #f_seq.write('\n')
            wordcount += len(words)
            f_train.write(line) 
        else:
            f_test.write(line)
print wordcount
f_seq.close()
f_train.close()
f_test.close()

