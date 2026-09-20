from database import db


class Faculty(db.Model):
    __tablename__="faculty"

    id=db.Column(db.Integer, primary_key=True)
    faculty_id=db.Column(db.String(100), unique=True,nullable=False)

    full_name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)

    password = db.Column(db.String(255), nullable=False)
    phone=db.Column(db.String(30), nullable=False)
    
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))

    address = db.Column(db.String(200))
    department=db.Column(db.String(100))

    class_assigned = db.Column(db.String(100), nullable=True)
    join_date=db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False,default='Active')



    
    

    