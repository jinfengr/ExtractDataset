import os
import re
from collections import defaultdict

paper_dir = '../data/'

dataset_name_count = defaultdict(int)

regexp = 'the (.{1,50}?) dataset'
pattern = re.compile(regexp)

files = os.listdir(paper_dir)
for f in files:
    if f.endswith('_refined.txt'):
        infp = open(paper_dir+f,'rb')
        for line in infp:
            names = pattern.findall(line.lower())
            for name in names:
                dataset_name_count[name] += 1
        infp.close()
        
for name in sorted(dataset_name_count, key=dataset_name_count.get, reverse=True):
    print name, dataset_name_count[name]