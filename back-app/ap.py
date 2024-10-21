from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# Configure the path to Tesseract executable (only required on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path

UPLOAD_FOLDER = 'upload'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    # Perform OCR on the image
    try:
        text = pytesseract.image_to_string(Image.open(image_path), lang='ara')
    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

    # Write recognized text to a file
    output_file = os.path.join(UPLOAD_FOLDER, 'output.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

    return jsonify({'message': 'Text recognized and saved'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
