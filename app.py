import os
import io
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas
from config import Config
from models import db, User, Complaint
from forms import LoginForm, SignupForm, ComplaintForm
from auth import auth

# ===================== ⚙️ CONFIG =====================

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail = Mail(app)
app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ===================== 🔥 SMART COMPLAINT =====================

def generate_complaint(data, lang='en'):
    if lang == 'en':
        return f"""
        Dear Sir/Madam,

        I, {data['name']}, wish to lodge a complaint regarding "{data['issue']}" against "{data['against']}".
        The issue occurred on {data['date']} at {data['location']}.

        Description: {data['description']}

        Kindly take the necessary action.

        Regards,
        {data['name']}
        """
    elif lang == 'hi':
        return f"""
        मान्यवर,

        मैं, {data['name']}, "{data['against']}" के खिलाफ "{data['issue']}" की शिकायत दर्ज कराना चाहता/चाहती हूँ।
        यह घटना {data['date']} को {data['location']} में हुई थी।

        विवरण: {data['description']}

        कृपया आवश्यक कार्रवाई करें।

        धन्यवाद,
        {data['name']}
        """

# ===================== 🏠 INDEX =====================

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

# ===================== 📤 EXPORT PDF =====================

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.form
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "AutoComplaint Report")
    p.line(100, 795, 500, 795)
    p.drawString(100, 770, f"Date: {data['date']}")
    p.drawString(100, 750, f"Location: {data['location']}")
    p.drawString(100, 730, f"From: {data['name']}")
    p.drawString(100, 710, f"Issue: {data['issue']}")
    p.drawString(100, 690, f"Against: {data['against']}")
    p.drawString(100, 670, "Description:")
    text_object = p.beginText(100, 650)
    text_object.setFont("Helvetica", 11)
    text_object.textLines(data['description'])
    p.drawText(text_object)

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="complaint.pdf", mimetype='application/pdf')

# ===================== 📧 EMAIL =====================

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.form
    user_email = request.form['email']

    subject = "🚨 Complaint Registered Successfully"
    body = f"""
Hello {data['name']},

Your complaint regarding "{data['issue']}" against "{data['against']}" has been registered successfully.

📍 Location: {data['location']}
🗓️ Date: {data['date']}
📝 Description: {data['description']}

We will take action as soon as possible.

Thank you,
AutoComplaint Team
    """

    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[user_email])
    msg.body = body

    try:
        mail.send(msg)
        return '✅ Email sent successfully!'
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"

# ===================== 🧑 USER DASHBOARD =====================

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ComplaintForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        complaint = Complaint(
            issue=form.issue.data,
            against=form.against.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            language='English',
            filename=filename,
            user=current_user
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('dashboard.html', form=form, complaints=complaints)

# ===================== 🛡️ ADMIN DASHBOARD =====================

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        flash("🚫 Access denied. Admins only!", "danger")
        return redirect(url_for('dashboard'))

    all_complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    users = User.query.all()
    return render_template('admin_dashboard.html', complaints=all_complaints, users=users)

# ===================== 📂 FILE SERVE =====================

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ===================== 🚀 RUN =====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
