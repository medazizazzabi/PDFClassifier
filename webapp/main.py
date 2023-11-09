from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import os
import uuid
import threading
import json

from classifier import classify
from utils import convertPDF2IMG, OCR, base64_to_numpy
from PSA import PSA

app = Flask(__name__)
model = YOLO('best.pt')

def predict(name):
    directory = 'uploads/images/'+name
    results = model(directory)
    jsonR = {}
    i = 0
    for r in results:
        jsonR['page'+str(i)] = []
        for box in r.boxes.xyxy:
            box = box.tolist()
            text = OCR(r.orig_img,box)
            jsonR['page'+str(i)].append({'x':box[0],'y':box[1],'w':box[2]-box[0],'h':box[3]-box[1],'text':text})
        i+=1
    return jsonR

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/uploadPDF', methods=['POST'])
def uploadPDF():
    if 'PDF' in request.files:
        PDFfile = request.files['PDF']
        fileID = str(uuid.uuid4())  # Convert UUID object to a string
        encoded = convertPDF2IMG(PDFfile.read(), fileID)
        boxes = predict(fileID)
        response = jsonify({'status': 'success', 'images': encoded,"boxes":boxes})
        response.set_cookie('fileID', fileID)
        return response
    elif 'api_key' and 'modelID' in request.form:
        api_key = request.form['api_key']
        modelID = request.form['modelID']

        fileID = str(uuid.uuid4())

        psa = PSA(api_key,modelID,fileID)
        boxes = predict(fileID)
        response = jsonify({'status': 'success', 'images': psa.jsonImages,"fields":psa.jsonFields,"boxes":boxes})
        response.set_cookie('fileID', fileID)
        return response
    else:
        return jsonify({'status': 'failed'})
    

@app.route('/api/result', methods=['GET'])
def getResult():
    fileID = request.cookies.get('fileID')
    if fileID is None:
        return jsonify({'status': 'failed', 'message': 'No file uploaded'})
    elif 'Fields' in request.files:
        fields = request.files['Fields']
        fields_path = os.path.join('uploads/fields/', fileID + '.json')
        fields.save(fields_path)
        with open('uploads/titles/',fileID+".json") as titles:
            categories = json.load(titles)
        with open(fields_path) as fields:
            fields = json.load(fields)
        result = classify(categories,fields)
        return jsonify({'status': 'success', 'result': result})
    else:
        return jsonify({'status': 'failed', 'message': 'Missing Files'})

@app.route('/api/OCR', methods=['POST'])
def getOCR():
    if 'image' and 'box' in request.form:
        #Conver image from a base64 string to a numpy array
        image = request.form['image']
        image = base64_to_numpy(image)
        #Box
        box = request.form['box']
        box = json.loads(box)
        xyxy = [box['x'],box['y'],box['x']+box['w'],box['y']+box['h']]

        text = OCR(image,xyxy).strip()
        return jsonify({'status': 'success', 'text': text})
    elif 'boxes' in request.form:
        boxes = request.form['boxes']
        boxes = json.loads(boxes)
        image = request.form['image']
        image = base64_to_numpy(image)
        text = []
        for box in boxes:
            xyxy = [box['x'],box['y'],box['x']+box['w'],box['y']+box['h']]
            text.append(OCR(image,xyxy).strip())
        return jsonify({'status': 'success', 'text': text})
    else:
        return jsonify({'status': 'failed', 'message': 'Missing Files'})
    
@app.route('/api/classify', methods=['POST'])
def getClassification():
    if 'fields' in request.files and 'categories' in request.form:
        fields = request.files['fields']
        fields = json.load(fields)
        categories = request.form['categories']
        categories = json.loads(categories)
        result = classify(categories,fields)
        return jsonify({'status': 'success', 'result': result})
    else:
        return jsonify({'status': 'failed', 'message': 'Missing Files'})

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,port=3232)