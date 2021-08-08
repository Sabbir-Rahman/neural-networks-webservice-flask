
import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask
from flask_cors import CORS, cross_origin
import cv2

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_model():
    global model
    model = load_model('vgg_16tl.model')
    print(" * Model Loaded! ")

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    # print('=========== preprocess image ===========')
    open_cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    open_cv_img = open_cv_img/255
    new_array = cv2.resize(open_cv_img, (224, 224))
    
    return new_array.reshape(-1, 224, 224, 3)

print(" * Loading keras model...")
get_model()

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224,224))

    prediction = model.predict(processed_image).tolist()
    print('===============')
    print(np.argmax(prediction))
    response = {
        'prediction':{
            'Bacterialblight': prediction[0][0],
            'Blast': prediction[0][1],
            'Brownspot': prediction[0][2],
            'Tungro': prediction[0][3],
        }
    }
 

    return jsonify(response)