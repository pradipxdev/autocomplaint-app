from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from flask_mail import Mail, Message
import io
import os
import openai

app = Flask(__name__)

# Configure Flask-Mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email@gmail.com',        # 🔁 Replace with your Gmail
    MAIL_PASSWORD='your_app_password',           # 🔁 Replace with your Gmail App Password
)
mail = Mail(app)

# OpenAI Key
openai.api_key = "your_openai_api_key"  # 🔁 Replace with your OpenAI API key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        issue = request.form['issue']
        against = request.form['against']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']
        email = request.form['email']

        # ChatGPT generated content
        prompt = f"Write a legal complaint in simple English about {issue} against {against} that occurred on {date} at {location}. Description: {description}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        complaint_text = response.choices[0].message.content.strip()

        # Email the complaint
        if email:
            msg = Message('Your Complaint Document', sender='your_email@gmail.com', recipients=[email])
            msg.body = complaint_text
            mail.send(msg)

        # Generate PDF
        pdf_buffer = io.BytesIO()
        p = canvas.Canvas(pdf_buffer)
        p.drawString(100, 800, "AutoComplaint Generator")
        p.drawString(100, 780, f"Date: {date}")
        p.drawString(100, 760, f"Location: {location}")
        p.drawString(100, 740, f"Issue: {issue}")
        p.drawString(100, 720, f"Against: {against}")
        p.drawString(100, 700, "Complaint:")
        text_object = p.beginText(100, 680)
        for line in complaint_text.split('\n'):
            text_object.textLine(line)
        p.drawText(text_object)
        p.showPage()
        p.save()
        pdf_buffer.seek(0)

        return send_file(pdf_buffer, as_attachment=True, download_name="complaint.pdf")

    return render_template('index.html')
