from app import app
from models import db, User

# Create a Flask application context to access DB
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.is_admin = True
        db.session.commit()
        print("✅ Admin privileges granted to 'admin'")
    else:
        print("❌ User 'admin' not found. Please create the user first.")
