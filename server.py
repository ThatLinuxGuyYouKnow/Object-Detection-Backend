from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
from PIL import Image
import io
import torch

app = Flask(__name__)

# Disable fork validation check
torch.hub._validate_not_a_forked_repo = lambda a,b,c: True

# Load YOLOv5-nano model
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
model.conf = 0.25  # confidence threshold
model.eval()

def process_image(image_bytes):
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Run inference
    results = model(image)
    
    # Get bounding boxes, classes and confidence scores
    boxes = results.xyxy[0].cpu().numpy()
    
    # Draw boxes on image
    img_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    for box in boxes:
        x1, y1, x2, y2, conf, cls = box
        cv2.rectangle(img_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img_np, f'{results.names[int(cls)]} {conf:.2f}', 
                    (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Convert back to bytes
    is_success, buffer = cv2.imencode(".jpg", img_np)
    return io.BytesIO(buffer.tobytes())

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