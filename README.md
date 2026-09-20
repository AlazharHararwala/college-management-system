# 🎓 CampusHub - College Management System

CampusHub is a role-based full-stack College Management System built using **Flask**, **SQLAlchemy**, and **MySQL**. It provides separate portals for **students**, **faculty**, and **admins** to manage attendance, marks, assignments, fees, and student and faculty records through a clean and user-friendly interface.

This project was developed as a learning project to strengthen my understanding of backend and frontend technologies, relational databases, the SQLAlchemy ORM, and full-stack web development.

> ⚠️ CampusHub is a learning project and is not production-ready. It has no CSRF protection, rate limiting, or HTTPS setup, so please do not deploy it as it is.

---


# 🚀 Features

### 🎓 Student Portal
- Student Login and Logout
- View Profile
- View Subjects for the Current Semester
- Attendance Summary per Subject (Total, Attended, Absent, Percentage)
- View Marks (Mid-Sem, Internal, End-Sem)
- View Assignments for Their Class
- Change Password

### 👨‍🏫 Faculty Portal
- Faculty Login and Logout
- View Profile
- Mark Attendance by Class, Subject, Date, and Time
- Create Assignments
- View Assignment History by Class and Semester
- Enter, Update, and View Student Marks
- Change Password

### 🛠 Admin Portal
- Admin Login and Logout
- View Profile
- Student Management
  - Add, View (with filters), Update, and Delete Students
- Faculty Management
  - Add, View (with filters), Update, and Delete Faculty
- Subject Management
  - Add and Delete Subjects
- Fees Management
  - View Fees with Filters
  - Add or Update a Student's Fee Amount and Paid/Unpaid Status

### 🔐 Security
- Password Hashing (Werkzeug)
- Separate Session for Each Role
- Students Can Only Access Their Own Data
- Delete Actions Require the Admin's Own Password
- Secrets Stored in a `.env` File

### 🎨 User Interface
- Landing Page with Portal Selection
- Styled Tables and Forms
- Clean Card-Based Layout

---

# 🛠 Tech Stack

## Backend
- Python
- Flask
- Flask-SQLAlchemy

## Database
- MySQL

## Frontend
- HTML5
- CSS3
- Jinja2 Templates

## Libraries Used
- Flask
- Flask-SQLAlchemy
- PyMySQL
- python-dotenv
- Werkzeug (password hashing, installed with Flask)

---

# 🗄 Database Design

Tables created automatically on the first run:

- `students`
- `faculty`
- `admins`
- `subjects`
- `attendance`
- `attendance_summary`
- `marks`
- `assignments`
- `fees`

Attendance, marks, and attendance summary rows are linked to `students` and `subjects` with foreign keys. Unique constraints protect IDs, emails, and subject codes.

---

# 📂 Project Structure

```
college-management-system/
│
├── app.py                  # Flask app and all routes
├── config.py               # Configuration loaded from .env
├── database.py             # SQLAlchemy instance
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/                 # SQLAlchemy models
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── index.html          # Landing page
    ├── student/            # Student portal pages
    ├── faculty/            # Faculty portal pages
    └── admin/              # Admin portal pages (including student and faculty management)
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/AlazharHararwala/college-management-system.git
```

Move into the project folder.

```bash
cd college-management-system
```

---

## 2. Create a Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project folder (next to `app.py`).

Example:

```env
SECRET_KEY=your_secret_key

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sms

FLASK_DEBUG=1
```

Generate a secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

`FLASK_DEBUG=1` is for local development only.

---

## 5. Create the Database

Open MySQL and execute:

```sql
CREATE DATABASE sms;
```

---

## 6. Run the Project

```bash
python app.py
```

The tables are created automatically on the first run.

Visit:

```
http://127.0.0.1:5000
```

---

## 7. Create the First Admin

There is no sign-up page. Admins create student and faculty accounts, so the first admin has to be inserted manually with a **hashed** password.

Generate the hash:

```bash
python -c "from werkzeug.security import generate_password_hash as g; print(g('choose_a_password'))"
```

Then run this in MySQL:

```sql
INSERT INTO admins (admin_id, full_name, email, password, gender, date_of_birth, phone)
VALUES ('ADMIN01', 'Demo Admin', 'admin@example.com', 'PASTE_THE_HASH_HERE', 'Other', '1990-01-01', '9999999999');
```

---

## 8. Add Some Data

1. Log in at `/admin/login`.
2. Add subjects.
3. Add a faculty member with a class assigned (for example `CSE-1A`).
4. Add students with the same class ID and a semester.
5. Log in as faculty at `/faculty/login` to mark attendance, create assignments, and enter marks.
6. Log in as a student at `/student/login` to view attendance, marks, and assignments.

---

# 🧪 Testing

The project was tested manually, role by role: all three logins, both change-password flows, adding a student and logging in as them, attendance entry, marks entry and viewing, assignments, fee updates, and both delete flows. There are no automated tests yet.

---

# 📝 Design Notes

- **No student fees page:** the university already gives students a physical receipt and an online copy, so only admins manage fee records in this system.
- **Attendance percentages** are calculated from the raw attendance records each time a page is opened.
- **Classes are stored as plain text** (for example `CSE-1A`), and a faculty member's classes are stored as a comma-separated list.

---

# 📚 What I Learned

While building this project, I learned:

- Flask Routing
- Flask Sessions
- Role-Based Access Control
- SQLAlchemy ORM
- MySQL Database Integration
- CRUD Operations
- Foreign Keys, Constraints, and Joins
- Password Hashing and Migrating Existing Data Safely
- Environment Variables
- Jinja2 Templating
- Form Handling and Optional Filters
- Debugging Flask Applications
- Manual Testing

---

# 🤖 AI Usage

This project was **not entirely AI-generated**.

AI was used as a development assistant to review code, help debug issues, suggest fixes, and generate the styling. I applied and tested every AI-assisted change before including it in the final project.

## Primarily Developed by Me

- Flask Backend (`app.py`)
- Application Routing and Role-Based Sessions
- Login and Authentication Logic
- SQLAlchemy Models and Database Design
- CRUD Operations for Students, Faculty, Subjects, Marks, and Fees
- Attendance, Marks, and Assignment Features
- Project Structure
- HTML Templates
- Manual Testing

## AI-Assisted Components

- CSS Styling (`style.css`) and CSS Class Names in the Templates
- Code Review and Debugging Assistance

The purpose of using AI was to assist the development process, not to replace learning. I made sure to test and verify all AI-assisted code before including it in the final project.

---

# 🚀 Future Improvements

- Numeric Marks Columns with Range Validation
- Subject Edit and List Pages
- Success and Error Messages After Actions
- Shared Base Template (`base.html`)
- Splitting Routes into Blueprints
- Database Migrations (Flask-Migrate)
- CSRF Protection
- A Separate Class Table with SQLAlchemy Relationships
- Update Attendance Feature
- Automated Tests

---

# 📄 License

This project is created for educational and portfolio purposes.

---

# 👨‍💻 Author

**Alazhar Hararwala**

GitHub:
https://github.com/AlazharHararwala

Linkedin:
https://www.linkedin.com/in/al-azhar-hararwala-091a02370
---

## ⭐ Support

If you found this project helpful or interesting, consider giving it a ⭐ on GitHub.

Feedback and suggestions are always welcome!