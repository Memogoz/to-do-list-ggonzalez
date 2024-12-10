from flask import Flask, render_template, url_for, request, redirect, flash, Blueprint, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..models.models import Task, User
from .services import login_required
from datetime import datetime, timedelta
from dotenv import load_dotenv

tasks = Blueprint('tasks', __name__)

@tasks.route('/')
def login():
    if session.get('logged_in'):  
        return redirect('/todo')  
    return render_template('login.html')  



@tasks.route('/login', methods=['POST', 'GET'])
def check_login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        
        from app import db
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id  # Guardar ID del usuario en la sesión
            session['username'] = user.username  # Guardar el nombre de usuario
            session['logged_in'] = True
            flash('Welcome back, {}'.format(user.username), 'success')
            return redirect('/todo')
        elif username == 'admin' and password == 'admin':
            session['username'] = 'admin'
            session['logged_in'] = True
            flash('Welcome Admin', 'success')
            return 'Admin page in development...'
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect('/login')
    else:
        return redirect('/')


@tasks.route('/logout')
def logout():
    session.clear()  # Limpiar todos los datos de la sesión
    flash('You have been logged out.', 'info')
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
@login_required
def index():
    if not session.get('logged_in'):  # Verificar si el usuario está logueado
        flash('Please log in to access your tasks.', 'warning')
        return redirect('/')
    
    if request.method == 'POST':
        task_title = request.form['title']
        task_details = request.form['details']
        task_priority = request.form['priority']
        new_task = Task(title=task_title, details=task_details, priority=task_priority, user_id=session['user_id'])

        from app import db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Task.query.filter_by(user_id=session['user_id']).order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)

    


@tasks.route('/delete/<int:id>')
@login_required
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
@login_required
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
