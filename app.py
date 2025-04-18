from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from models import db, User
from auth import auth
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autocomplaint.db'
db.init_app(app)

# Authentication setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
app.register_blueprint(auth)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Smart GPT-like complaint generator
def generate_complaint(data, lang='en'):
    if lang == 'en':
        return f"""
        Dear Sir/Madam,

        I, {data['name']}, wish to lodge a complaint regarding "{data['issue']}" against "{data['against']}".
        The issue occurred on {data['date']} at {data['location']}. Details: {data['description']}

        I request you to kindly take necessary action.

        Regards,  
        {data['name']}
        """
    elif lang == 'hi':
        return f"""
        मान्यवर,

        मैं, {data['name']}, {data['against']} के खिलाफ "{data['issue']}" की शिकायत दर्ज कराना चाहता/चाहती हूँ।
        यह घटना {data['date']} को {data['location']} में हुई थी। विवरण: {data['description']}

        कृपया आवश्यक कार्रवाई करें।

        धन्यवाद,  
        {data['name']}
        """

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "issue": request.form['issue'],
            "against": request.form['against'],
            "date": request.form['date'],
            "location": request.form['location'],
            "description": request.form['description'],
            "lang": request.form['language']
        }
        complaint_text = generate_complaint(data, data['lang'])
        return render_template('complaint.html', complaint=complaint_text, data=data)
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/download', methods=['POST'])
def download_pdf():
    text = request.form['complaint']
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Disposition'] = 'attachment; filename=complaint.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response

@app.route('/send_email', methods=['POST'])
def send_email():
    email_address = request.form['email']
    complaint_text = request.form['complaint']

    msg = EmailMessage()
    msg.set_content(complaint_text)
    msg['Subject'] = 'Your AutoComplaint'
    msg['From'] = 'youremail@example.com'  # Change this
    msg['To'] = email_address

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('youremail@example.com', 'yourpassword')  # Change this
            smtp.send_message(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return f"Error sending email: {str(e)}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
