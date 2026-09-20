from database import db
from datetime import date

class Attendance(db.Model):

    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20),db.ForeignKey('students.student_id'),nullable=False)

    subject_name = db.Column(db.String(200),nullable=True)
    subject_id = db.Column(db.Integer,db.ForeignKey('subjects.id'),nullable=False)
    class_id=db.Column(db.String(100),nullable=False)

    class_time = db.Column(db.String(20), nullable=True)
    attendance_date = db.Column(db.Date,nullable=False)
    status = db.Column(db.Enum('Present', 'Absent'),nullable=False)
    