import sys, os

# customized database class
from database import Database

# parser ANTLR
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from PdfDividendLexer import PdfDividendLexer
from PdfDividendParser import PdfDividendParser
from listener_dividend import ListenerDividend

# pdf miner
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

#
# function reads a pdf file and returns the content as string
#
def convert_pdf_to_txt(path):
    # setup
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    extracted_text = ''
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
    
    # close file and return its content
    fp.close()
    return extracted_text

def main(argv):
    
    dir_app = os.path.dirname(os.path.abspath(__file__))
    dir_tmp = os.path.join(dir_app, 'tmp')
    if len(sys.argv) > 2:
        print('usage: ./run_data_extraction.py [pdf-directory-abs]')
        sys.exit(1)
    elif len(sys.argv) == 2:
        dir_pdf = sys.argv[1]
    else:
        dir_pdf = os.path.join(dir_app, 'pdf')
    
    # get all the PDF filenames
    pdfFiles = []
    for filename in os.listdir(dir_pdf):
        if filename.endswith('.pdf'):
            pdfFiles.append(filename)
    pdfFiles.sort(key=str.lower)
    print(pdfFiles)
  
    # initiate the database class and open a database connection
    db = Database()
    
    listen_div = ListenerDividend()
    for filename in pdfFiles:
        
        # read pdf file, convert it to text, and store it as text file in the
        # tmp directory for further processing/debugging
        print('processing file ' + filename)
        tmp_filename = os.path.join(dir_tmp, filename.replace('.pdf', '.txt'))
        sometext = convert_pdf_to_txt(os.path.join(dir_pdf, filename))
        f = open(tmp_filename, mode='w', encoding='UTF-8')
        f.write(sometext)
        f.close()
        istream = FileStream(tmp_filename, encoding='UTF-8')
        
        # parse the file
        lexer = PdfDividendLexer(istream)
        stream = CommonTokenStream(lexer)
        parser = PdfDividendParser(stream)
        tree = parser.rules()
        #print(tree.toStringTree(recog=parser))
        
        # listen to the words
        walker = ParseTreeWalker()
        walker.walk(listen_div, tree)
        
        # write listen words and filename to database
        db.write_to_database(listen_div, filename)
        
        # clean up tmp file
        os.remove(tmp_filename)
        listen_div.reset()
        
    # close database connection
    db.close()
    
if __name__ == '__main__':
    main(sys.argv)
