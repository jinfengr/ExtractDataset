import os

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

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
    for line in infp:
        current = line.strip().replace('  ',' ')
        if current == '':
            outfp.write(''.join(stringlist)+'\n')
            stringlist = []
            outfp.write('\n')
        elif current[-1] == '-':
            stringlist.append(current[0:-1])
        else:
            stringlist.append(current+' ')
    outfp.write(''.join(stringlist)+'\n')
    

paper_dir = '../data/training_data/'

files = os.listdir(paper_dir)
for f in files:
    if f.endswith('.pdf') and not f.replace('.pdf','.txt') in files:
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
