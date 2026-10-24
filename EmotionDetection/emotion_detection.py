"""Emotion detection using the Watson NLP emotion model."""
import json

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return the five emotion scores and the dominant emotion for the text.

    If the API responds with status 400 (for example, blank input),
    every value in the returned dictionary is None.
    """
    input_json = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, json=input_json, headers=HEADERS, timeout=30)

    if response.status_code == 400:
        result = {emotion: None for emotion in EMOTIONS}
        result["dominant_emotion"] = None
        return result

    formatted = json.loads(response.text)
    emotions = formatted["emotionPredictions"][0]["emotion"]

    result = {emotion: emotions[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(emotions, key=emotions.get)
    return result
