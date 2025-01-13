from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, send_file
from routes.analyse import generate_analysis
from routes.report import generate_report
from yolo import process_image


app = Flask(__name__)
cors = CORS(app)
@app.route('/report', methods=['POST', 'OPTIONS'])
def report():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return generate_report(request)

@app.route('/analyse', methods=['POST', 'OPTIONS'])
def analyse():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return generate_analysis(request)
@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    img_bytes = file.read()
    
    # Process image and get result
    result_image = process_image(img_bytes)
    
    # Return the processed image
    return send_file(
        result_image,
        mimetype='image/jpeg',
        as_attachment=True,
        download_name='result.jpg'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)