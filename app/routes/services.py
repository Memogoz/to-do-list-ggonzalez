from functools import wraps
from flask import redirect, session, flash
import requests


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('You need to log in first.', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function



def getTimezones():
    locations = ['ip','timezone/Europe/Berlin','timezone/America/Argentina/Salta','timezone/Asia/Bangkok']
    timezones =[]

    for location in locations:
        url = "http://worldtimeapi.org/api/" + location
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()  
                time = data['datetime'][11:19]
                timezones.append(time)
            else:
                print(f"Error en la solicitud. Código de estado: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Error al realizar la solicitud:", e)

    return timezones