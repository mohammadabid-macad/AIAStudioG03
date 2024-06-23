from flask import Flask, request, render_template, jsonify
from facade_calc import calculate_facade_area_and_materials, image_url, lat, lon

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    global image_url, lat, lon
    image_url = data['image_url']
    lat = float(data['latitude'])
    lon = float(data['longitude'])
    results = calculate_facade_area_and_materials()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
