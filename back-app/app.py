from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    # Get the image from the request
    image_file = request.files['image']
    img = Image.open(io.BytesIO(image_file.read()))

    # Perform OCR on the image using Tesseract, specifying Arabic language
    text = pytesseract.image_to_string(img, lang='ara')

    # Filter to just Arabic numbers (٠١٢٣٤٥٦٧٨٩)
    arabic_numbers = ''.join(filter(lambda x: x in '٠١٢٣٤٥٦٧٨٩', text))

    return jsonify({"numbers": arabic_numbers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
