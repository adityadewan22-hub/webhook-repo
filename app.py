from flask import Flask
import logging
from config import PORT
from routes.webhook import webhook_bp
from routes.events import events_bp
from routes.ui import ui_bp
from loggin_config import setup_logging


setup_logging()

app = Flask(__name__)

app.register_blueprint(webhook_bp)
app.register_blueprint(events_bp)
app.register_blueprint(ui_bp)


@app.route("/", methods=["GET"])
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
