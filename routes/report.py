from flask import json, jsonify
import base64
import google.generativeai as genai
import os
from dotenv import load_dotenv




load_dotenv()

api_key: str = os.environ.get("GEMINI_API_KEY")
# Configure Gemini
genai.configure(api_key=api_key)

# Define system instruction to avoid unwanted formatting, best not to change this AT ALL
system_instruction = """
Generate a report on the image file you have recieved, start by describing the scene, and then the lighting, and then a general description. Return this report as pure json,no  code blocks, line breaks or slashes
Example of bad output: ```json\n{\n  \"report\": \"Scenery is vegetation, likely a farm\"\n}\n```
Example of good output: {"report": "Scenery is vegetation, likely a farm"}
"""

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)

def generate_report(request):
 try:
       
        file = request.files.get('file')
        
        # Validate input
        if not file:
            return {'error': 'image is required'}, 400
            
        # Read the file content
        image_content = file.read()
        
        # Encode the file content in base64
        image_data = base64.b64encode(image_content).decode('utf-8')
        
        # Define the prompt for Gemini
        prompt = """
        Generate a report on the objects found this image, be very descriptive
        """
        
        # Pass the file content and prompt to Gemini
        response = model.generate_content([
            {'mime_type': file.mimetype, 'data': image_data},
            prompt
        ])
        
        # Get the response text and parse it as JSON
        print(response.text)
        extracted_data = json.loads(response.text)
  
            
        # Return the data without jsonifying it yet
        return {'data': extracted_data}, 200

 except Exception as e:
        return {'error': str(e)}, 400
