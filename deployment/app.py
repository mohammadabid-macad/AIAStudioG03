from flask import Flask, request, render_template, jsonify
import pickle
from PIL import Image
import io
import numpy as np

app = Flask(__name__)

# Load your model
with open('deployment\templates\building_with_materials.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_coordinates', methods=['POST'])
def handle_coordinates():
    data = request.json
    coordinates = data['coordinates']
    
    # Process coordinates if needed and make predictions
    prediction = model.predict([coordinates])
    
    return jsonify({"status": "success", "prediction": prediction.tolist()})

@app.route('/upload_image', methods=['POST'])
def handle_image_upload():
    image = request.files['file']
    image = Image.open(image.stream)
    
    # Preprocess the image for your model
    image = image.resize((224, 224))  # Example resize
    image_array = np.array(image) / 255.0  # Example normalization
    image_array = image_array.reshape((1, -1))
    
    # Predict materials using the model
    prediction = model.predict(image_array)
    
    # Process the prediction results to a suitable format
    results = {
        "wood": prediction[0][0],
        "concrete": prediction[0][1],
        "stone": prediction[0][2],
        "plaster": prediction[0][3],
        "metal": prediction[0][4]
    }
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
