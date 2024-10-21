from flask import Flask, request, jsonify
import cv2
import numpy as np
import pyttsx3
from PIL import Image

app = Flask(__name__)

# Define iPhone-like dimensions for resizing (e.g., 1280x960)
IPHONE_WIDTH, IPHONE_HEIGHT = 1280, 960

# Load templates for Arabic numerals (0-9) and preprocess them
def load_and_preprocess_templates():
    templates = {}
    for i in range(10):
        template_path = f'templates/{i}.png'
        template = cv2.imread(template_path, 0)  # Load in grayscale
        if template is not None:
            # Resize template to iPhone-like dimensions
            template = cv2.resize(template, (IPHONE_WIDTH, IPHONE_HEIGHT), interpolation=cv2.INTER_AREA)
            # Apply adaptive thresholding for binary conversion
            _, binary_template = cv2.threshold(template, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # Apply morphological operations to clean the template
            kernel = np.ones((3, 3), np.uint8)
            binary_template = cv2.morphologyEx(binary_template, cv2.MORPH_CLOSE, kernel)
            templates[i] = binary_template
        else:
            print(f"Template for numeral {i} not found or could not be loaded.")
            templates[i] = None
    return templates

# Load templates
templates = load_and_preprocess_templates()

def preprocess_image(image):
    """Preprocess input image to handle shadows and non-white background."""
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize to iPhone-like dimensions
    resized_image = cv2.resize(gray_image, (IPHONE_WIDTH, IPHONE_HEIGHT), interpolation=cv2.INTER_AREA)
    # Apply adaptive thresholding to create a binary image
    binary_image = cv2.adaptiveThreshold(resized_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 11, 2)
    # Apply morphological operations to reduce noise
    kernel = np.ones((3, 3), np.uint8)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    # Apply edge detection to highlight the numeral's shape
    edges = cv2.Canny(binary_image, 50, 150)
    return edges

def recognize_numeral(image):
    """Recognize numeral using robust template matching."""
    preprocessed_image = preprocess_image(image)
    best_match, best_score = None, -1

    for numeral, template in templates.items():
        if template is None:
            continue  # Skip if the template is missing

        # Perform template matching using cross-correlation
        res = cv2.matchTemplate(preprocessed_image, template, cv2.TM_CCOEFF_NORMED)
        max_val = cv2.minMaxLoc(res)[1]

        # Print the score for debugging
        print(f"Matching score for numeral {numeral}: {max_val}")

        # Update best match if correlation is higher
        if max_val > best_score:
            best_match, best_score = numeral, max_val

    # Define a threshold for similarity
    similarity_threshold = 0.5
    print(f"Best matching score: {best_score}, Threshold: {similarity_threshold}")

    if best_score > similarity_threshold:
        print(f"Recognized numeral: {best_match} (score: {best_score})")
        return best_match
    else:
        print("No numeral recognized.")
        return None

def speak_number(numeral):
    """Speak the recognized numeral using text-to-speech."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)
    engine.say(str(numeral))
    engine.runAndWait()

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and numeral recognition."""
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
