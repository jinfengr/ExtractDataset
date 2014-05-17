'''
Created on Mar 28, 2014

@author: jeffy
'''
import urllib2
import json
import urllib
import csv
from bs4 import BeautifulSoup

urls = {
    2011:'http://dl.acm.org/citation.cfm?id=2020408&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2010:'http://dl.acm.org/citation.cfm?id=1835804&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2009:'http://dl.acm.org/citation.cfm?id=1557019&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2008:'http://dl.acm.org/citation.cfm?id=1401890&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2007:'http://dl.acm.org/citation.cfm?id=1281192&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2006:'http://dl.acm.org/citation.cfm?id=1150402&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2005:'http://dl.acm.org/citation.cfm?id=1081870&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2004:'http://dl.acm.org/citation.cfm?id=1014052&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2003:'http://dl.acm.org/citation.cfm?id=956750&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2002:'http://dl.acm.org/citation.cfm?id=775047&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2001:'http://dl.acm.org/citation.cfm?id=502512&picked=prox&CFID=452889752&CFTOKEN=54870889',
    2000:'http://dl.acm.org/citation.cfm?id=347090&picked=prox&CFID=452889752&CFTOKEN=54870889'  }

def downByYear(year):
    seed_url = urls[year]
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib2.Request(seed_url, headers=hdr)
    soup = BeautifulSoup(urllib2.urlopen(req).read())
    href_tags = soup.findAll("a",title="FullText PDF")
    pdf_id = 0
    dest_dir = "../data/KDD"+str(year%100)
    for tag in href_tags:
        pdf_id += 1
        urllib.urlretrieve(tag['href'],"../data/dest_dir/"+str(pdf_id)+".pdf")

downByYear(2011)