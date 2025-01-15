## Object Detection Backend
### Hosts a YoloV5 nano model(from Ultralytics, loaded through Pytorch)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![YOLOv5](https://img.shields.io/badge/YOLOv5-7.0+-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A Flask-based backend service that provides object detection capabilities using YOLOv5 nano model, enhanced with Gemini AI for detailed scene analysis and reporting.

## Features

- Real-time object detection using YOLOv5 nano model
- Scene analysis and contextual insights using Gemini AI
- Detailed report generation for detected objects
- Cross-origin resource sharing (CORS) enabled
- Low confidence threshold for maximum object detection

## API Endpoints

### 1. Object Detection
```
POST /detect
```
Processes an image and returns the annotated version with detected objects.

**Request:**
- Content-Type: multipart/form-data
- Body: image file

**Response:**
- JPEG image with bounding boxes and labels

### 2. Analysis
```
POST /analyse
```
Provides contextual insights about the detected objects using Gemini AI.

**Request:**
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
    "data": {
        "analysis": "Contextual analysis of the scene"
    }
}
```

### 3. Report
```
POST /report
```
Generates a detailed report about the scene and detected objects.

**Request:**
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
    "data": {
        "report": "Detailed description of the scene"
    }
}
```

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up environment variables:
```bash
GEMINI_API_KEY=your_gemini_api_key
```
4. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Technical Details

- **YOLOv5 Configuration:**
  - Model: YOLOv5-nano (optimized for speed)
  - Confidence threshold: 0.1 (set low to minimize false negatives)
  - Auto-download of model weights on first run

- **Gemini AI Integration:**
  - Uses Gemini 1.5 Flash for rapid inference
  - Custom system instructions for consistent JSON output
  - Base64 encoding for image processing

## Dependencies

- Flask
- PyTorch
- OpenCV
- Pillow
- google.generativeai
- python-dotenv
- Flask-CORS

## Notes

- The server includes CORS support for cross-origin requests
- YOLOv5 fork validation is disabled for compatibility with cloud deployment services
- Error handling is implemented for all endpoints with appropriate status codes
- Image processing results are returned in JPEG format

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.