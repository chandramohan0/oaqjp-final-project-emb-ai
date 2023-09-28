import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    response = requests.post(url, json=input_json, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        emotions = response_json.get("emotion_scores", {})

        # Extract emotion scores
        anger_score = emotions.get("anger", 0)
        disgust_score = emotions.get("disgust", 0)
        joy_score = emotions.get("joy", 0)
        fear_score = emotions.get("fear", 0)
        sadness_score = emotions.get("sadness", 0)

        # Determine the dominant emotion
        emotion_scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'joy': joy_score,
            'fear': fear_score,
            'sadness': sadness_score,
        }
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        # Create the desired output format
        result = {
            'anger': anger_score,
            'disgust': disgust_score,
            'joy': joy_score,
            'fear': fear_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion,
        }
        return result
    elif response.status_code == 400:
        # Handle blank entries by returning a dictionary with all values as None
        result = {
            'anger': None,
            'disgust': None,
            'joy': None,
            'fear': None,
            'sadness': None,
            'dominant_emotion': None,
        }
        return result
    else:
        print("Error:", response.text)
        return None
