from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox, LTTextLine, LTFigure

def parse_pdf(f_name):
    fp = open(f_name, 'rb') # open the file in binary
    parser = PDFParser(fp)

    document = PDFDocument(parser, '')
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    analysis = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        analysis.append(device.get_result())

    return analysis

column_range = [(40, 130)]

def analyze(lt_obj: LTTextBox):
    if len(lt_obj.get_text()) != 0:
        # perform task
        print('----- obj ------')
        print(f'pos: x0: {lt_obj.x0} x1: {lt_obj.x1} y0: {lt_obj.y0} y1: {lt_obj.y1}')
        print(lt_obj.get_text().split('\n'))
        print('----- obj ------')

def test_range(r, lt_obj):
    l, r = r[0], r[1]
    if len(lt_obj.get_text()) != 0:
        # perform task
        if lt_obj.x0 >= l and lt_obj.x1 <= r:
            # in range
            print('----- obj ------')
            print(f'pos: x0: {lt_obj.x0} x1: {lt_obj.x1} y0: {lt_obj.y0} y1: {lt_obj.y1}')
            print(f'height: {lt_obj.height}')
            print(lt_obj.get_text().split('\n'))
            print('----- obj ------')


def extract_page(page):
    for lt_obj in page:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            # if parsable text
            # analyze(lt_obj)
            test_range(column_range[0], lt_obj)

def test():
    pages = parse_pdf('menu.pdf')
    extract_page(pages[0])

if __name__ == '__main__':
    test()

