from database import db

class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(200), nullable=False)
    subject_name=db.Column(db.String(200), nullable=False)
    semester=db.Column(db.String(20), nullable=False)
    class_id=db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())