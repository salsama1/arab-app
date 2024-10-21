from flask import Flask, request, jsonify
import cv2
import numpy as np
import pyttsx3
from PIL import Image
import io

app = Flask(__name__)

# Load templates for Arabic numerals (0-9)
templates = {i: cv2.imread(f'templates/{i}.png', 0) for i in range(10)}

def recognize_numeral(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    best_match, best_score = None, float('inf')

    for numeral, template in templates.items():
        res = cv2.matchTemplate(gray_image, template, cv2.TM_SQDIFF)
        min_val, _, _, _ = cv2.minMaxLoc(res)

        if min_val < best_score:
            best_match, best_score = numeral, min_val

    return best_match

def speak_number(numeral):
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)
    engine.say(str(numeral))
    engine.runAndWait()

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    image = Image.open(file.stream)
    image = np.array(image)

    recognized_numeral = recognize_numeral(image)

    if recognized_numeral is not None:
        speak_number(recognized_numeral)
        return jsonify({'number': recognized_numeral}), 200
    else:
        return jsonify({'error': 'No numeral recognized'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
