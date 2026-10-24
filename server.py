"""Flask web server for the emotion detector."""
from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

INVALID_TEXT_MESSAGE = "Invalid text! Please try again!"


@app.route("/")
def render_index_page():
    """Render the home page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze the textToAnalyze query parameter and return a formatted sentence."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    # Handle blank input before calling the API.
    if not text_to_analyze.strip():
        return INVALID_TEXT_MESSAGE

    result = emotion_detector(text_to_analyze)

    # The API returned status 400, so emotion_detector gave back None values.
    if result["dominant_emotion"] is None:
        return INVALID_TEXT_MESSAGE

    return (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} "
        f"and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
