from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# an empty list that will hold user responses
RESPONSES_KEY = "responses"


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# home/starting page
@app.route("/")
def show_survey_on_start():
    # select which survey to start with
    return render_template("first_survey.html", survey=survey)


# Start survey
@app.route("/start", methods=["POST"])
def start_survey():
    
    session[RESPONSES_KEY] = []
    
    return redirect("/questions/0")

# User Responses
@app.route("/responses", methods=["POST"])
def handle_question():
    # save the user responses and redirect to the next question
    # get the response choice
    choice =  request.form['answer']
    
    # add response to the current session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    if (len(responses) == len(survey.questions)):
        # all questions have been completed
        return redirect("/surveycomplete")
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/questions/<int:questionid>")
def show_question(questionid):
    """Shows the current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # reached questions page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # User finished survey.
        return redirect("/endofsurvey")

    if (len(responses) != questionid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {questionid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[questionid]
    return render_template(
        "questions.html", question_num=questionid, question=question)

@app.route("/complete")
def completed_survey():
    """Finished survey!"""

    return render_template("endofsurvey.html")
    
    












