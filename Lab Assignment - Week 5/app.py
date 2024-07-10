from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

db = SQLAlchemy(app)

class student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey(student.student_id), nullable=True)  
    ecourse_id = db.Column(db.Integer, db.ForeignKey(course.course_id), nullable=True)  
    

d = {"course_1":"MAD I","course_2":"DBMS","course_3":"PDSA","course_4":"BDM"}

@app.route("/")
def executer():
    students = student.query.all()
    return render_template("index.html", students=students)

@app.route("/student/create", methods=["GET","POST"])
def creator():
    if request.method=="POST":
        roll = request.form["roll"]
        f_name = request.form["f_name"]
        l_name = request.form["l_name"]
        cour = [d[i] for i in request.form.getlist("courses")]
        
        studata = student.query.all()
        for i in studata:
            if i.roll_number==roll:
                return render_template("create_exist.html")

        stu = student(roll_number=roll,first_name=f_name,last_name=l_name)
        db.session.add(stu)

        sid = student.query.filter_by(roll_number=roll).first().student_id
        for i in cour:
            cid = course.query.filter_by(course_name=i).first().course_id
            en = enrollments(estudent_id=sid,ecourse_id=cid)
            db.session.add(en)    
            
        db.session.commit()
        return redirect("/")
        
    return render_template("create.html")

@app.route("/student/<int:student_id>/update", methods=["GET","POST"])
def updater(student_id):
    if request.method == "POST":
        f_name = request.form["f_name"]
        l_name = request.form["l_name"]
        cour = [d[i] for i in request.form.getlist("courses")]

        stu = student.query.filter_by(student_id=student_id).first()
        stu.first_name = f_name
        stu.last_name = l_name
        db.session.add(stu)

        en = enrollments.query.filter_by(estudent_id=student_id)
        for i in en:
            db.session.delete(i)
        for i in cour:
            cid = course.query.filter_by(course_name=i).first().course_id
            enr = enrollments(estudent_id=student_id,ecourse_id=cid)
            db.session.add(enr)  
        db.session.commit()
        return redirect("/")
    
    stu = student.query.filter_by(student_id=student_id).first()
    return render_template("update.html",student=stu)

@app.route("/student/<int:student_id>/delete", methods=["GET","POST"])
def destroyer(student_id):
    stu = student.query.filter_by(student_id=student_id).first()
    db.session.delete(stu)
    db.session.commit()
    return redirect("/")

@app.route("/student/<int:student_id>", methods=["GET"])
def viewer(student_id):
    stu = student.query.filter_by(student_id=student_id).first()
    en = enrollments.query.filter_by(estudent_id=student_id)
    enroll = []
    for i in en:
        cour = course.query.filter_by(course_id=i.ecourse_id).first()
        enroll.append({"code":cour.course_code,"name":cour.course_name,"desc":cour.course_description})
    return render_template("view.html",student=stu,enroll=enroll)

if __name__=="__main__":
    app.run()