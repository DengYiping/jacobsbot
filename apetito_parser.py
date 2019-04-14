from PyPDF2 import PdfFileReader, PdfFileWriter
from wand.image import Image
import os, sys
import datetime

PDF_FILE = 'menu.pdf'

def find_today():
    weekday = datetime.date.today().weekday()
    lunch_jpg = f'{weekday}_lunch.jpg'
    dinner_jpg = f'{weekday}_dinner.jpg'

    if not os.path.exists(lunch_jpg):
        crop_pdf(PDF_FILE, f'{weekday}_lunch.jpg', 0, offset_list[weekday])

    if not os.path.exists(dinner_jpg):
        crop_pdf(PDF_FILE, f'{weekday}_dinner.jpg', 1, offset_list[weekday])

    return lunch_jpg, dinner_jpg

def crop_pdf(pdf, target, page_num, tup):
    top, left, bottom, right = tup
    tmp_fname = 'tmp.pdf'
    pdf_fp = open(pdf, 'rb')
    pdf = PdfFileReader(pdf_fp)
    out = PdfFileWriter()

    page = pdf.pages[page_num]

    page.mediaBox.upperRight = (page.mediaBox.getUpperRight_x() - right, page.mediaBox.getUpperRight_y() - top)
    page.mediaBox.lowerLeft  = (page.mediaBox.getLowerLeft_x()  + left,  page.mediaBox.getLowerLeft_y()  + bottom)

    out.addPage(page)
    ous = open(tmp_fname, 'wb')
    out.write(ous)
    ous.close()

    with Image(filename = tmp_fname, resolution = 300) as img:
        img.save(filename = target)

    os.remove(tmp_fname)
    pdf_fp.close()

offset_list = [
    (100, 40, 100, 690),
    (100, 150, 100, 580),
    (100, 260, 100, 460),
    (100, 375, 100, 350),
    (100, 490, 100, 240),
    (100, 600, 100, 130),
    (100, 710, 100, 10)
]

def main():
    crop_pdf('menu.pdf', 'test.jpg', 0, offset_list[6])

if __name__ == '__main__':
    main()
