'''
Created on Mar 28, 2014

@author: jeffy
'''
import urllib2
import json
import urllib
import csv
from bs4 import BeautifulSoup

def downByMonth(domain, year, month):
    print year+month
    base_url = "http://arxiv.org"
    seed_url = base_url + "/list/"+domain+"/"+year+month
    soup = BeautifulSoup(urllib2.urlopen(seed_url).read())
    all_tag = soup.find("a", text="all")
    if all_tag != None:
        all_url = base_url + all_tag['href']
        soup = BeautifulSoup(urllib2.urlopen(all_url).read())
    docs = soup.find_all("a",title="Download PDF")
    for doc in docs:
        pdf_url = doc['href']
        pdf_id = pdf_url[5:]
        urllib.urlretrieve(base_url+pdf_url, "../data/"+pdf_id+".pdf")

def downByYear(domain, year):
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    [downByMonth(domain, year, month) for month in months]

downByYear("cs.IR","13")