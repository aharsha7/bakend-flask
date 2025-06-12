from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from config import Config
from mailer.send_mail import handle_send_mail
import os

app = Flask(__name__)
app.config.from_object(Config)

CORS(app) 
mail = Mail(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/api/mail/send", methods=["POST"])
def send_mail():
    return handle_send_mail(mail)

@app.route("/")
def index():
    return "📬 Flask Mail Sender API is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   
    app.run(host="0.0.0.0", port=port)         
