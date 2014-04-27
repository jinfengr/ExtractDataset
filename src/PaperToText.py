import os
import nltk

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams

from lib.converter import TextConverter
from lib.tokenizer import MyTokenizer

def extractText(infp, outfp):
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(infp)
    # Create a PDF document object that stores the document structure.
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    laparams = LAParams()
    device = TextConverter(rsrcmgr,outfp,laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)

def refineText(infp, outfp):
    stringlist = []
    textline = ""
    size = ""
    for line in infp:
        current = line.strip().replace('  ',' ')
        if current.startswith("<size>"):
            if current != size and size != "":
                for sentence in nltk.sent_tokenize(''.join(stringlist)):
                    for token in MyTokenizer().tokenize(sentence):
                        outfp.write(token+' ')
                outfp.write('\n')
                stringlist = []
                outfp.write('\n')
            stringlist.append(textline)
            size = current
        elif current == '':
            continue
        elif current[-1] == '-':
            textline = current[0:-1]
        else:
            textline = current+' '
    for sentence in nltk.sent_tokenize(''.join(stringlist)):
        for token in MyTokenizer().tokenize(sentence):
            outfp.write(token+' ')
    outfp.write('\n')

paper_dir = '../data/training_data/'

#f = "KDD1.pdf"
#infp = open(paper_dir+f,'rb')
#outfp = file(paper_dir+f.replace('.pdf','.txt'), 'w')
#extractText(infp, outfp)
#outfp.close()
#infp.close()
#f = "KDD1.txt"
#infp = open(paper_dir+f,'rb')
#outfp = file(paper_dir+f.replace('.txt','_refined.txt'), 'w')
#refineText(infp, outfp)
#outfp.close()
#infp.close()

files = os.listdir(paper_dir)
for f in files:
#    if f.endswith('.pdf') and not f.replace('.pdf','.txt') in files:
    if f.endswith('.pdf'):
        infp = open(paper_dir+f,'rb')
        outfp = file(paper_dir+f.replace('.pdf','.txt'), 'w')
        print 'Converting ' + f + '...'
        try:
            extractText(infp, outfp)
        except (ValueError, TypeError):
            print "Error! " + f
        outfp.close()
        infp.close()

files = os.listdir(paper_dir)
for f in files:
    if f.endswith('.txt') and not f.endswith('_refined.txt'):
        infp = open(paper_dir+f,'rb')
        outfp = file(paper_dir+f.replace('.txt','_refined.txt'), 'w')
        print 'Refining ' + f + '...'
        refineText(infp, outfp)
        outfp.close()
        infp.close()