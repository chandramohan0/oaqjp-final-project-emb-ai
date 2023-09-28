"""
Emotion Detector Web Application

This Flask-based web application allows users to input text for emotion analysis. It sends the
text to an external Emotion Detection API and displays the result on a web page.

Author: Your Name
Date: Date of creation
"""
from flask import Flask, request, render_template
import requests

app = Flask("Emotion Detector")

# Define the URL for the Emotion Detection API
EMOTION_API_URL = (
    'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/'
    'NlpService/EmotionPredict'
)

@app.route('/')
def index():
    """Render the index.html template.

    This function handles the root URL and renders the index.html template, which contains
    a form for users to input text for emotion analysis.
    """
    return render_template('index.html')

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector():
    """Analyze the emotion in the input text and return the result.

    This function analyzes the emotion in the text provided by the user in the POST request.
    It sends the text to the Emotion Detection API and displays the result on a web page.

    Returns:
        - If successful, it renders the result.html template with emotion analysis results.
        - If there is an error in the request or response, it renders the error.html template
          with an error message.
    """
    text_to_analyze = request.form.get('text_to_analyze')

    # Define headers and input data for the API request
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        # Send a POST request to the Emotion Detection API
        response = requests.post(EMOTION_API_URL, json=input_json, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for non-200 responses

        # Parse the API response and extract emotion scores
        response_json = response.json()
        emotions = response_json.get("emotion_scores", {})

        # Extract emotion scores
        emotion_scores = {
            'anger': emotions.get("anger", 0),
            'disgust': emotions.get("disgust", 0),
            'joy': emotions.get("joy", 0),
            'fear': emotions.get("fear", 0),
            'sadness': emotions.get("sadness", 0),
        }

        # Determine the dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        if dominant_emotion is None:
            # Handle the case where dominant_emotion is None
            return render_template(
                'error.html',
                error_message="Invalid text! Please try again."
            )

        # Create the desired output format
        result = {
            'anger': emotion_scores['anger'],
            'disgust': emotion_scores['disgust'],
            'joy': emotion_scores['joy'],
            'fear': emotion_scores['fear'],
            'sadness': emotion_scores['sadness'],
            'dominant_emotion': dominant_emotion,
        }

        # Render the result.html template with the analysis result
        return render_template('result.html', result=result, text_to_analyze=text_to_analyze)
    except requests.exceptions.RequestException as exception:
        # Handle exceptions that may occur during the API request
        error_message = f"Request Exception: {exception}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
