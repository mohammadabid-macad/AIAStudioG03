from flask import Flask, request, render_template, jsonify
import os
import facade_calc_part_b as fcpb

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def handle_image_upload():
    image = request.files['file']
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    if image:
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        # Get building info using lat and lon
        building_info = fcpb.get_building_info(float(lat), float(lon))

        # Return a simple test message with building info
        return jsonify({
            "message": "Image received successfully!",
            "image_path": image_path,
            "building_info": building_info
        })
    else:
        return jsonify({"message": "No image uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True)
