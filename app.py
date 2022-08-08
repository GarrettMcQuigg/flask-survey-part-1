
from flask import Flask, render_template, request, flash, session, redirect
from surveys import satisfaction_survey as survey

RESPONSE_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"

@app.route('/')
def home_page():
    
    return render_template('survey_start.html', survey=survey)

@app.route('/begin', methods=['POST'])
def begin_survey():

    session[RESPONSE_KEY] = []

    return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def survey_questions(qid):

    responses = session.get(RESPONSE_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/finish")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template('questions.html', question=question, question_number=qid)

@app.route("/answer", methods=["POST"])
def save_question():
    
    choice = request.form['answer']

    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/finish")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/finish')
def finish():
    return render_template('finish.html')
