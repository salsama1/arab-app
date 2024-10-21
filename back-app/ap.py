import os

# Set environment variable to allow duplicate OpenMP runtime initialization
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, request, jsonify
import easyocr
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize EasyOCR reader with Arabic language support
reader = easyocr.Reader(['ar'])

# Arabic digits list
arabic_digits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        print("No image part in the request")
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    try:
        # Perform OCR using EasyOCR
        results = reader.readtext(image_path, detail=0)
        recognized_text = ''.join(results)
        print(f"Recognized text: {recognized_text}")

        # Filter out the first Arabic digit found
        single_arabic_digit = None
        for char in recognized_text:
            if char in arabic_digits:
                single_arabic_digit = char
                break

        if single_arabic_digit is None:
            return jsonify({'error': 'No Arabic digit recognized'}), 400

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': 'Failed to process image'}), 500

    # Write the recognized Arabic digit to a file
    try:
        output_file = os.path.join(UPLOAD_FOLDER, 'output.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(single_arabic_digit)
    except Exception as e:
        print(f"Error writing to file: {e}")
        return jsonify({'error': 'Failed to write output'}), 500

    return jsonify({'message': 'Arabic digit recognized and saved', 'recognized_digit': single_arabic_digit}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
