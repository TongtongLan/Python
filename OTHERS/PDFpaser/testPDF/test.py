#!/usr/bin/python
# -*- coding: UTF-8 -*-s
import sys
import os
from binascii import  b2a_hex

from pdfminer.pdfparser import  PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTRect, LTCurve
from pdfminer.pdfpage import PDFPage

def with_pdf(pdf_doc, pdf_pwd, fn, *arg):

    '''
    open the pdf document, and apply the function, retuning the results
    :param pdf_doc:
    :param pdf_pwd:
    :param fn:
    :param arg:
    :return:
    '''
    try:
        # open the pdf document
        fp = open(pdf_doc, 'rb')
        # create a paser Object
        parser = PDFParser(fp)
        # create a PDFdocument object that stores the document structure and connect the parser object
        doc = PDFDocument(parser, pdf_pwd)
        if doc.is_extractable:
            # apply the function and return the results
            result = fn(doc, *arg)
    except IOError:
        # the file doesn't exist or similar problem
        print ("The file doesn't exist")
    finally:
        # close the pdf file
        fp.close()

def _parser_toc(doc):
    '''
    With an open PDFDocument object, get the table of contents data
    :param doc:
    :return:
    '''

    toc = []
    try:
        outlines = doc.get_outlines()
        toc.append(outlines)
    except PDFNoOutlines as e:
        print e
    return toc

def _parser_page(doc, images_folder):
    '''
    With an open PDFDocument object, get the page and parse each one
    :param doc:
    :return:
    '''

    # create a PDFResourceManager object
    rsrcmgr = PDFResourceManager()
    # get the laparams to analsis PDF file(设置参数分析)
    laparams = LAParams()
    # create a device object
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # create a PDFPageInterpreter object(解释器对象)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    pagelist = []
    i = 0
    # parse each page
    for page in PDFPage.create_pages(doc):
        i += 1
        interpreter.process_page(page)
        # receive the LTPage object for this page
        layout = device.get_result()
        # layout is an LTPage object witch may contain child objects like LTTextBox, LTFigure, LTImage, etc.
        pagelist.append(parse_lt_objs(layout, i, images_folder))
    return pagelist

def determine_image_type(stream_first_4_bytes):
    """Find out the image file type based on the magic number comparison of the first 4 (or 2) bytes"""
    file_type = None
    bytes_as_hex = b2a_hex(stream_first_4_bytes)
    if bytes_as_hex.startswith('ffd8'):
        file_type = '.jpeg'
    elif bytes_as_hex == '89504e47':
        file_type = '.png'
    elif bytes_as_hex == '47494638':
        file_type = '.gif'
    elif bytes_as_hex.startswith('424d'):
        file_type = '.bmp'

    return file_type

def write_file(folder, filename, filedata, flags='w'):
    """Write the file data to the folder and filename combination
        (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
    result = False
    if os.path.isdir(folder):
        try:
            file_obj = open(os.path.join(folder, filename), flags)
            #print os.path.join(folder, filename)
            file_obj.write(filedata)
            file_obj.close()
            result = True
        except IOError:
            pass
    return result

def save_image(lt_image, page_number, images_folder):
    '''
    Try to save the image data from this LTImage object, and return the file name
    :param lt_image:
    :param page_number:
    :param images_folder:
    :return:
    '''
    result = None
    if lt_image.stream:
        file_stream = lt_image.stream.get_rawdata()
        if file_stream:
            file_ext = determine_image_type(file_stream[0:4])
            if file_ext:
                file_name = ''.join([str(page_number), '_', lt_image.name, file_ext])
                if write_file(images_folder, file_name, file_stream, flags = 'wb'):
                    result = file_name
    return result

def updage_page_text_hash(text_dict, lt_obj, pct = 0.2):
    '''
    use the bbox(bounding box)x0, x1 values within pct% to produce lists of associated text within the hass
    :param text_dict:
    :param lt_obj:
    :param pct:
    :return: text_dict
    '''

    x0 = lt_obj.bbox[0]
    x1 = lt_obj.bbox[1]

    key_found = False

    for k, v in text_dict.items():
        hash_x0 = k[0]
        if x0 >= (hash_x0 * (1 - pct)) or x0 <= (hash_x0 * (1 + pct)):
            hash_x1 = k[1]
            if x1 >= (hash_x1 * (1 - pct)) or x1 <= (hash_x1 * (1 + pct)):
                # the text inside this LT* object was positioned at the same
                # width as a prior series of text, so it belongs together
                key_found = True
                #print 'lt_obj_text:'+lt_obj.get_text()
                data = str(lt_obj.get_text().encode('utf-8'))
                print str(lt_obj.get_text().encode('utf-8'))
                print data.split(' ')

                v.append(data)
                text_dict[k] = v

    if not key_found:
        #
        # so it gets its own series(entry in the hash)
        #print 'lt_obj_text:' + lt_obj.get_text()
        data = str(lt_obj.get_text().encode('utf-8'))

        text_dict[(x0, x1)] = list(data)
    return text_dict

def parse_lt_objs(lt_objs, page_number, images_folder, text=[]):
    '''
    Iterate through the list of LT* objects and capture the text or image data contained in each page
    :param lt_objs:
    :param page_number:
    :param images_folder:
    :param text:
    :return:
    '''

    text_content = []
    page_text = {}

    for lt_obj in lt_objs:
        if isinstance(lt_obj, LTTextLine) or isinstance(lt_obj, LTTextBox):
            # text, so arrange is logically based on its column width
            page_text = updage_page_text_hash(page_text, lt_obj)
            #text_content.append(lt_obj.get_text())
        elif isinstance(lt_obj, LTImage):
            # image
            print 'image'
            # an image, so save it to the designated folder, and note its place in the text
            saved_file = save_image(lt_obj, page_number, images_folder)
            if saved_file:
                print "the current image saved_file name is :" + saved_file
                # use html style <img /> tag to mark the position of the image within the text
                text_content.append('<img src="' + os.path.join(images_folder, saved_file) + '" />')
            else:
                print >> sys.stderr, "error saving image on page", page_number, lt_obj.__repr__

        elif isinstance(lt_obj, LTFigure):
            # LTFigure objects are containers for other LT* objects, so recurse the children
            print 'LTFigure'
            text_content.append(parse_lt_objs(lt_obj, page_number, images_folder, text_content))
            print 'LTFigure end'

    for k, v in sorted([(key, value) for (key, value) in page_text.items()]):
        # sort the page_text hash by the keys (x0, x1 values of the bbox, witch produces a top-down,
        # left-to-rigth sequence of related columns
        #text_content.append('\n' + v)
        text_content.append(v)
        #print text_content
        #data = data.replace('\n', ' ')
        for data in v:
            #print data
            write_file('/home/tongtong/文档', 'testPDF', data, flags='a')

    return text_content



def get_toc(pdf_doc, pdf_pwd=''):
    return with_pdf(pdf_doc, pdf_pwd, _parser_toc)

def get_page(pdf_doc, pdf_pwd='', images_folder='/home/tongtong/文档'):
    return with_pdf(pdf_doc, pdf_pwd, _parser_page, *tuple([images_folder]))

#get_toc("/home/tongtong/文档/1-s2.0-S0009261416307229-main.pdf",pdf_pwd='')
get_page("/home/tongtong/文档/1-s2.0-S0009261416307229-main.pdf",
        pdf_pwd='', images_folder='/home/tongtong/文档')