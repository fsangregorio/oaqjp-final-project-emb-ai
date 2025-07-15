"""Flask app for emotion detection using Watson API."""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route():
    """Handle emotion detection requests."""
    text_to_analyze = request.args.get("textToAnalyze")

    if not text_to_analyze:
        return "No text provided.", 400

    try:
        result = emotion_detector(text_to_analyze)

        if result.get("dominant_emotion") is None:
            return "Invalid text! Please try again!", 400

        html_response = (
            f"<strong>Anger:</strong> {result['anger']:.4f}<br>"
            f"<strong>Disgust:</strong> {result['disgust']:.4f}<br>"
            f"<strong>Fear:</strong> {result['fear']:.4f}<br>"
            f"<strong>Joy:</strong> {result['joy']:.4f}<br>"
            f"<strong>Sadness:</strong> {result['sadness']:.4f}<br>"
            f"<strong>Dominant Emotion:</strong> <em>{result['dominant_emotion']}</em>"
        )
        return html_response

    except Exception as error:  # pylint: disable=broad-except
        app.logger.error("Error in emotion_detector_route: %s", error)
        return "An error occurred.", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
