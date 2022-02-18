from re import S
from flask import render_template
from flask_login import login_required
from app_config import app






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
    
    return render_template('SignUp.html')

#------------------------------------------------------------------------------------------------------------------------------DASHBOARD---------


@app.route('/dashboard')
def dashboard():

    return render_template('Dashboard.html')


#----------------------------------------------------------------------------------------------------------------------------PATIENTS---------


@app.route('/patients', methods=['POST','GET'])
def patients():

  return render_template('Patients.html')
    
#--------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":  # Makes sure this is the main process
	  app.run( # Starts the site
		host='127.0.0.1',  # Establishes the host, required for repl to detect the site
		port=5000  # Randomly select the port the machine hosts on.
	)
