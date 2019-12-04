from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64,re,time
import numpy as np
import imutils
import cv2
import os
app = Flask(__name__)
CORS(app)

def convert_and_save(b64_string):
    base64_data = re.sub('^data:image/.+;base64,', '', b64_string)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    t = time.time()
    print(os.getcwd() + str(t))
    img.save('fromclient.jpg')

@app.route('/',methods = ['GET'])
def hello_world():
    print(cv2)
    return 'Hello World!'

@app.route('/getSkeleton', methods = ['POST'])
def get_skeleton():
    base_64_code = request.json["image"]
    print(base_64_code)
    convert_and_save((base_64_code) )
    os.system("python final_model_script.py")
    with open("output.jpg", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    print(my_string.decode('utf-8'))
    f = open('predicted_pose.txt')
    line = f.readline()
    f.close()
    return jsonify(name=line, code=my_string.decode('utf-8'))


if __name__ == '__main__':
    app.run()
