from database import db

class Marks(db.Model):
    __tablename__ = "marks"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(200), db.ForeignKey("students.student_id"), nullable=False)
    subject_name=db.Column(db.String(200),nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    semester=db.Column(db.String(100),nullable=False)
    midsem_marks = db.Column(db.String(20), nullable=True)
    internal_marks= db.Column(db.String(20), nullable=True)
    endsem_marks=db.Column(db.String(20), nullable=True)