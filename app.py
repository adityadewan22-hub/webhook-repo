from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "OK", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    # For now, just acknowledge receipt
    return jsonify({"status": "received"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    # Temporary placeholder
    return jsonify([]), 200


if __name__ == "__main__":
    app.run(debug=True)
