
from re import S
from flask import render_template, flash, url_for, request, redirect, make_response
from flask_login import login_required, login_user, current_user, logout_user, login_required
from app_config import app, db

from form import RegistrationForm
from models import Users, Patients, Tests
from passlib.hash import bcrypt

import pickle
import pandas as pd

diabetes_model, scaler = pickle.load(open("diabetes.pkl", "rb"))


#-------------------------------------------------------------------------------------------------------------------------------LOG IN---------


@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST','GET'])
def login():
   if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
   if request.method == 'POST':
        # Get Form Fields
      email = request.form['email']
      password_candidate = request.form['password']

      user=Users.query.filter_by(email=email).first()
      if user:

          passwordd=Users.query.filter_by(email=email).first()
          if bcrypt.verify(password_candidate, passwordd.password):
              login_user(user)
              return redirect(url_for('dashboard'))
          else:
              error = "Invalid Password"
              return render_template('Login.html', error=error)

      else:
          error = "Invalid email"
          return render_template('Login.html', error=error)    
   return render_template('Login.html') 


#-------------------------------------------------------------------------------------------------------------------------------LOG OUT---------


@app.route('/logout')
@login_required
def logout():
   logout_user()
   resp = make_response(redirect(url_for('login')))
   return resp
   #return render_template("Login.html")


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
@login_required
def dashboard():

    return render_template('Dashboard.html')


#----------------------------------------------------------------------------------------------------------------------------PATIENTS---------


@app.route('/patients', methods=['POST','GET'])
@login_required
def patients():
    patients = Patients.query.filter(Patients.id_user == current_user.get_id()).all()
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        sex = request.form.get('sex')
        date_of_birth = request.form.get('dateofbirth')
        address = request.form.get('homeaddress')
        email = request.form.get('email')
        phone_number = request.form.get('phonenumber')
        add = Patients(first_name = first_name, last_name = last_name, sex = sex, date_of_birth = date_of_birth, address = address, email = email, phone_number = phone_number, id_user = current_user.get_id())
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('patients'))

    return render_template('Patients.html', patients = patients)

@app.route("/updatepatient/<int:patient_id>", methods=['POST','GET'])
@login_required
def update_product(patient_id):
    patient = Patients.query.get(patient_id)
    if request.method == 'POST':
        patient.first_name = request.form.get('firstname')
        patient.last_name = request.form.get('lastname')
        patient.sex = request.form.get('sex')
        patient.date_of_birth = request.form.get('dateofbirth')
        patient.address = request.form.get('homeaddress')
        patient.email = request.form.get('email')
        patient.phone_number = request.form.get('phonenumber')
        db.session.commit()
        return redirect(url_for('patients'))

    return render_template('update_patient.html', patient = patient)

@app.route("/patient/delete/<int:patient_id>", methods=['POST'])
@login_required
def delete_patient(patient_id):
    patient = Patients.query.get(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('patients'))


#----------------------------------------------------------------------------------------------------------------------------TESTS---------

@app.route('/tests/<int:patient_id>', methods=['POST', 'GET'])
@login_required
def tests(patient_id):

    tests = Tests.query.filter(Tests.patient_id == patient_id).all()
    if request.method == 'POST':
        pregnancies = request.form.get('pregnancies')
        glucose = request.form.get('glucose')
        blood_pressure = request.form.get('bloodpresure')
        skin_thickness = request.form.get('skinthickness')
        insulin = request.form.get('insulin')
        bmi = request.form.get('bmi')
        diabetes_pedigree_function = request.form.get('diabetespredigreefunction')
        age = request.form.get('age')
        # row = pd.DataFrame([pd.Series([pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age])])
        data = {'Pregnancies': [pregnancies], 'Glucose': [glucose], "BloodPressure": [blood_pressure], 
            'SkinThickness': [skin_thickness], 'Insulin': [insulin], 'BMI': [bmi],
            'DiabetesPedigreeFunction': [diabetes_pedigree_function], 'Age': [age]}
        row = pd.DataFrame.from_dict(data)
        row = scaler.transform(row)
        print(row)
        prediction = diabetes_model.predict_proba(row)
        outcome='{0:.{1}f}'.format(prediction[0][1], 2)
        outcome = str(float(outcome)*100)+'%'
        add = Tests(pregnancies = pregnancies, glucose = glucose, blood_pressure = blood_pressure,
                     skin_thickness = skin_thickness, insulin = insulin, bmi = bmi, 
                     diabetes_pedigree_function = diabetes_pedigree_function,age = age,  patient_id = patient_id, outcome = outcome)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('tests', patient_id = patient_id))

    return render_template('Tests.html', tests = tests)
  
@app.route("/tests/<int:patient_id>/delete/<int:test_id>", methods=['POST'])
@login_required
def delete_test(test_id, patient_id):
    test = Tests.query.get(test_id)
    db.session.delete(test)
    db.session.commit()
    return redirect(url_for('tests', patient_id = patient_id))


#--------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":  # Makes sure this is the main process
	  app.run( # Starts the site
		host='127.0.0.1',  # Establishes the host, required for repl to detect the site
		port=5000  # Randomly select the port the machine hosts on.
	)
