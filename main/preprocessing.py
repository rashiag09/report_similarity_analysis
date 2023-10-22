#mounting to google drive
from google.colab import drive
drive.mount('/content/drive')
import json, pickle
import pandas as pd

#importing required libraries
import glob, sys, fitz
import tqdm
import os
import io
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal,LTTextBox, LTFigure, LTImage
import pandas as pd
import numpy as np
import re
import json
import cv2

#function for creating a bounding box
def get_bbox(sizeRatioW, sizeRatioH, pageW, pageH, bbox):
    return int(bbox[0] * sizeRatioW), int(pageH - bbox[1] * sizeRatioH),  int(bbox[2] * sizeRatioW), int(pageH - bbox[3] * sizeRatioH)

#function for converting pdf to image
def pdftoimg(filepath,filename):
    doc = fitz.open(filepath)
    i = 0
    for page in doc:
        i += 1
        pix = page.get_pixmap()
#         pdfname = file.split('.')[0].split('\\')[-1]
        file = "/content/drive/MyDrive/data/pdfminer_processing/image/"+filename
        pix.save("{}_page-{}.png".format(file, page.number))
#     self.total_page = i

#adding the path of the folder in google drive to access the reports
file_path = "/content/drive/MyDrive/annotated_fold/"
file_list = os.listdir(file_path)

#the number of files in the folder
len(file_list)

#name of the first report
file_list[0]

#running all the functions and saving the input in google drive
count = 0
from tqdm import tqdm
for todo_file in tqdm(file_list):
    count += 1

    doc_path = file_path + todo_file
    file_name = todo_file[:-4]
    pdftoimg(doc_path,file_name)

    document = open(doc_path, 'rb')
    #Create resource manager
    rsrcmgr = PDFResourceManager()
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_num = 0

    print("Now processing : ", count)
    try:
     for page in PDFPage.get_pages(document):

        json_file = {}
        json_file[file_name] = {}

        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        obj_id = 0


        imgFilePath = "/content/drive/MyDrive/data/pdfminer_processing/image/"+ file_name + '_page-' + str(page_num) +'.png'

        img = cv2.imread(imgFilePath, cv2.IMREAD_UNCHANGED)

        imgHeight, imgWidth, imgChannels = img.shape

        pageW = page.mediabox[2]
        pageH = page.mediabox[3]
        sizeRatioW =  imgWidth / page.mediabox[2]
        sizeRatioH =  imgHeight / page.mediabox[3]

        for lt_obj in layout:

            #code to annotate the table in the report
            if isinstance(lt_obj, LTTextBox):
                for obj in lt_obj:
                    new_bbox = get_bbox(sizeRatioW, sizeRatioH, pageW, pageH, obj.bbox) #find text box
                    cv2.rectangle(img, (new_bbox[0], new_bbox[1]), (new_bbox[2], new_bbox[3]), (0, 0, 255, 255), 1) #red
                    if obj_id not in json_file[file_name]:
                      json_file[file_name][obj_id] = {}
                      json_file[file_name][obj_id]['LTTextBox'] = {}
                      json_file[file_name][obj_id]['LTTextBox']['bbox'] = new_bbox
                      json_file[file_name][obj_id]['LTTextBox']['text'] = obj.get_text()
                      obj_id += 1

            elif isinstance(lt_obj, LTFigure):
                for obj in lt_obj:
                    new_bbox = get_bbox(sizeRatioW, sizeRatioH, pageW, pageH, obj.bbox) #find text box
                    cv2.rectangle(img, (new_bbox[0], new_bbox[1]), (new_bbox[2], new_bbox[3]), (0, 255, 0, 255), 1) #green
                    if obj_id not in json_file[file_name]:
                      json_file[file_name][obj_id] = {}
                      json_file[file_name][obj_id]['LTFigure'] = {}
                      json_file[file_name][obj_id]['LTFigure']['bbox'] = new_bbox
                      obj_id += 1


        # save img
        img_file = "/content/drive/MyDrive/data/pdfminer_processing/image2/" + file_name + '_page-' + str(page_num) +'.png'
        cv2.imwrite(img_file, img)

        file_loc = "/content/drive/MyDrive/data/pdfminer_processing/textline/" + file_name + "_page-" + str(page_num) + ".json"

        with open(file_loc,'w') as output:
            json_str = json.dumps(json_file)
            output.write(json_str)

        page_num += 1
    except:
     print(todo_file)
