from database import db

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(20), unique=True, nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'),nullable=False)

    date_of_birth=db.Column(db.Date)
    phone=db.Column(db.String(20),nullable=False)