# run with commend : flask --app MainScores.py run
import werkzeug
from flask import Flask, render_template , request, redirect ,url_for
from Score import read_score

app = Flask(__name__, template_folder='template')


@app.route('/')
def content():
    return render_template('index.html', score=read_score())


@app.route('/gamepicker', methods=["GET","POST"])
def gamepicker():
    return render_template('gamepicker.html')


@app.route('/memorygame')
def memorygame():
    return render_template('memorygame.html')


@app.route('/guessgame')
def guessgame():
    return render_template('guessgame.html')


@app.route('/currency')
def currency():
    return render_template('currency.html')


@app.route('/savegame')
def savegame():
    return render_template('savegame.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    game_chosen = int(request.form['game_chosen'])
    if game_chosen == 1:
        return redirect(url_for('memorygame'))
    elif game_chosen == 2:
        return redirect(url_for('guessgame'))
    elif game_chosen == 3:
        return redirect(url_for('currency'))


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return render_template('err500.html')


app.register_error_handler(500, handle_bad_request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
