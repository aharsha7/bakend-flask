from flask import request, jsonify, current_app
from flask_mail import Message
import os

def handle_send_mail(mail):
    try:
        to = request.form.get("to")
        subject = request.form.get("subject")
        text = request.form.get("text")
        file = request.files.get("file")

        if not to or not subject or not text:
            return jsonify({"message": "Missing required fields"}), 400

        if not to.endswith("@gmail.com"):
            return jsonify({"message": "Only Gmail addresses are supported"}), 400

        msg = Message(subject=subject, recipients=[to], body=text)

        if file:
            filename = file.filename
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path, "rb") as f:
                msg.attach(filename, file.content_type, f.read())
            os.remove(file_path)

        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        print("Email sending error:", str(e))
        return jsonify({"message": "Failed to send email", "error": str(e)}), 500
