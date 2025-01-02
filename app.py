from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.sqlite3'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


app.app_context().push()

class register(db.Model, UserMixin):
    id =  db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), unique=False, nullable = False)
    email = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(210), nullable = False)

    def __repr__(self):
        return f'{self.id} - {self.email}'
    
@login_manager.user_loader
def load_user(user_id):
    return register.query.get(int(user_id))

@app.route("/home", methods=['GET','POST'])
def home():
    
    username = session.get('username')
    sighn= register.query.all()
    print(sighn)
    return render_template('index.html', username=username)


@app.route('/user_register',methods=['GET','POST'])
def user_register():
   if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        existing_email = register.query.filter_by(email=email).first()
        if existing_email:
            flash(f"The email {email} is already registered. Please try another email.", 'danger')
            return redirect(url_for('user_register'))
        
        hash_psw = bcrypt.generate_password_hash(password).decode('utf-8')

        sign_in =register(username=username,email=email,password=hash_psw)
        db.session.add(sign_in)
        db.session.commit()
        flash(f"Welcome, {username}! You have successfully registered.", 'success')
        return redirect(url_for('login'))
      
    
   return render_template('user_register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # If already logged in, redirect to home page

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = register.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)  
            flash(f"Welcome, {user.username}! You are now logged in.", 'success')
            return redirect(url_for('profile'))  
        else:
            flash("Invalid email or password.", 'danger')
            return render_template('login.html')  

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", 'success')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html')
    return redirect(url_for('user_register'))


if __name__ == '__main__':
    app.run(debug=True)