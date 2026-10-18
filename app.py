import os
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JSON_SORT_KEYS"] = False

# Demo responses only. Connect a real AI provider on the server to enable live AI.
def demo_reply(message: str) -> str:
    text = message.lower()
    if any(word in text for word in ["landing", "business", "website"]):
        return ("A strong landing page usually includes a clear hero section, services, benefits, "
                "a call to action, and a contact form. Tell me your audience and main goal.")
    if any(word in text for word in ["portfolio", "project", "github"]):
        return ("A portfolio can highlight your introduction, skills, projects, and contact details. "
                "You can share project links and screenshots to plan the layout.")
    if any(word in text for word in ["ai", "chatbot", "automation"]):
        return ("A real AI assistant needs a server-side AI API integration. This starter currently "
                "uses safe demo replies; no API key is needed.")
    if any(word in text for word in ["price", "cost", "budget"]):
        return ("Project pricing depends on page sections, design complexity, and required features. "
                "Share the scope first so the work can be estimated clearly.")
    return ("Thanks for your message! I can help you plan a website. Tell me the purpose, audience, "
            "preferred style, and sections you need.")

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Brandly backend", "time": datetime.now(timezone.utc).isoformat()})

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please enter a message."}), 400
    if len(message) > 1000:
        return jsonify({"error": "Message must be 1000 characters or fewer."}), 400
    return jsonify({"reply": demo_reply(message.strip()), "mode": "demo"})

@app.post("/api/contact")
def contact():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    message = str(data.get("message", "")).strip()
    if not name or not email or not message:
        return jsonify({"error": "Please fill in your name, email, and message."}), 400
    if len(name) > 100 or len(email) > 254 or len(message) > 3000:
        return jsonify({"error": "One or more fields are too long."}), 400
    # Starter behavior: acknowledge the message. It is not stored or emailed yet.
    # Add database/email delivery before using this endpoint for real customer leads.
    return jsonify({
        "success": True,
        "message": "Thanks! The form is connected to the backend demo. Message storage/email delivery is not configured yet."
    }), 200

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
