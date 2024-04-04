from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('quiz'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    
    df = pd.read_excel('Quizz 1 1 (1).xlsx', engine='openpyxl')
    options = ['A', 'B', 'C', 'D']
    score = 0
    
    return render_template('quiz.html', questions=df)

@app.route('/quiz_submit', methods=['POST'])
def quiz_submit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    responses = request.form
    user_id = session['user_id']
    
    
    return redirect(url_for('quiz_result'))

@app.route('/quiz_result')
def quiz_result():

    return render_template('quiz_result.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

