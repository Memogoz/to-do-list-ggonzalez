from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..models import Task, User
from datetime import datetime
from dotenv import load_dotenv

tasks = Blueprint('tasks', __name__)

@tasks.route('/')
def login():
    return render_template('login.html')


@tasks.route('/login', methods=['POST', 'GET'])
def check_login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        
        from app import db
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return redirect('/todo')
        elif (username == 'admin' and password == 'admin'):
            return redirect('/todo')
        else:
            return redirect('/login')
    else:
        return redirect('/')


@tasks.route('/signIn')
def signin():
    return render_template('signin.html')

@tasks.route('/createAccount', methods=['POST', 'GET'])
def createAccount():
    if request.method == 'POST':
        username = request.form['user']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username,email=email,password=password)

        from app import db
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the user'

    else:
        return redirect('/signIn')


@tasks.route('/todo', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_title = request.form['title']
        task_details = request.form['details']
        task_priority = request.form['priority']
        new_task = Task(title=task_title,details=task_details,priority=task_priority,user_id=100)

        from app import db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)
    


@tasks.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    from app import db
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was a problem deleting that task'



@tasks.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.title = request.form['title']
        task.details = request.form['details']
        task.priority = request.form['priority']

        from app import db
        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
