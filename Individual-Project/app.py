from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

Config = {
    "apiKey": "AIzaSyDvYNdFeczJ7iRUhlrUJAsl90GlT_OvL3Q",
    "authDomain": "individual-project-12d83.firebaseapp.com",
    "projectId": "individual-project-12d83",
    "storageBucket": "individual-project-12d83.appspot.com",
    "messagingSenderId": "1019117001507",
    "appId": "1:1019117001507:web:2bad1b7ea504c0f88dca96",
    "measurementId": "G-J89TSMRSE7",
    "databaseURL": "https://individual-project-12d83-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name= request.form['fullname']
        username= request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'email':email, 'fullname':fullname, 'username':username}
            db.child('Users').child(UID).set(user)
            return redirect(url_for('home'))
        except:
            return render_template('signup.html')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(debug=True)