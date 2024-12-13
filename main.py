from flask import Flask, render_template, request, session, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_quiz(genres, levels):
    file_path = f"quizinfo/{levels}_{genres}_questions.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            if isinstance(data, list) and data:
                return data
            else:
                print("Invalid or empty quiz data.")
                return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


@app.route('/quiz/<genres>/<levels>', methods=['GET', 'POST'])
def quiz(genres, levels):
    genres = genres.lower()
    levels = levels.lower()


    quiz_data = load_quiz(genres, levels)
    if not quiz_data or not isinstance(quiz_data, list):
        return render_template('404.html'), 404


    if 'current_question' not in session:
        session['current_question'] = 0
        session['score'] = 0


    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        correct_answer = quiz_data[session['current_question']]['correct']


        if selected_answer == correct_answer:
            session['score'] += 1


        session['current_question'] += 1


        if session['current_question'] >= len(quiz_data):
            session['total_questions'] = len(quiz_data)
            return redirect(url_for('quizresults'))


    if session['current_question'] >= len(quiz_data):
        return redirect(url_for('quizresults'))


    current_question_index = session['current_question']
    current_question = quiz_data[current_question_index]
    return render_template(
        'quiz.html',
        question=current_question,
        question_number=current_question_index + 1,
        total_questions=len(quiz_data),
        genres=genres.capitalize(),
        levels=levels.capitalize()
    )



@app.route('/quizresults')
def quizresults():

    score = session.get('score', 0)
    total = session.get('total_questions', 0)


    session.pop('current_question', None)
    session.pop('score', None)
    session.pop('total_questions', None)

    return render_template('quizresults.html', score=score, total=total)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/genres/<genres>')
def genres_page(genres):
    genres = genres.lower()
    return render_template('genres.html', genres=genres.capitalize())

@app.route('/levels/<genres>')
def levels_page(genres):
    genres = genres.lower()
    return render_template('levels.html', genres=genres.capitalize())

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
