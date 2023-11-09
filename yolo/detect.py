from ultralytics import YOLO
from PIL import Image
import pytesseract

#set pytesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def OCR(image,boudingbox)-> str:
    #Crop the image to the bounding box
    cropped_image = image.crop(boudingbox)
    #Convert the image to grayscale
    cropped_image = cropped_image.convert('L')
    #Convert the image to a string
    text = pytesseract.image_to_string(cropped_image)
    return text
    
# Load a pretrained YOLOv8n model
model = YOLO('best.pt')

# Define path to the image file
source = 'test2.png'
# Run inference on the source
results = model(source) 

for r in results:
    for box in r.boxes.xyxy:
        box = box.tolist()
    
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image