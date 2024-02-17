from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash, json, jsonify
from flask_cors import cross_origin
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
from application.models import Entry, Quiz
from sqlalchemy import desc
from . import ai_description, imageArr, dataset_description, db
import re
import base64
import json
import numpy as np
import requests
import os
import datetime
import random
import pytz

main = Blueprint('main', __name__)

# Change timezone to locale timezone
sgt = pytz.timezone('Asia/Singapore')

# Define URLs for Deployed Models
url = {
    "31 x 31 px": {
        "vgg31": "https://ca2-doaa-dl-models.onrender.com/v1/models/vgg31:predict",
    },
    "128 x 128 px": {
        "alexnet128": "https://ca2-doaa-dl-models.onrender.com/v1/models/alexnet128:predict"
    }
}

def parseImage(imgData, imageName):
    """
    Parse base64 image data to save and return the image path.

    Args:
        imgData (str): Base64 encoded image data.
        imageName (str): Name of the image.

    Returns:
        str: Path to the saved image.
    """
    saved_images_dir = os.path.join('application', 'static', 'images', 'saved')
    if not os.path.exists(saved_images_dir):
        os.makedirs(saved_images_dir)
    
    imgStr = re.search(r'base64,(.*)', imgData).group(1)
    unique_filename = f"{datetime.datetime.now().strftime('%f')}-{imageName}"
    imgPath = os.path.join(saved_images_dir, unique_filename)
    
    imgData = base64.b64decode(imgStr)
    with open(imgPath, 'wb') as output:
        output.write(imgData)
    
    im = Image.open(imgPath).convert('RGB')
    im.save(imgPath)
    return f"./{imgPath}"

def make_prediction(instances, model, dataset):
    """
    Make prediction using the provided model and dataset.

    Args:
        instances (numpy.ndarray): Image data as numpy array.
        model (str): Model to be used for prediction.
        dataset (str): Dataset size.

    Returns:
        list: Predicted values.
    """
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url[dataset][model], data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions

@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    """Route to Index Page."""
    return render_template("index.html", logIn=current_user)

@main.route('/history')
@login_required
def history():
    """Route to History Page."""
    if request.args.get("id"):
        return render_template('history.html', logIn=current_user, entries=get_entries(current_user), dataset_description=dataset_description, result=get_entry(request.args.get("id")), quiz_entry=get_quiz_entries(current_user))
    return render_template('history.html', logIn=current_user, entries=get_entries(current_user), dataset_description=dataset_description, result=None, quiz_entry=get_quiz_entries(current_user))

@main.route('/predict', methods=["GET", "POST"])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
@login_required
def predict():
    """Route to Prediction Page."""
    if request.method == 'POST':
        imgPath = parseImage(request.json["imageBlob"], request.json["imageName"])
        
        if request.json['dataset'] == '31 x 31 px':
            target_size = (31, 31)
        elif request.json['dataset'] == '128 x 128 px':
            target_size = (128, 128)
        else:
            return jsonify({"error": "Invalid dataset size"}), 400
        
        img = image.img_to_array(image.load_img(imgPath, color_mode="grayscale", target_size=target_size)) / 255.
        img = img.reshape(1, *target_size, 1)
        
        prediction = make_prediction(img, request.json['model'], request.json['dataset'])
        if not request.json["quiz"]:
            new_entry = Entry(
                user=current_user.id,
                filePath=imgPath,
                modelType=request.json["model"],
                imageSize=request.json['dataset'],
                prediction=int(np.argmax(prediction[0])),
                predicted_on=datetime.datetime.now(sgt))
            new_entryID = add_entry(new_entry)
            return jsonify({'redirect': f'/history?id={new_entryID}', "prediction": int(np.argmax(prediction[0]))})
        return jsonify({"Prediction": int(np.argmax(prediction[0]))})

    random.shuffle(imageArr)
    return render_template("predict.html", logIn=current_user, ai_description=ai_description, dataset_description=dataset_description, imageArr=imageArr)

@main.route('/quiz', methods=["GET", "POST"])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
@login_required
def quiz():
    """Route to Quiz Page."""
    if request.method == "POST":
        new_quiz = Quiz(
            user=current_user.id,
            modelType=request.json["model"],
            imageSize=request.json['dataset'],
            imgs=request.json['imgs'],
            userScore=request.json['userScore'],
            aiScore=request.json['aiScore'],
            quiz_on=datetime.datetime.now(sgt))
        add_entry(new_quiz)
        return jsonify({'message': f'Success'})
    random.shuffle(imageArr)
    return render_template('quiz.html', imageArr=imageArr, logIn=current_user, dataset_description=dataset_description, ai_description=ai_description)

@main.route('/delete/<id>', methods=['POST'])
def delete(id):
    """Deleting ID for History and Quiz."""
    if request.method == "POST":
        delete_entry(id)
    return redirect(url_for('main.history'))

@main.route('/quiz/delete/<id>', methods=['POST'])
def quiz_delete(id):
    """Deleting ID for Quiz."""
    if request.method == "POST":
        delete_quiz(id)
    return redirect(url_for('main.history'))

def add_entry(new_entry):
    """Function to add entry."""
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0

def get_entries(user):
    """Function to get entries."""
    try:
        entries = Entry.query.filter_by(
            user=user.id).order_by(desc(Entry.id)).all()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0

def get_quiz_entries(user):
    """Function to get quiz entries."""
    try:
        entries = Quiz.query.filter_by(
            user=user.id).order_by(desc(Quiz.id)).all()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0
    
def get_entry(id):
    """Function to get entry."""
    try:
        result = Entry.query.get(id)
        return result
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0

def delete_entry(id):
    """Function to delete entry."""
    try:
        entry = Entry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0

def delete_quiz(id):
    """Function to delete quiz."""
    try:
        entry = Quiz.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0
    
# Specifying the API Routes for Add / Get / Delete / Predict
    
# API Get Entry Endpoint
@main.route("/api/get/<id>", methods=['GET'])
def api_get(id):
    entry = get_entry(int(id))
    data = {
        "id": entry.id,
        "user": entry.user,
        "filePath": entry.filePath,
        "modelType": entry.modelType,
        "imageSize": entry.imageSize,
        "prediction": entry.prediction
    }
    result = jsonify(data)
    return result

# API Delete Entry Endpoint
@main.route('/api/delete/<id>', methods=['GET'])
def api_delete(id):
    if request.method == "GET":
        delete_entry(id)
    return jsonify({'result': 'Ok! Delete Successful!'})

# API Add Entry Endpoint
@main.route("/api/add", methods=['POST'])
def api_add():
    # Retrieve the JSON file posted from client
    data = request.get_json()
    # Retrieve each field from the data
    user = data['user']

    imgPath = data['imgPath']
    if imgPath[-4:] != ".png" and imgPath[-4:] != ".jpg" and imgPath[-5:] == ".jpeg":
        return 'Bad request!', 400
    
    modelType = data["modelType"]
    if modelType != "vgg31" and modelType != "alexnet128":
        return 'Bad request!', 400
    
    imageSize = data["imageSize"]
    if imageSize != "31 x 31 px" and imageSize != "128 x 128 px":
        return 'Bad request!', 400
    
    prediction = data["prediction"]
    if imageSize == "31 x 31 px" or imageSize == "128 x 128 px":
        if not (prediction >= 0 and prediction < 15):
            return 'Bad request!', 400
        
    # Create an Entry object to store all data for database
    new_entry = Entry(
        user=user,
        filePath=imgPath,
        modelType=modelType,
        imageSize=imageSize,
        prediction=int(prediction),
        predicted_on=datetime.datetime.now(sgt))
    # Invoke the Add Entry function 
    result = add_entry(new_entry)
    # Return the result of the database action
    return jsonify({'id': result})

# API Predict Endpoint
@main.route("/api/predict", methods=['POST'])
def api_predict():
    data = request.get_json()
    # Perform image preprocessing (Grayscaling & Resizing)
    imgPath = parseImage(data["imageBlob"], data["imageName"])   

    if data['dataset'] == '31 x 31 px':
        target_size = (31, 31)
    elif data['dataset'] == '128 x 128 px':
        target_size = (128, 128)
    else:
        return jsonify({"error": "Invalid dataset size!"}), 400
    
    img = image.img_to_array(image.load_img(imgPath, color_mode="grayscale", target_size=target_size)) / 255.
    img = img.reshape(1, *target_size, 1)
    prediction = make_prediction(img, data['model'], data['dataset'])

    # Create an Entry object to store all data for database
    new_entry = Entry(
        user=data["user"],
        filePath=imgPath,
        modelType=data["model"],
        imageSize=data['dataset'],
        prediction=int(np.argmax(prediction[0])),
        predicted_on=datetime.datetime.now(sgt))
    # Invoke the Add Entry Function
    result = add_entry(new_entry)
    return jsonify({'id': result, "prediction": int(np.argmax(prediction[0]))})



