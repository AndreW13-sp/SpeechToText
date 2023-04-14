from pathlib import Path

import librosa
import soundfile as sf
import speech_recognition as sr
from flask import Flask, jsonify, render_template, request, send_file
from flask_cors import CORS, cross_origin
from gtts import gTTS

# Application Settings
app = Flask(__name__)
app.config["CORS_HEADERS"] = "application/json"
CORS(app, support_credentials=True)
file_name = "output/mic.flac"

# API Routes
@app.route("/", methods=["GET", "POST"])
@cross_origin(support_credentials=True)
def index():
   if request.method == "POST":
      data = request.get_json()
      myobj = gTTS(text=data.get("text"), lang="en", slow=False)
      myobj.save(file_name)
      return send_file(Path(file_name), mimetype="audio/wav", as_attachment=True, download_name=file_name)
   return render_template("home.html")


@app.route("/upload", methods=["POST"])
def handle_upload():
   file_input = request.files.get("speech_file")
   action = request.form.get("action")
   
   if action == "SpeechToText":
      recognizer = sr.Recognizer()

      x, _ = librosa.load(file_input, sr=16000)
      sf.write("output.wav", x, 16000, format="wav")

      with sr.AudioFile("./output.wav") as source:
         audio_text = recognizer.record(source)
         try:
            converted_text = recognizer.recognize_google(audio_data=audio_text, language="en-US")
            print(f"My Text: {converted_text}")
            return jsonify(transcribed_speech=converted_text)
         except Exception as e:
            return jsonify(error="Something went wrong when trying to convert stt")
   else:
      return jsonify(error="Unsupported action type!")

# ----------------------------------------------------------------------------
# Running main server here...
# ----------------------------------------------------------------------------
if __name__ == "__main__":
   app.run(debug=True)