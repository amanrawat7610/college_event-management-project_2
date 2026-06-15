from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify



from flask_sqlalchemy import SQLAlchemy



from werkzeug.security import generate_password_hash, check_password_hash



import os



from functools import wraps



import time

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

import pandas as pd



from io import BytesIO


from werkzeug.utils import secure_filename




app = Flask(__name__)
UPLOAD_FOLDER = 'static/event_images'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


app.secret_key = "college_event_final_perfect_version"







# Database Configuration



basedir = os.path.abspath(os.path.dirname(__file__))







app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'instance', 'college_event.db'))







app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)



# app.py mein jahan db = SQLAlchemy(app) hai uske niche ye dalo:



with app.app_context():



    db.create_all()















MASTER_KEY = 'admin@786'







def login_required(f):



    @wraps(f)



    def decorated_function(*args, **kwargs):



        if not session.get('logged_in') or not session.get('user_id'):



            return redirect(url_for('login'))



        return f(*args, **kwargs)



    return decorated_function







# --- Database Models ---



class User(db.Model):



    id = db.Column(db.Integer, primary_key=True)



    email = db.Column(db.String(100), unique=True, nullable=False)



    password = db.Column(db.String(200), nullable=False)







class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    date = db.Column(db.String(20), nullable=False)

    image = db.Column(db.String(200), nullable=True)




class Student(db.Model):



    id = db.Column(db.Integer, primary_key=True)



    roll_no = db.Column(db.String(20), unique=True, nullable=False)



    name = db.Column(db.String(100), nullable=False)



    branch = db.Column(db.String(50), nullable=False)



    year = db.Column(db.String(20), nullable=False)



    phone = db.Column(db.String(15), nullable=False)



    event_name = db.Column(db.String(100), nullable=False)





class Feedback(db.Model):



    id = db.Column(db.Integer, primary_key=True)



    name = db.Column(db.String(100), nullable=False)



    roll_number = db.Column(db.String(20), nullable=False)



    rating = db.Column(db.Integer, nullable=False)



    comments = db.Column(db.Text, nullable=True)



    timestamp = db.Column(db.String(50), default=lambda: time.strftime('%Y-%m-%d %H:%M:%S'))







with app.app_context():



    if not os.path.exists(os.path.join(basedir, 'instance')):



        os.makedirs(os.path.join(basedir, 'instance'))



    db.create_all()







# --- Main Routes ---







@login_required



@app.route('/')



def dashboard():



    all_events = Event.query.all()



    total = Student.query.count()



    return render_template('dashboard.html', events=all_events, total_reg=total)







@app.route('/signup', methods=['GET', 'POST'])



def signup():



    if request.method == 'POST':



        if request.form.get('master_key').strip() != MASTER_KEY:



            flash("Invalid Master Key!", "danger")



            return redirect(url_for('signup'))



       



        hashed_pw = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')



        try:



            db.session.add(User(email=request.form.get('email').strip(), password=hashed_pw))



            db.session.commit()



            return redirect(url_for('login'))



        except:



            db.session.rollback()



            flash("Email already registered!", "danger")



    return render_template('signup.html')







@app.route('/login', methods=['GET', 'POST'])



def login():



    if request.method == 'POST':



        user = User.query.filter_by(email=request.form.get('email').strip()).first()



        if user and check_password_hash(user.password, request.form.get('password')):



            session['logged_in'] = True



            session['user_id'] = user.id



            return redirect(url_for('dashboard'))



        flash("Invalid Credentials", "danger")



    return render_template('login.html')







@app.route('/forgot_password', methods=['GET', 'POST'])



def forgot_password():



    if request.method == 'POST':



        m_key = request.form.get('master_key').strip()



        u_email = request.form.get('email').strip()



        new_p = request.form.get('new_password').strip()







        if m_key != MASTER_KEY:



            flash("Wrong Master Key!", "danger")



            return redirect(url_for('forgot_password'))







        user = User.query.filter_by(email=u_email).first()



        if user:



            user.password = generate_password_hash(new_p, method='pbkdf2:sha256')



            db.session.commit()



            flash("Password Reset Successful! Please Login.", "success")



            return redirect(url_for('login'))



        flash("Email not found!", "danger")



    return render_template('forgot_password.html')







@app.route('/register', methods=['GET', 'POST'])



def register():



    if request.method == 'POST':



        try:



            # Form data save karna



            new_s = Student(



                roll_no=request.form['roll_no'],



                name=request.form['name'],



                branch=request.form['branch'],



                year=request.form['year'], # Dropdown value yahan aayegi



                phone=request.form['phone'],



                event_name=request.form['event']



            )



            db.session.add(new_s)



            db.session.commit()



            # Return JSON response for ticket display



            return jsonify({



                'success': True,



                'student_name': new_s.name,



                'roll_number': new_s.roll_no,



                'event_name': new_s.event_name



            })



        except:



            db.session.rollback()



            return jsonify({



                'success': False,



                'message': 'Error: Roll Number already exists!'



            }), 400



    return render_template('register.html')







@login_required
@app.route('/add_event', methods=['POST'])
def add_event():

    image_file = request.files.get('event_image')

    image_name = None


    if image_file:

        image_name = secure_filename(image_file.filename)

        image_file.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                image_name
            )
        )


    event = Event(

        name=request.form['event_name'],

        date=request.form['event_date'],

        image=image_name

    )


    db.session.add(event)

    db.session.commit()


    return redirect(url_for('view_students'))







@login_required
@app.route('/delete_event/<int:id>')
def delete_event(id):

    event = Event.query.get(id)


    if event:

        if event.image:

            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                event.image
            )

            if os.path.exists(image_path):
                os.remove(image_path)


        db.session.delete(event)

        db.session.commit()


    return redirect(url_for('view_students'))







@login_required
@app.route('/students')
def view_students():

    if not session.get('logged_in'):
        return redirect(url_for('login'))

    students = Student.query.all()

    events = Event.query.all()

    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()

    return render_template(
        'view_students.html',
        students=students,
        events=events,
        feedbacks=feedbacks
    )







@login_required



@app.route('/download_excel')



def download_excel():



    students = Student.query.all()



    data = [{



        'Roll No': s.roll_no,



        'Name': s.name,



        'Branch': s.branch,



        'Year': s.year,



        'Phone': s.phone,



        'Event': s.event_name



    } for s in students]



    df = pd.DataFrame(data)



    output = BytesIO()



    df.to_excel(output, index=False, sheet_name='Students')



    output.seek(0)



    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='students.xlsx')







@login_required
@app.route('/download_pdf')
def download_pdf():

    students = Student.query.all()


    data = [

        [
            "Roll No",
            "Name",
            "Branch",
            "Year",
            "Phone",
            "Event"
        ]

    ]


    for s in students:

        data.append([

            s.roll_no,
            s.name,
            s.branch,
            s.year,
            s.phone,
            s.event_name

        ])



    output = BytesIO()


    pdf = SimpleDocTemplate(output)


    table = Table(data)


    table.setStyle(
        TableStyle([

            ('BACKGROUND',(0,0),(-1,0),colors.grey),

            ('TEXTCOLOR',(0,0),(-1,0),colors.white),

            ('GRID',(0,0),(-1,-1),1,colors.black),

            ('ALIGN',(0,0),(-1,-1),'CENTER')

        ])

    )


    pdf.build([table])


    output.seek(0)



    return send_file(

        output,

        mimetype='application/pdf',

        as_attachment=True,

        download_name='students.pdf'

    )






@app.route('/logout', methods=['POST'])
def logout():

    session.clear()

    response = redirect(url_for('login'))

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    flash("Logout successfully!", "success")

    return response







@login_required



@app.route('/delete_student/<i' \



'nt:id>')



def delete_student(id):



    student = Student.query.get(id)



    if student:



        db.session.delete(student)



        db.session.commit()



        flash("Student record deleted!", "success")



    return redirect(url_for('view_students'))




@login_required
@app.route('/delete_feedback/<int:id>')
def delete_feedback(id):

    feedback = Feedback.query.get(id)

    if feedback:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted successfully!", "success")

    return redirect(url_for('view_students'))










@app.route('/keep-alive')



def keep_alive():



    return "Server is awake!", 200





@app.route('/submit_feedback', methods=['POST'])



def submit_feedback():



    try:



        feedback = Feedback(



            name=request.form.get('name').strip(),



            roll_number=request.form.get('roll_number').strip(),



            rating=int(request.form.get('rating')),



            comments=request.form.get('comments').strip()



        )



        db.session.add(feedback)



        db.session.commit()



        return jsonify({



            'success': True,



            'message': 'Thank you for your feedback!'



        })



    except Exception as e:



        db.session.rollback()



        return jsonify({



            'success': False,



            'message': 'Error submitting feedback!'



        }), 400





@login_required



@app.route('/view_feedback')



def view_feedback():



    feedback_list = Feedback.query.order_by(Feedback.id.desc()).all()



    return render_template('view_feedback.html', feedbacks=feedback_list)





@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "-1"

    return response




if __name__ == '__main__':







    app.run(debug=True)
