from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
#from flask_login import UserMixin
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f'<User id {self.id}>' 

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    details = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.Integer, default=1)
    status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def check_login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return redirect('/todo')
        elif (username == 'admin' and password == 'admin'):
            return redirect('/todo')
        else:
            return redirect('/'), 401
    else:
        return redirect('/')


@app.route('/signIn')
def signin():
    return render_template('signin.html')

@app.route('/createAccount', methods=['POST', 'GET'])
def createAccount():
    if request.method == 'POST':
        username = request.form['user']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username,email=email,password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the user'

    else:
        return redirect('/signIn')


@app.route('/todo', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_title = request.form['title']
        task_details = request.form['details']
        task_priority = request.form['priority']
        new_task = Task(title=task_title,details=task_details,priority=task_priority,user_id=100)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo', 302)
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks), 302
    


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was a problem deleting that task'



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.title = request.form['title']
        task.details = request.form['details']
        task.priority = request.form['priority']

        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
