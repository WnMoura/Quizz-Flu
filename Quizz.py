
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

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
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Este usuário já foi cadastrado, por favor insira outro.', 'error')
            return redirect(url_for('register'))
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
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
    session['responses'] = responses  
    print("Respostas submetidas pelo usuário:", responses)  
    
    return redirect(url_for('quiz_result'))


@app.route('/quiz_result')
def quiz_result():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('login'))
    
    df = pd.read_excel('Quizz 1 1 (1).xlsx', engine='openpyxl')
    print("Total de perguntas no arquivo Excel:", len(df))  
    responses = session.get('responses', {})
    print("Respostas armazenadas na sessão:", responses)  
    score = calculate_score(df, responses)  
    
    score, total_questions = calculate_total_score(df, responses)
    
    total_questions = len(df)
    message = ""
    
    if score < total_questions:
        message += ""
    
    if score >= total_questions * 0.7:
        image_url = "/static/Faz_o_L.jpg"
    else:
        image_url = "/static/acaba_carioca.jpg"
    
    return render_template('quiz_result.html', score=score, total_questions=total_questions, message=message, image=image_url)



def calculate_score(df, responses):
    score = 0
    for index, row in df.iterrows():
        question_number = row['Perguntas']
        correct_answer = row['Resposta Correta']
        user_answer = responses.get('answer_' + str(index))
        print("Pergunta:", question_number)
        print("Resposta correta:", correct_answer)
        print("Resposta do usuário:", user_answer)
        if user_answer and user_answer == correct_answer:
            score += 1
    return score

def calculate_total_score(df, responses):
    total_questions = len(df)
    score = calculate_score(df, responses)
    return score, total_questions


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)