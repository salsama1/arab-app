import cv2
import easyocr
import numpy as np
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Initialize EasyOCR Reader for Arabic language
reader = easyocr.Reader(['ar'])

def process_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize image to a standard size for better OCR accuracy
    resized = cv2.resize(gray, (600, 600), interpolation=cv2.INTER_LINEAR)
    return resized

def extract_text(image):
    # Read text using EasyOCR
    results = reader.readtext(image, detail=0)  # Get all detected text without filtering
    return results

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return make_response(jsonify({"message": "No image file provided"}), 400)

    file = request.files['image']

    # Check if the file is an image
    if not file.content_type.startswith('image/'):
        return make_response(jsonify({"message": "Uploaded file is not an image"}), 400)

    # Read the image from the uploaded file
    np_img = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if image is None:
        return make_response(jsonify({"message": "Invalid image file"}), 400)

    # Process the image and extract text
    processed_image = process_image(image)
    detected_text = extract_text(processed_image)

    # Print all detected text in the terminal
    if detected_text:
        print(f"Detected text: {', '.join(detected_text)}")
        return jsonify({"message": f"Detected text: {', '.join(detected_text)}"})
    else:
        print("No text found in the image")
        return jsonify({"message": "No text found in the image"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
