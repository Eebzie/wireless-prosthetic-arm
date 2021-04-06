from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, make_response
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mysqldb import MySQL
import MySQLdb
from flask_mqtt import Mqtt
from datetime import datetime
import json
from time import time
from random import random
import yaml


app = Flask(__name__)

#set up secret key
app.secret_key = '>Cqz>o/{oWwU,B0!I>]q'

#set up login manager
login_manager = LoginManager()
login_manager.init_app(app)

##set up database
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB']  = db['mysql_db']
mysql = MySQL(app)

#set up mqtt
app.config['MQTT_BROKER_URL'] = 'driver.cloudmqtt.com'
app.config['MQTT_BROKER_PORT'] = 18828
app.config['MQTT_USERNAME'] = 'aukszoac'
app.config['MQTT_PASSWORD'] = 'tkKyhEKbPwRh'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

class  User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    if user_id != "":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email= %s", [user_id])
        serial_status = cur.fetchone()
        cur.close()
        if serial_status:
            user = User()
            user.id = user_id
            return user
        else: 
            return
    else:
        return

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email= %s", [email])
    serial_status = cur.fetchone()
    cur.close()
    if serial_status:
        user = User()
        user.id = email
        user.is_authenticated = True
        return user

    else:
        return

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('arduino')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    ValToSend = message.payload.decode()
    ValToSend = ValToSend.split(";")
    with app.app_context():

        now = datetime.now() #current date and time
        date_time = now.strftime("%H%M%S")

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO datatable VALUES (%s, %s, %s, %s)', (ValToSend[3], ValToSend[2], ValToSend[4], date_time))
        cur.execute('UPDATE livedata SET EMG = %s, Temp1 = %s, Temp2 = %s WHERE serialnumber = %s', (ValToSend[2], ValToSend[0], ValToSend[1], ValToSend[3]))
        mysql.connection.commit()
        cur.close

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

##########################################################################################
@app.route('/')
def index():
    if current_user.is_anonymous == True:
        return render_template("index.html")
    else:
        return redirect(url_for('protected'))

##########################################################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if current_user.is_anonymous == True:
            return render_template("login.html")
        else:
            return redirect(url_for('protected'))
    else:
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email= %s AND password= %s", (email, password))
        account = cur.fetchone()
        cur.close()
        if account:
            user = User()
            user.id = email
            login_user(user)
            return redirect(url_for('protected'))
        else:
            flash('Incorrect Email and Password Combination')
            return redirect(url_for('login'))

##########################################################################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        if current_user.is_anonymous == False:
            return redirect(url_for('protected'))
        else:
            session['Serial_Confirmed'] = 0
            return render_template("register.html")
    else: #if post request
        #if no serial number has been confirmed
        if session['Serial_Confirmed'] == 0: 
            Serial_Number = request.form['serial-number']

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM serialnumber WHERE serialnumber= %s", [Serial_Number])
            serial_status = cur.fetchone()
            #if the serial number is found
            if serial_status:
                cur.execute("SELECT taken FROM serialnumber WHERE serialnumber= %s", [Serial_Number])
                serial_status = cur.fetchone()
                #if the serial number is not being used
                if 0 in serial_status:
                    session['Serial_Confirmed'] = 1 
                    session['Serial_Number'] = Serial_Number
                    return render_template('profile-creation.html', Serial_Number=Serial_Number)
                #if the serial number is being used
                else:
                    cur.close
                    flash('Serial Number Already in Use')
                    return redirect(url_for('register'))
            #if the serial number is not found
            else:
                cur.close
                flash('Serial Number Not Valid')
                return redirect(url_for('register'))

        #if the serial number has been confirmed
        elif session['Serial_Confirmed'] == 1: 
            session['Serial_Confirmed'] == 0
            fullname = request.form['fullname']
            city = request.form['city']
            birthday = request.form['birthday']
            email = request.form['email']
            password = request.form['password']
            Serial_Number = session['Serial_Number']

            cur = mysql.connection.cursor()
            #Add to users table
            cur.execute('INSERT INTO users VALUES (%s, % s, % s, % s, % s, % s)', (fullname, city, birthday, Serial_Number, email, password))
            #Update serialnumber table
            mysql.connection.commit()
            cur.execute('UPDATE serialnumber SET taken = 1, email = %s WHERE serialnumber = %s', [email, Serial_Number])
            mysql.connection.commit()
            #Update livedata table
            cur.execute('UPDATE livedata SET email = %s WHERE serialnumber = %s', [email, Serial_Number])
            mysql.connection.commit()
            
            cur.close()

            session.pop('Serial_Confirmed', None)
            session.pop('Serial_Number', None)
            user = User()
            user.id = email
            login_user(user)
            return redirect(url_for('protected'))

##########################################################################################
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/about_guest')
def about_guest():
    return render_template("homeAbout.html")

##########################################################################################
@app.route('/protected')
@login_required
def protected():

    cur = mysql.connection.cursor()

    cur.execute('SELECT serialnumber FROM serialnumber WHERE email = %s', [current_user.id])
    results = cur.fetchone()
    for result in results:
        email = result

    #GET HISTORICAL EMG DATA
    cur.execute("SELECT EMG FROM datatable WHERE SerialNumber = %s", [email])
    results = cur.fetchall()
    EMG_Values =[x[0] for x in results]

    #GET HISTORICAL TIME DATA
    cur.execute("SELECT DateTime FROM datatable WHERE SerialNumber = %s", [email])
    results = cur.fetchall()
    Time_Values =[x[0] for x in results]

    #GET NAME
    cur.execute("SELECT fullname FROM users WHERE email= %s", [current_user.id])
    results = cur.fetchone()
    json_array = ["1"]
    for i in results:
        json_array[0] = i.split(' ')[0]
    cur.close
    
    return render_template("dashboard.html", Time_Object = json.dumps(Time_Values), name = json_array[0], EMG_Object = json.dumps(EMG_Values))

##########################################################################################
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfuly logged out')
    return redirect(url_for('login'))

##########################################################################################
@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Unauthorized Input')
    return redirect(url_for('index'))

##########################################################################################
@app.route('/livegrab', methods=['GET', 'POST'])
@login_required
def testgrab():
    cur = mysql.connection.cursor()
    cur.execute("SELECT EMG, Temp1, Temp2 FROM livedata WHERE email= %s", [current_user.id])
    results = cur.fetchone()
    json_array = ["1", "2", "3"]
    foo = 0
    for i in results:
        json_array[foo] = i
        foo = foo + 1
    cur.close
    response = make_response(json.dumps(json_array))
    response.content_type = 'application/json'

    return response

#set up autoclear
def clear_userdata():
    now = datetime.now() #current date and time
    date_time = int(now.strftime("%H"))
    print('test')
    if date_time >= 0 and date_time < 1:
        db = MySQLdb.connect(db['mysql_host'], db['mysql_user'], db['mysql_password'], db['mysql_db'])
        cur = db.cursor()
        cur.execute('TRUNCATE TABLE datatable')
        db.commit()
        cur.close

sched = BackgroundScheduler()
sched.add_job(func=clear_userdata,trigger="interval", minutes=60)
sched.start()

if __name__ == "__main__":
    app.run(debug=True)
