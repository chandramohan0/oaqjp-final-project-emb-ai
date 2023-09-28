from flask import Flask, request, render_template, jsonify
import requests

app = Flask("Emotion Detector")

EMOTION_API_URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector():
    text_to_analyze = request.form.get('text_to_analyze')

    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(EMOTION_API_URL, json=input_json, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 responses

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
            # Handle case where dominant_emotion is None
            return render_template('error.html', error_message="Invalid text! Please try again.")

        # Create the desired output format
        result = {
            'anger': emotion_scores['anger'],
            'disgust': emotion_scores['disgust'],
            'joy': emotion_scores['joy'],
            'fear': emotion_scores['fear'],
            'sadness': emotion_scores['sadness'],
            'dominant_emotion': dominant_emotion,
        }

        return render_template('result.html', result=result, text_to_analyze=text_to_analyze)
    except requests.exceptions.RequestException as e:
        error_message = f"Request Exception: {e}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
