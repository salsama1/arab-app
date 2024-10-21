from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the 'image' part is present in the request
    if 'image' not in request.files:
        print("No image part in the request")
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    print(f"Received image: {image_file.filename}")

    # Save the image to the uploads folder
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    # Perform OCR on the image
    try:
        text = pytesseract.image_to_string(Image.open(image_path), lang='ara')
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': 'Failed to process image'}), 500

    # Write recognized text to a file
    try:
        output_file = os.path.join(UPLOAD_FOLDER, 'output.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(f"Error writing to file: {e}")
        return jsonify({'error': 'Failed to write output'}), 500

    return jsonify({'message': 'Text recognized and saved'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
