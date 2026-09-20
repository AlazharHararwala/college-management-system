from database import db

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    
    address = db.Column(db.String(200))
    department = db.Column(db.String(200))
    
    semester = db.Column(db.Integer)
    enrollment_date = db.Column(db.Date)



    class_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default="Active")
    fee_status = db.Column(db.String(100),nullable=False,default="Unpaid")