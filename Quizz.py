import pandas as pd
import random
from flask import Flask, render_template, request, jsonify

app = Flask (__name__, template_folder='templates')

@app.route('/')
def index():
    df = pd.read_excel('Quizz 1 1 (1).xlsx', engine='openpyxl')
    return render_template('index.html', questions=df)

@app.route('/quizz', methods=['POST'])
def quizz():
    df = pd.read_excel('Quizz 1 1 (1).xlsx', engine='openpyxl')
    options = ['A', 'B', 'C', 'D']
    score = 0
    responses = request.form

    for index, row in df.iterrows():
        question = row['Perguntas']
        questions_options = [row['Opção A'], row['Opção B'], row['Opção C'], row['Opção D']]
        correct_answer = row['Resposta Correta']
        user_answer = responses.get(f'answer_{index}', '').strip().upper()
    
        correct_index = questions_options.index(correct_answer)
    
        if user_answer == options[correct_index]:
            score += 1
    
    return jsonify({'score': score, 'total_questions': len(df)})
 
if __name__ == '__main__':
    app.run(debug=True)
