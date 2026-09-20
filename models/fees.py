from database import db

class Fees(db.Model):
    __tablename__ = "fees"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    class_id = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    semester = db.Column(db.Integer)
    total_fees = db.Column(db.Integer)

    status = db.Column(db.String(100), nullable=False, default="Unpaid")