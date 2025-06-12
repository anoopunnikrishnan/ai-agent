import openai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import os

# Load environment variables from .env file
load_dotenv() 

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set OpenAI API key here directly (for testing purposes)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400

        prompt = data['prompt']
        
        # Log received prompt
        app.logger.debug(f"Received prompt: {prompt}")

        # Make a request to the OpenAI API
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # You can try other models too
            prompt=prompt,
            max_tokens=150  # You can adjust this value as per your requirement
        )

        # Log the OpenAI API response
        app.logger.debug(f"OpenAI response: {response}")

        generated_text = response['choices'][0]['text']
        return jsonify({'response': generated_text})

    except KeyError:
        app.logger.error("KeyError: Missing prompt or invalid response format.")
        return jsonify({'error': 'Invalid data format, missing "prompt" key'}), 400
    except Exception as e:
        # Log the full exception message
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

    # The below line ensures the app uses the PORT environment variable in production (e.g., on Vercel)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)
