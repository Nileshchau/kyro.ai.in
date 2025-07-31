import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route("/", methods=["GET", "HEAD"])
def home():
    return render_template("index.html")

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "creator": "TEAM KYRO",
        "message": "Welcome to the KYRO.AI intelligent assistant system.",
        "status": "KYRO.AI online"
    })

@app.route("/ask", methods=["POST"])
def ask_kyro():
    data = request.get_json()
    message = data.get("message", "")
    try:
        if "gemini" in message.lower():
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(message)
            reply = getattr(response, 'text', 'Gemini did not return text')
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}]
            )
            reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"KYRO Error: {str(e)}"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
