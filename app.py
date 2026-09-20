from flask import Flask, render_template, request, session, redirect, url_for,flash
from database import db
from config import Config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from models.student import Student
from models.subjects import Subject
from models.attendance_entry import Attendance
from models.marks import Marks
from models.assigments import Assignment
from models.attendance_summary import AttendanceSummary



@app.route("/")
def index():
    return render_template('index.html')

# STUDENT ROUTES

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form['student_id']
        password = request.form['password']

        

        try:
            student = Student.query.filter_by(student_id=student_id).first()

            if not student or not check_password_hash(student.password, password):
                raise Exception("Invalid Student ID or Password")

            session['student_id'] = student.student_id
            return redirect(url_for('student_dashboard'))

        except Exception as e:
            return render_template('student/login.html',error=str(e))
    
    return render_template('student/login.html')



@app.route('/student/dashboard')
def student_dashboard():
    student_id=session.get('student_id')

    if not student_id:
        return redirect(url_for('student_login'))

    student=Student.query.filter_by(student_id=student_id).first()
    return render_template('student/dashboard.html',student=student)

@app.route('/student/profile')
def student_profile():
    student_id=session.get('student_id')

    if not student_id:
        return redirect(url_for('student_login'))

    student=Student.query.filter_by(student_id=student_id).first()

    return render_template('student/profile.html',student=student)


@app.route('/student/subjects')
def student_subjects():
    student_id=session.get('student_id')

    if not student_id:
        return redirect(url_for('student_login'))

    student=Student.query.filter_by(student_id=student_id).first()
    subjects=Subject.query.filter_by(semester=student.semester,department=student.department).all()

    
    return render_template('student/subjects.html',student=student,subjects=subjects)



@app.route('/student/attendance')
def student_attendance():

    student_id = session.get('student_id')

    if not student_id:
        return redirect(url_for('student_login'))

    student = Student.query.filter_by(student_id=student_id).first()

    attendance_records = Attendance.query.filter_by(student_id=student_id).all()
    attendance_data = {}

    for record in attendance_records:
        subject_id = record.subject_id

        if subject_id not in attendance_data:

            attendance_data[subject_id] = {
                'subject_name': record.subject_name,
                'total_classes': 0,
                'attended_classes': 0,
                'absent_classes': 0,
                'percentage': 0
            }

        attendance_data[subject_id]['total_classes'] += 1

        if record.status == 'Present':
            attendance_data[subject_id]['attended_classes'] += 1

        elif record.status == 'Absent':
            attendance_data[subject_id]['absent_classes'] += 1

    for subject in attendance_data.values():

        if subject['total_classes'] > 0:
            subject['percentage'] = (subject['attended_classes']/ subject['total_classes']) * 100

    return render_template('student/attendance.html',student=student,attendance_data=attendance_data.values())

@app.route('/student/marks')
def student_marks():
    student_id=session.get('student_id')
    if not student_id:
        return redirect(url_for('student_login'))

    student=Student.query.filter_by(student_id=student_id).first()
    marks=Marks.query.filter_by(student_id=student_id).all()
    
    return render_template('student/marks.html', student=student,marks=marks)


@app.route('/student/assignments')
def student_assignments():
    student_id=session.get('student_id')

    if not student_id:
        return redirect(url_for('student_login'))
    
    student=Student.query.filter_by(student_id=student_id).first()
    assignment=Assignment.query.filter_by(semester=student.semester,class_id=student.class_id).all()


    return render_template('student/assignments.html',student=student,assignment=assignment)

@app.route('/student/change-password',methods=['GET','POST'])
def student_change_password():

    student_id=session.get('student_id')

    if not student_id:
            return redirect(url_for('student_login'))
    
    student = Student.query.filter_by(student_id=student_id).first()
    error=None
    verify=False

    if request.method=='POST':

        action=request.form['action']

        try:

            if action=='verify':

                enterd_student_id=request.form['student_id']
                old_password=request.form['password']

                if enterd_student_id==student.student_id and check_password_hash(student.password, old_password): 
                    verify=True
                else:
                    raise Exception("Invalid ID or password")

            elif action=='change':
                student.password=generate_password_hash(request.form['new_password'])
                db.session.commit()
                return redirect(url_for('student_login'))

        except Exception as e:
            db.session.rollback()
            return render_template('student/change_password.html',error=str(e),verify=verify,student=student)
        
    return render_template('student/change_password.html',student=student,verify=verify)
                    

@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    return redirect(url_for('index'))


# FACULTY ROUTES
from models.faculty import Faculty
from models.attendance_entry import Attendance
from models.assigments import Assignment


@app.route('/faculty/login', methods=['GET','POST'])
def faculty_login():
    if request.method=='POST':
        faculty_id=request.form['faculty_id']
        password=request.form['password']

        
        try:
            faculty=Faculty.query.filter_by(faculty_id=faculty_id).first() 
            if not faculty or not check_password_hash(faculty.password, password):
                raise Exception("Invalid Faculty ID or Password")
        
            session['faculty_id'] = faculty.faculty_id
            return redirect(url_for('faculty_dashboard'))
        
        except Exception as e:
            return render_template('faculty/login.html',error=str(e))

    return render_template('faculty/login.html')

@app.route('/faculty/dashboard')
def faculty_dashboard():
    faculty_id=session.get('faculty_id')

    if not faculty_id:
        return redirect(url_for('faculty_login'))
    faculty=Faculty.query.filter_by(faculty_id=faculty_id).first()

    return render_template('faculty/dashboard.html',faculty=faculty)

@app.route('/faculty/profile')
def faculty_profile():
    faculty_id=session.get('faculty_id')

    if not faculty_id:
        return redirect(url_for('faculty_login'))
    
    faculty=Faculty.query.filter_by(faculty_id=faculty_id).first()

    return render_template('faculty/profile.html',faculty=faculty)


@app.route('/faculty/attendance/entry', methods=['GET', 'POST'])
def attendance_entry():

    faculty_id = session.get('faculty_id')

    if not faculty_id:
        return redirect(url_for('faculty_login'))

    faculty = Faculty.query.filter_by(faculty_id=faculty_id).first()

    class_ids = faculty.class_assigned.split(',')

    students = []

    if request.method == 'POST':
        action = request.form['action']

        if action == 'load':
            class_id = request.form['class_id']
            students = Student.query.filter_by(class_id=class_id).all()

        elif action == 'submit':
            class_id = request.form['class_id']
            subject_code = request.form['subject_code']
            attendance_date = request.form['attendance_date']
            class_time = request.form['class_time']

            subject = Subject.query.filter_by(subject_code=subject_code).first()

            students = Student.query.filter_by(class_id=class_id).all()

            for student in students:
                status = request.form[f"status_{student.student_id}"]

                attendance = Attendance(
                    student_id=student.student_id,
                    subject_id=subject.id,
                    subject_name=subject.subject_name,
                    class_id=class_id,
                    attendance_date=attendance_date,
                    class_time=class_time,
                    status=status
                )

                db.session.add(attendance)
            db.session.commit()
    return render_template('faculty/attendance.html',faculty=faculty,class_ids=class_ids,students=students)

@app.route('/faculty/assignments',methods=['GET','POST'])
def create_assignment():
    faculty_id=session.get('faculty_id')

    if not faculty_id:
        return redirect(url_for('faculty_login'))

    faculty = Faculty.query.filter_by(faculty_id=faculty_id).first()
    class_ids = faculty.class_assigned.split(',')

    if request.method=='POST':
        subject_code=request.form['subject_code']
        subject_name=request.form['subject_name']
        semester = request.form['semester']
        class_id = request.form['class_id']
        title=request.form['title']
        description=request.form['description']

        try:
            due_date = datetime.strptime(request.form['due_date'],'%Y-%m-%d').date()

            assignment=Assignment(
                subject_code=subject_code,
                subject_name=subject_name,
                semester=semester,
                class_id=class_id,
                title=title,
                description=description,
                due_date=due_date
            )
            db.session.add(assignment)
            db.session.commit()

            flash("Assignment created successfully!", "success")
            return redirect(url_for('create_assignment'))

        except Exception as e:
            db.session.rollback()
            flash(f"Could not create assignment: {str(e)}", "error")

    return render_template('faculty/assignments.html',class_ids=class_ids)


@app.route('/faculty/assignment/history',methods=['GET','POST'])
def assignment_history():
    faculty_id=session.get('faculty_id')

    if not faculty_id:
        return redirect(url_for('faculty_login'))

    faculty = Faculty.query.filter_by(faculty_id=faculty_id).first()
    class_id = faculty.class_assigned.split(',')
    assignment = []

    if request.method=='POST':
        action=request.form['action']

        if action=='load':
            selected_class=request.form['class_id']
            semester=request.form['semester']

            assignment=Assignment.query.filter_by(class_id=selected_class,semester=semester).all()

    return render_template('faculty/assignment_history.html',faculty=faculty,class_id=class_id,assignment=assignment)


@app.route('/faculty/marks', methods=['GET', 'POST'])
def view_marks():

    faculty_id = session.get('faculty_id')

    if not faculty_id:
        return redirect(url_for('faculty_login'))

    faculty = Faculty.query.filter_by(faculty_id=faculty_id).first()

    class_ids = faculty.class_assigned.split(',')
    students = []
    marks=[]

    if request.method == 'POST':
        action = request.form['action']

        if action == 'load':

            class_id = request.form['class_id']
            semester = request.form['semester']
            subject_name=request.form['subject_name']

            marks = (Marks.query.join(Student, Marks.student_id == Student.student_id)
                     .filter(Student.class_id == class_id,Marks.subject_name == subject_name,Marks.semester == semester).all())

    return render_template('faculty/marks.html',faculty=faculty,class_ids=class_ids,students=students,marks=marks)


@app.route('/faculty/marks/update', methods=['GET', 'POST'])
def update_marks():

    faculty_id=session.get('faculty_id')

    if not faculty_id:
        return redirect(url_for('faculty_login'))
    
    faculty = Faculty.query.filter_by(faculty_id=faculty_id).first()

    
    class_ids = faculty.class_assigned.split(',')

    if request.method=='POST':
        action=request.form['action']

        if action=='save':
            class_id = request.form['class_id']
            semester = request.form['semester']
            student_id = request.form['student_id']
            subject_code = request.form['subject_code']

            subject = Subject.query.filter_by(subject_code=subject_code).first()
            if not subject:
                flash("Invalid subject code", "error")
                return redirect(url_for('update_marks'))


            # Note: no restriction on which subjects this faculty can enter marks for —
            # any faculty can currently submit marks for any valid subject_code,
            # not just subjects they actually teach. Faculty.subjects_taught was considered
            # and deferred; revisit if per-faculty subject restriction becomes necessary.

            subject_id = subject.id
            subject_name = subject.subject_name

            midsem_marks = request.form['midsem_marks']
            internal_marks = request.form['internal_marks']
            endsem_marks = request.form['endsem_marks']

            student = Student.query.filter_by(student_id=student_id,class_id=class_id,semester=semester).first()

            if not student:

                flash("Student not found in class or semester", "error")
                return redirect(url_for('update_marks'))
            
            mark = Marks.query.filter_by(student_id=student_id,subject_id=subject_id,semester=semester).first()

            if mark:
                mark.midsem_marks=midsem_marks
                mark.internal_marks=internal_marks
                mark.endsem_marks=endsem_marks
            else:
                mark=Marks(
                    student_id=student_id,
                    subject_name=subject_name,
                    subject_id=subject_id,
                    semester=semester,
                    midsem_marks=midsem_marks,
                    internal_marks=internal_marks,
                    endsem_marks=endsem_marks
                )
                db.session.add(mark)
            db.session.commit()
            
            flash("Marks saved successfully!","success")
            return redirect(url_for('update_marks'))
        
    return render_template('faculty/enter_marks.html',faculty=faculty,class_ids=class_ids)


@app.route('/faculty/change-password', methods=['GET','POST'])
def faculty_change_password():

    faculty_id=session.get('faculty_id')
    
    if not faculty_id:
            return redirect(url_for('faculty_login'))

    faculty=Faculty.query.filter_by(faculty_id=faculty_id).first()
    error=None
    verify=False
    try:
        if request.method=='POST':

            action=request.form['action']

            if action=='verify':
                enterd_faculty_id=request.form['faculty_id']
                old_password=request.form['password']

                if enterd_faculty_id==faculty.faculty_id and check_password_hash(faculty.password, old_password):
                    verify=True
                else:
                    raise Exception("Invalid ID or Password")

            elif action=='change':
                faculty.password=generate_password_hash(request.form['new_password'])
                db.session.commit()
                return redirect(url_for('faculty_login'))
    except Exception as e:
        db.session.rollback()
        return render_template('faculty/change_password.html', error=str(e),verify=verify,faculty=faculty)

    return render_template('faculty/change_password.html',verify=verify,faculty=faculty)
    

@app.route('/faculty/logout')
def faculty_logout():
    session.pop('faculty_id', None)
    return redirect(url_for('index'))


# ADMIN ROUTES

from models.admin import Admin
from models.fees import Fees

@app.route('/admin/login',methods=['GET','POST'])
def admin_login():

    if request.method=='POST':
        admin_id=request.form['admin_id']
        password=request.form['password']

        admin=Admin.query.filter_by(admin_id=admin_id).first() 
        try:
            if not admin or not check_password_hash(admin.password, password):
                raise Exception("Invalid Admin ID or password")

            session['admin_id']=admin.admin_id
            return redirect(url_for('admin_dashboard'))
        
        except Exception as e:
            return render_template('admin/login.html',error=str(e))
        
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():

    admin_id=session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))
    
    admin=Admin.query.filter_by(admin_id=admin_id).first()
    return render_template('admin/dashboard.html',admin=admin) 

@app.route('/admin/profile')
def admin_profile():
    admin_id=session.get('admin_id')
    
    if not admin_id:
        return redirect(url_for('admin_login'))

    admin=Admin.query.filter_by(admin_id=admin_id).first()
    return render_template('admin/profile.html',admin=admin)
    

@app.route('/admin/student-management')
def student_management():

    admin_id=session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))
    
    return render_template('admin/student_management/student.html')

@app.route('/admin/faculty-management')
def faculty_management():

    admin_id = session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))

    return render_template('admin/faculty_managment/faculty.html')

@app.route('/admin/add-subject',methods=['GET','POST'])
def add_subject():
    admin_id = session.get('admin_id')
    
    if not admin_id:
        return redirect(url_for('admin_login'))


    if request.method=='POST':
        
        subject_code=request.form['subject_code']
        subject_name=request.form['subject_name']
        semester=request.form['semester']
        department=request.form['department']
        credits=request.form['credits']

        

        try:
            subjects = Subject.query.filter((Subject.subject_code == subject_code) | (Subject.subject_name == subject_name)).first()
            if subjects:
                    raise Exception("Subject ID and name already exists")
            
            subject=Subject(
                subject_code=subject_code,
                subject_name=subject_name,
                semester=semester,
                department=department,
                credits=credits
            )
            db.session.add(subject)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return render_template('admin/add_subject.html',error=str(e))
        
    return render_template('admin/add_subject.html')


@app.route('/admin/delete-subject',methods=['GET','POST'])
def delete_subject():
    admin_id = session.get('admin_id')
        
    if not admin_id:
        return redirect(url_for('admin_login'))

    subject=None

    if request.method=='POST':
        subject_code=request.form['subject_code']
        action=request.form['action']

        if action=='delete':
            try:
                subject=Subject.query.filter_by(subject_code=subject_code).first()

                if not subject:
                    raise Exception("Subject does not exists")

                db.session.delete(subject)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return render_template('admin/delete_subject.html',subject=subject,error=str(e))

    return render_template('admin/delete_subject.html',subject=subject)



#Admin-Student Management Routes

@app.route('/admin/add-student', methods=['GET', 'POST'])
def add_student():

    admin_id = session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':

        student_id = request.form['student_id']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        date_of_birth = datetime.strptime(request.form['date_of_birth'],'%Y-%m-%d').date()
        gender = request.form['gender']
        address = request.form['address']
        department = request.form['department']
        semester = request.form['semester']
        enrollment_date = datetime.strptime(request.form['enrollment_date'],'%Y-%m-%d').date()
        class_id = request.form['class_id']
        status = request.form['status']

        try:
            existing_student = Student.query.filter((Student.student_id == student_id) | (Student.email == email)).first()

            if existing_student:
                raise Exception("Student ID or Email already exists")

            student = Student(
                student_id=student_id,
                full_name=full_name,
                email=email,
                password=generate_password_hash(password), 
                phone=phone,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address,
                department=department,
                semester=semester,
                enrollment_date=enrollment_date,
                class_id=class_id,
                status=status
            )

            db.session.add(student)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return render_template('admin/student_management/add_student.html',error=str(e))

    return render_template('admin/student_management/add_student.html')

@app.route('/admin/delete-student', methods=['GET', 'POST'])
def delete_student():

    admin_id = session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':

        student_id = request.form['student_id']
        admin_password=request.form['password']

        try:
            admin = Admin.query.filter_by(admin_id=admin_id).first()
            if not admin or not check_password_hash(admin.password, admin_password):
                raise Exception("Admin password is incorrect")

            student = Student.query.filter_by(student_id=student_id).first()
            if not student:
                raise Exception("Student not found")

            Attendance.query.filter_by(student_id=student_id).delete()
            AttendanceSummary.query.filter_by(student_id=student_id).delete()
            Marks.query.filter_by(student_id=student_id).delete()
            Fees.query.filter_by(student_id=student_id).delete()

            db.session.delete(student)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return render_template('admin/student_management/delete_student.html',error=str(e))

    return render_template('admin/student_management/delete_student.html')


@app.route('/admin/view-students',methods=['GET','POST'])
def student_details():
    admin_id = session.get('admin_id')
    
    if not admin_id:
        return redirect(url_for('admin_login'))

    students=[]

    if request.method=="POST":
        action=request.form['action']

        student_id=request.form['student_id']
        semester=request.form['semester']
        class_id=request.form['class_id']
        department=request.form['department']
        status=request.form['status']

        if action=='load':
            students=Student.query

            if student_id:
                students=students.filter_by(student_id=student_id)
            if class_id:
                students=students.filter_by(class_id=class_id)
            if department:
                students=students.filter_by(department=department)
            if semester:
                students=students.filter_by(semester=semester)
            if status:
                students=students.filter_by(status=status)

            students=students.all()
        
    return render_template('admin/student_management/view_students.html',students=students)


@app.route('/admin/update-student', methods=['GET', 'POST'])
def update_student():

    admin_id = session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))

    student = None
    error = None
    success = None

    if request.method == 'POST':

        action = request.form['action']

        try:
            if action == 'find':

                student_id = request.form['student_id']
                student = Student.query.filter_by(student_id=student_id).first()

                if not student:
                    raise Exception("Student not found")

            elif action == 'update':

                student_id = request.form['student_id']
                student = Student.query.filter_by(student_id=student_id).first()

                if not student:
                    raise Exception("Student not found")

                else:
                    student.full_name = request.form['full_name']
                    student.email = request.form['email']
                    student.phone = request.form['phone']
                    student.date_of_birth = request.form['date_of_birth']
                    student.gender = request.form['gender']
                    student.address = request.form['address']
                    student.department = request.form['department']
                    student.semester = request.form['semester']
                    student.enrollment_date = request.form['enrollment_date']
                    student.class_id = request.form['class_id']
                    student.status = request.form['status']

                    db.session.commit()

        except Exception as e:
            db.session.rollback()

            return render_template('admin/student_management/update_student.html',student=student,error=str(e))

    return render_template('admin/student_management/update_student.html',student=student)


#Admin-Faculty Routes

@app.route('/admin/add-faculty' , methods=['GET','POST'])
def add_faculty():

    admin_id=session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))

    if request.method=='POST':

        faculty_id=request.form['faculty_id']
        full_name=request.form['full_name']
        email=request.form['email']
        password=request.form['password']
        phone=request.form['phone']
        date_of_birth=datetime.strptime(request.form['date_of_birth'],'%Y-%m-%d')
        gender=request.form['gender']
        address=request.form['address']
        department=request.form['department']
        join_date=datetime.strptime(request.form['join_date'],'%Y-%m-%d')
        status=request.form['status']
        class_assigned=request.form['class_assigned']

        try:
            existing_faculty=Faculty.query.filter((Faculty.faculty_id==faculty_id) | (Faculty.email==email)).first()

            if existing_faculty:
                raise Exception("Faculty already exsists")

            faculty=Faculty(
                faculty_id=faculty_id,
                full_name=full_name,
                email=email,
                password=generate_password_hash(password),
                phone=phone,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address,
                department=department,
                join_date=join_date,
                status=status,
                class_assigned=class_assigned
            )
            db.session.add(faculty)
            db.session.commit() 
            
        except Exception as e:
            db.session.rollback()
            return render_template('admin/faculty_managment/add_faculty.html',error=str(e))
        
    return render_template('admin/faculty_managment/add_faculty.html')


@app.route('/admin/delete-faculty', methods=['GET', 'POST'])
def delete_faculty():

    admin_id = session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':

        faculty_id= request.form['faculty_id']
        admin_password=request.form['password']

        try:
            admin = Admin.query.filter_by(admin_id=admin_id).first()
            if not admin or not check_password_hash(admin.password, admin_password):
                raise Exception("Admin password is incorrect")

            faculty = Faculty.query.filter_by(faculty_id=faculty_id).first()
            if not faculty:
                raise Exception("Faculty not found")

            db.session.delete(faculty)
            db.session.commit()


        except Exception as e:
            db.session.rollback()
            return render_template('admin/faculty_managment/delete_faculty.html',error=str(e))

    return render_template('admin/faculty_managment/delete_faculty.html')


@app.route('/admin/view-faculty',methods=['GET','POST'])
def view_faculty():
    admin_id = session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))
    faculty=[]

    if request.method=='POST':
        action=request.form['action']

        faculty_id=request.form['faculty_id']
        department=request.form['department']
        status=request.form['status']
        gender=request.form['gender']
        class_assigned=request.form['class_assigned']

        if action=='load':
            faculty=Faculty.query

            if faculty_id:
                faculty=faculty.filter_by(faculty_id=faculty_id)
            if department:
                faculty=faculty.filter_by(department=department)
            if status:
                faculty=faculty.filter_by(status=status)
            if gender:
                faculty=faculty.filter_by(gender=gender)
            if class_assigned:
                faculty = faculty.filter(Faculty.class_assigned.contains(class_assigned))

            faculty=faculty.all()
    return render_template('admin/faculty_managment/view_faculty.html',faculty=faculty)
            

@app.route('/admin/update_faculty',methods=['GET','POST'])
def update_faculty():
    admin_id = session.get('admin_id')
    
    if not admin_id:
        return redirect(url_for('admin_login'))
    faculty=[]

    if request.method=='POST':

        action=request.form['action']

        try:
            if action=='find':
                faculty_id=request.form['faculty_id']
                faculty=Faculty.query.filter_by(faculty_id=faculty_id).first()

                if not faculty:
                    raise Exception("Faculty not found")
                
            elif action=='update':
                faculty_id=request.form['faculty_id']
                faculty=Faculty.query.filter_by(faculty_id=faculty_id).first()

                if not faculty:
                    raise Exception("Faculty not found")
                else:
                    faculty.full_name=request.form['full_name']
                    faculty.email=request.form['email']
                    faculty.phone=request.form['phone']
                    faculty.date_of_birth=request.form['date_of_birth']
                    faculty.gender=request.form['gender']
                    faculty.address=request.form['address']
                    faculty.department=request.form['department']
                    faculty.status=request.form['status']
                    faculty.class_assigned=request.form['class_assigned']

                    db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template('admin/faculty_managment/update_faculty.html', faculty=faculty,error=str(e))

    return render_template('admin/faculty_managment/update_faculty.html',faculty=faculty)


@app.route('/admin/fees-managment', methods=['GET', 'POST'])
def fees_managment():

    admin_id = session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))

    fees = []

    if request.method == 'POST':

        action = request.form.get('action')

        if action == 'load':

            student_id = request.form.get('student_id')
            class_id = request.form.get('class_id')
            semester = request.form.get('semester')
            department = request.form.get('department')
            status = request.form.get('status')

            fees = Fees.query

            if student_id:
                fees = fees.filter_by(student_id=student_id)

            if class_id:
                fees = fees.filter_by(class_id=class_id)

            if semester:
                fees = fees.filter_by(semester=int(semester))

            if department:
                fees = fees.filter_by(department=department)

            if status:
                fees = fees.filter_by(status=status)

            fees = fees.all()

    return render_template('admin/fees_managment.html',fees=fees)


@app.route('/admin/update-fees', methods=['GET', 'POST'])
def update_fees():

    admin_id = session.get('admin_id')

    if not admin_id:
        return redirect(url_for('admin_login'))

    fees = None
    student = None
    error=None

    if request.method == 'POST':
        action = request.form.get('action')

        try:

            if action == 'find':

                student_id = request.form.get('student_id')
                student = Student.query.filter_by(student_id=student_id).first()

                if not student:
                    raise Exception("Student not found")

                fees = Fees.query.filter_by(student_id=student_id).first()

            elif action == 'update':

                student_id = request.form.get('student_id')
                student = Student.query.filter_by(student_id=student_id).first()

                if not student:
                    raise Exception("Student not found")
                
                fee = Fees.query.filter_by(student_id=student_id).first()

                if not fee:
                    
                    fee = Fees(
                        student_id=student.student_id,
                        full_name=student.full_name,
                        department=student.department,
                        class_id=student.class_id,
                        semester=student.semester,
                        total_fees=request.form.get('total_fees'),
                        status=request.form.get('status'),
                    )

                    db.session.add(fee)

                else:
                    
                    fee.total_fees = request.form.get('total_fees')
                    fee.status = request.form.get('status')

                db.session.commit()
                return redirect(url_for('update_fees'))

        except Exception as e:
            db.session.rollback()
            return render_template('admin/update_fees.html',fees=fees,student=student,error=str(e))

    return render_template('admin/update_fees.html',fees=fees,student=student)

                    
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)