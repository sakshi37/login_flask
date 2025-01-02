from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()


class register(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), unique=False, nullable = False)
    email = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(210), nullable = False)

    def __repr__(self):
        return f'{self.id} - {self.email}'

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
        
        flash(f"Welcome, {username}! You have successfully registered.", 'success')
       
        sign_in =register(username=username,email=email,password=password)
        db.session.add(sign_in)
        db.session.commit()
        return redirect(url_for('login'))

   return render_template('user_register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user=register.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                session['username'] = user.username
                flash(f"Welcome, {user.username}! You are now logged in.", 'success')
                return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)