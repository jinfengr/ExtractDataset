'''
Created on May 7, 2014

@author: jeffy
'''
import os
def rename(dir):
    files = os.listdir(dir)
    os.chdir(dir)
    count = 0
    for f in files:
        if f.endswith('.pdf'):
            count += 1
            os.rename(f, 'KDD'+str(count)+'.pdf')
                
if __name__ == '__main__':
    rename('../../data/KDD11')