from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for('success', email=user.email))
        else:
            error_message = 'Incorrect email or password'
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error_message = 'Email address is already registered.'
            return redirect(url_for('message', message=error_message))
        
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        success_message = 'Successfully registered! You can now log in.'
        return redirect(url_for('message', message=success_message))
    else:
        return render_template('register.html')

    
@app.route('/success/<email>')
def success(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return render_template('success.html', user=user)
    else:
        return 'User not found'

@app.route('/message/<message>')
def message(message):
    return render_template('message.html', message=message)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
