from flask import Flask, request, render_template, jsonify
import os
from PIL import Image
import io
import facade_calc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def handle_image_upload():
    image = request.files['file']
    image_path = os.path.join('static', image.filename)
    image.save(image_path)

    # Update the image_url in facade_calc
    facade_calc.image_url = image_path

    return jsonify({"message": "Image uploaded successfully"})

@app.route('/analyze_location', methods=['POST'])
def analyze_location():
    data = request.json
    lat = data['lat']
    lon = data['lon']

    # Update the lat and lon in facade_calc
    facade_calc.lat = lat
    facade_calc.lon = lon

    # Run the facade calculation with the new data
    results = facade_calc.calculate_facade_area_and_materials()

    return jsonify(results)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True, host='0.0.0.0')
