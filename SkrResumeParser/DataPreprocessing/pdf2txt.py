from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os

'''
this package is used for coverting pdf file to txt file
it contain two funtion
    convert(fname, pages=None)
    convertMultiple(pdfDir, txtDir)
'''
#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    '''
    this funtion is used to convert any pdfs file to text and return all text
    :param fname:path of file with its name
    :param pages:
    :return: text in file
    '''
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def convertMultiple(pdfDir, txtDir):
    '''
    this funtion is used to convert multiple pdfs which is stored in some folder
    :param pdfDir: path of dir of pdfs
    :param txtDir: path where txt file will be save after converting
    :return: nothing
    '''
    if pdfDir == "": pdfDir = os.getcwd() + "\\" #if no pdfDir passed in
    for pdf in os.listdir(pdfDir): #iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf
            text = convert(pdfFilename) #get string of text content of pdf
            textFilename = txtDir + pdf + ".txt"
            textFile = open(textFilename, "w") #make text file
            textFile.write(text) #write text to text file

if __name__ == "__main__":

    convertMultiple('../Data/resume_samples/pdfs/samples/', '../Data/resume_samples/txts/samples/')