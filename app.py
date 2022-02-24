from re import S
from flask import render_template, flash, url_for, request, redirect
from flask_login import login_required
from app_config import app, db

from form import RegistrationForm
from models import Users
from passlib.hash import bcrypt




#-------------------------------------------------------------------------------------------------------------------------------LOG IN---------


@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST','GET'])
def login():

    return render_template('Login.html')


#-------------------------------------------------------------------------------------------------------------------------------LOG OUT---------


@app.route('/logout')
def logout():
    return render_template("Login.html")


#-------------------------------------------------------------------------------------------------------------------------------SIGN UP---------


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
  form = RegistrationForm(request.form)
  if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = bcrypt.hash(str(form.password.data))
        user = Users(first_name=first_name, last_name=last_name, email=email, password= password)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered', 'success')
        return redirect(url_for('login'))
    
  return render_template('SignUp.html', form = form)

#------------------------------------------------------------------------------------------------------------------------------DASHBOARD---------


@app.route('/dashboard')
def dashboard():

    return render_template('Dashboard.html')


#----------------------------------------------------------------------------------------------------------------------------PATIENTS---------


@app.route('/patients', methods=['POST','GET'])
def patients():

  return render_template('Patients.html')


#----------------------------------------------------------------------------------------------------------------------------TESTS---------


@app.route('/tests', methods=['POST','GET'])
def tests():

  return render_template('Tests.html')
  

#--------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":  # Makes sure this is the main process
	  app.run( # Starts the site
		host='127.0.0.1',  # Establishes the host, required for repl to detect the site
		port=5000  # Randomly select the port the machine hosts on.
	)
