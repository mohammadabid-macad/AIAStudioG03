from flask import Flask, request, render_template, jsonify
#from segmentation_model.py import run_segmentation_model
from second_model import run_second_model
import os
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def handle_image_upload():
    image = request.files['file']
    image_path = os.path.join('uploads', image.filename)
    image.save(image_path)

    #segmented_image, segmentation_results = run_segmentation_model(image_path)

    # Save segmented image
   # segmented_image_path = os.path.join('uploads', 'segmented_' + image.filename)
   # Image.fromarray(segmented_image).save(segmented_image_path)

    #return jsonify({
    #    "segmented_image_path": segmented_image_path,
    #    "segmentation_results": segmentation_results
   # })

@app.route('/analyze_location', methods=['POST'])
def analyze_location():
    data = request.json
    lat = data['lat']
    lon = data['lon']
    segmentation_results = data['segmentation_results']

    analysis_results = run_second_model(lat, lon, segmentation_results)
    return jsonify(analysis_results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
