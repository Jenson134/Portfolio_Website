from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from email.message import EmailMessage
import smtplib
import json
import os

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=OPENAI_KEY)

ABOUT_ME_CONTEXT = """

You are an AI assistant that answers questions ONLY about Jenson.

Facts about Jenson:
- Name: Jenson Allaway
- Birthday: 29 November 2003
- Occupation: Part-time Pub Supervisor
- Interests: Rugby, Travel, Basketball, Coding
- Projects: Personal website, Recycling CNN, Handwritten forgery detection, Speech to text Web application
- Birth place: Port Elizabeth, South Africa
- Location: London, United Kingdom
- Preffered work location: London, Hertfordshire, Cambridge or Essex
- Education: Computer Science (Artificial Intelligence) at the University of Greenwich, graduated with a 2:1
- Coding Languages: Python, SQL, HTML/CSS, Bash, Delphi (Pascal), R Studio
- Spoken Languages: English (Mother tongue), Afrikaans (Fluent), Spanish (basic)
- Visa Status/ Right to Work: Obtains a Graduate Visa expiring September 2027


Do not invent facts. If information is not present here, say you do not know.
"""

SYSTEM_INSTRUCTIONS = """
You are a personal assistant for Jenson.

Rules:
- You may ONLY answer questions about Jenson.
- Use ONLY the provided context.
- If a question is not about Jenson, respond with:
  "I'm programmed to only answer questions about Jenson."
- If the question asks for information not in the context, respond with:
  "I don't have that information. Are there any other quetions I can answer?"
- Do not answer general knowledge, opinions, or hypothetical questions.
- You must avoid speculation about future plans, job searches, salary expectations, or availability.
"""

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_projects():
    with open(os.path.join(BASE_DIR, "projects.json")) as f:
        return json.load(f)["projects"]

def extract_stack():
    with open(os.path.join(BASE_DIR, "stack.json")) as f:
        return json.load(f)["stack"]


def handle_contact_form(email, subject, message):
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")

    if not sender_email or not sender_password:
        raise RuntimeError("SMTP credentials not configured")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = "jensonallaway03@gmail.com"
    msg["Subject"] = f"Contact Form: {subject}"
    msg["Reply-To"] = email

    msg.set_content(
        f"Sender Email: {email}\n\n"
        f"Message:\n{message}"
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(sender_email, sender_password)
        connection.send_message(msg)

def is_about_me(question: str) -> bool:
    keywords = ["you", "jenson", "your", "yourself", "projects", "background"]
    return any(word in question.lower() for word in keywords)

@app.route('/')
def home():
    stack = extract_stack()
    stack_size = len(stack)
    return render_template('index.html', stack=stack, stack_size=stack_size)

@app.route('/projects')
def projects():
    projects = extract_projects()
    number = len(projects)
    return render_template('projects.html', num=number, projects=projects)

@app.route('/education')
def education():
    return render_template('education.html')

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not is_about_me(user_message):
            return jsonify({
                "reply": "I can only answer questions about Jenson Allaway."
            })

    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_INSTRUCTIONS
                },
                {
                    "role": "system",
                    "content": ABOUT_ME_CONTEXT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        return jsonify({
            "reply": response.output_text
        })
    except Exception:
        return jsonify({
            "reply": "The assistant is temporarily unavailable."
        })


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/email', methods=['GET','POST'])
def email():
    error=None
    success=None
    if request.method == "POST":
        email = request.form.get("email")
        confirm_email = request.form.get("confirm_email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if email != confirm_email:
            error = "Email addresses do not match."
        else:
            handle_contact_form(
                email=email,
                subject=subject,
                message=message
            )
            success = "Email has been sent!"
        
    return render_template(
        'email.html',
        error=error,
        success=success
        )

if __name__ == '__main__':
    app.run()