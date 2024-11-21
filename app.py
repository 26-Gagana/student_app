from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Updated Student model with additional fields
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    usn = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    father_phone_number = db.Column(db.String(15), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    mother_phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)


# Create all tables in the database
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        usn = request.form['usn']
        age = request.form['age']
        department = request.form['department']
        email = request.form['email']
        phone_number = request.form['phone_number']
        father_name = request.form['father_name']
        father_phone_number = request.form['father_phone_number']
        mother_name = request.form['mother_name']
        mother_phone_number = request.form['mother_phone_number']
        address = request.form['address']

        # Creating new student with additional fields
        new_student = Student(
            id=id,
            name=name,
            usn=usn,
            age=age,
            department=department,
            email=email,
            phone_number=phone_number,
            father_name=father_name,
            father_phone_number=father_phone_number,
            mother_name=mother_name,
            mother_phone_number=mother_phone_number,
            address=address
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.id = request.form['id']
        student.name = request.form['name']
        student.usn = request.form['usn']
        student.age = request.form['age']
        student.department = request.form['department']
        student.email = request.form['email']
        student.phone_number = request.form['phone_number']
        student.father_name = request.form['father_name']
        student.father_phone_number = request.form['father_phone_number']
        student.mother_name = request.form['mother_name']
        student.mother_phone_number = request.form['mother_phone_number']
        student.address = request.form['address']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})


if __name__ == "__main__":
    app.run(debug=True)
