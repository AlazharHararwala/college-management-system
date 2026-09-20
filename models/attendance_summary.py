from database import db

class AttendanceSummary(db.Model):
    __tablename__ = 'attendance_summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    student_id = db.Column(
        db.String(20),
        db.ForeignKey('students.student_id'),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey('subjects.id'),
        nullable=False
    )

    subject_name = db.Column(
        db.String(200),
        nullable=False
    )

    total_classes = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    present_classes = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    attendance_percentage = db.Column(
        db.Float,
        nullable=False,
        default=0
    )