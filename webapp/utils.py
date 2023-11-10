import os
import pdf2image
import pytesseract
from PIL import Image
import base64
from io import BytesIO
from PIL import Image
import numpy as np

def image_to_base64(img, format="PNG"):
    buffered = BytesIO()
    img.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')

def convertPDF2IMG(path,name = None):
    if name is None:
        file_name = os.path.splitext(os.path.basename(path))[0]
        pages = pdf2image.convert_from_path(path)
    else:
        file_name = name
        pages = pdf2image.convert_from_bytes(path)

    output_folder = 'uploads/images/'+file_name+'/'
    #Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    #Split the pdf into pages
    #Save the pages
    jsonR = {}
    for i in range(len(pages)):
        jsonR['page'+str(i)] = image_to_base64(pages[i])
        pages[i].save(output_folder + file_name+"_page_"+str(i) + ".png", "PNG")

    return jsonR

def OCR(image_numpy,boudingbox)-> str:
    image = Image.fromarray(image_numpy)
    #For debugging
    image.save('image.png')
    #Crop the image to the bounding box
    cropped_image = image.crop(boudingbox)
    #Convert the image to grayscale
    cropped_image = cropped_image.convert('L')

    #For debugging
    cropped_image.save('cropped.png')

    #Convert the image to a string
    text = pytesseract.image_to_string(cropped_image, lang='fra')
    return text

def base64_to_numpy(base64_string):
    imgdata = base64.b64decode(base64_string)
    image = Image.open(BytesIO(imgdata))
    return np.array(image)
    