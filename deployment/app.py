from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_coordinates', methods=['POST'])
def handle_coordinates():
    data = request.json
    coordinates = data['coordinates']
    # Process coordinates if needed
    return jsonify({"status": "success", "coordinates": coordinates})

@app.route('/upload_image', methods=['POST'])
def handle_image_upload():
    image = request.files['file']
    # Here you would process the image and estimate materials
    # Dummy response
    results = {
        "wood": "20 m²",
        "concrete": "15 m²",
        "stone": "5 m²",
        "plaster": "10 m²",
        "metal": "3 m²"
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

