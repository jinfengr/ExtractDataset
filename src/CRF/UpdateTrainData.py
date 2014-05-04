'''
Created on May 2, 2014

@author: jeffy
'''
import re, operator 
import math
# Insert new train instances from previous CRF predicted results

def NormalizeInstance(instance):
    lines = instance.split('\n')
    for i in range(len(lines)):
        if lines[i].isspace():
            continue
        tags = lines[i].split('\t')
        lines[i] = ''
        for index in range(len(tags)):
            if index == COLUMN -2:
                continue
            elif index == COLUMN -1:
                lines[i] += tags[COLUMN-1].split('/')[0]
            else:
                lines[i] += tags[index]+' '
    newinstance = ''
    for line in lines:
        if line and not line.isspace():
            newinstance += line + '\n'
    return newinstance

data_dir = '../../data/training_data/'
predict_file = open(data_dir+'CRF_predict.dat')
COLUMN = 9
Percentage = 0.5

prob_exp = re.compile('# [0-9.]+\n')
ProbDict = {}
InstDict = {}

contents = predict_file.read()
predict_file.close()
instances = prob_exp.split(contents)
test_instances = []
for instance in instances:
    if not instance or instance.isspace():
        continue
    flag = False
    for line in instance.split('\n'):
        if not line or line.isspace():
            continue
        tags = line.split('\t')
        word = tags[0]
        tagAndProb = tags[COLUMN-1]
        tag = tagAndProb.split('/')[0]
        prob = tagAndProb.split('/')[1]
        if tag == 'B-DATASET':
            flag = True
            if not ProbDict.has_key(word):
                ProbDict[word] = prob
                InstDict[word] = [NormalizeInstance(instance)]
            else:
                ProbDict[word] = max(prob,ProbDict[word])
                InstDict[word].append(NormalizeInstance(instance))
    if flag == False:
        test_instances.append(NormalizeInstance(instance))

f_train = open(data_dir + 'CRF_train.dat','a')
f_test = open(data_dir + 'CRF_test.dat','w')

train_instances = []
sorted_problist = sorted(ProbDict.iteritems(), key=operator.itemgetter(1), reverse = True)
for i in range(len(sorted_problist)):
    if i <= math.ceil((len(sorted_problist)*Percentage)):
        word = sorted_problist[i][0]
        for instance in InstDict[word]:
            if instance not in train_instances:
                train_instances.append(instance)
    else:
        word = sorted_problist[i][0]
        for instance in InstDict[word]:
            if instance not in test_instances:
                test_instances.append(instance)

for instance in train_instances:
    f_train.write(instance+'\n')
for instance in test_instances:
    f_test.write(instance+'\n')

f_train.close()
f_test.close()

            