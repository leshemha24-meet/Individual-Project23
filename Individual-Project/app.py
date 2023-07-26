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

def get_checked_items(user_uid):
    user_data=db.child('Users').child(user_uid).get()
    return user_data.val() or {}

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
            user = {'email':email, 'fullname':name, 'username':username}
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
    name=''
    if 'user' in login_session:
        user=login_session['user']
        if user != None:
            try:
                uid=user['localId']
                name=db.child('Users').child(uid).get().val()['username'] 
            except:
                pass   
    if name=='':
        return redirect(url_for('index'))
    if request.method=='GET':
        return render_template('home.html', name=name) 
    else:
        feedback=request.form['feedback']
        db.child('Feedbacks').push(feedback)  
    return render_template('home.html', name=name)

@app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    return render_template('aboutus.html')

@app.route('/all', methods=['GET', 'POST'])
def all():
    checked_items = {}
    if 'user' in login_session:
        user_uid=login_session['user']['localId']
        checked_items=get_checked_items(user_uid)
    else:
        checked_items={}
    if request.method == 'POST':
        checkbox1=request.form.get('checkbox1')
        checkbox2=request.form.get('checkbox2')
        checkbox3=request.form.get('checkbox3')
        checkbox4=request.form.get('checkbox4')
        if user_uid:
            user_checklist = {'checkbox1':checkbox1, 'checkbox2':checkbox2, 'checkbox3':checkbox3, 'checkbox4':checkbox4}
        # done=request.form.get('checkbox')
        # print(done)
        db.child('Users').child(user_uid).child('myvids').set(user_checklist)
        return redirect(url_for('all'))
    else:
        return render_template("all.html", checked_items=checked_items)


@app.route('/signout')
def signout():
    login_session['User']=None
    auth.current_user= None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)