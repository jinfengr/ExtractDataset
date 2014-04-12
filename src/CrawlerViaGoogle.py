'''
Created on Apr 11, 2014

@author: jeffy
'''
import urllib
import urllib2
import re
import time,random
from bs4 import BeautifulSoup
from pygoogle import pygoogle
from xgoogle.search import GoogleSearch, SearchError

paper_dir = '../data/training_data/'
seed_url = 'http://kdd2012.sigkdd.org/papers.shtml'
soup = BeautifulSoup(urllib2.urlopen(seed_url).read())
papers_tags = soup.findAll('p')
pattern = re.compile('Paper')
count = 0
last_count = 48
for paper in papers_tags:
    if pattern.match(paper.getText()):
        count = count + 1
        if count <= last_count: 
            continue
        title = paper.getText().split('\n')[1].strip()
        try:
            gs = pygoogle(title[7:])
            gs.pages = 1
            wt = random.uniform(10,31)
            urls = gs.get_urls()
            for url in urls:
                if re.compile('.*pdf.*').match(url):
                    print url, count
                    urllib.urlretrieve(url, paper_dir+'KDD'+str(count)+'.pdf')
                    time.sleep(wt)
                    break
        except Exception:
            print "Search failed: %s" % title