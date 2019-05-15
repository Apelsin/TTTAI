from flask import Flask, request, render_template, redirect, url_for, abort
from tictactoe import State, Mark
from tictactoe.cache import StateCache
from tictactoe.ai import calculate_next_state_for
import json
from random import randint
import os

app = Flask(__name__)
app.config['SESSION_COOKIE_PATH'] = os.environ.get('FLASK_APPLICATION_ROOT', '/')

EMPTY_BOARD = list(State()[:].flatten())  # No touchy


class SessionData:
    def __init__(self, starting_mark):
        self.state = State()
        self.mark = starting_mark


ACTIVE_SESSIONS = {}

STATE_CACHE = StateCache()
STATE_CACHE.load('state-cache.json')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start-new-game')
def start_new_game():
    sid = randint(10000, 99999)
    ACTIVE_SESSIONS[sid] = ACTIVE_SESSIONS.get(sid, SessionData(Mark.OMARK))
    return redirect(url_for('session', session_id=sid))


@app.route('/session/<session_id>')
def session(session_id):
    try:
        session = ACTIVE_SESSIONS[int(session_id)]
    except KeyError as e:
        return repr(e), 404  # TODO
    return render_template(
        'game.html',
        board_marks=EMPTY_BOARD,
        session_id=session_id)


def advance_session(session):
    next_board_state = calculate_next_state_for(
        STATE_CACHE, session.state, session.mark)
    session.state = next_board_state
    session.mark = Mark.get_next(session.mark)


@app.route('/session-data/<session_id>')
def session_data(session_id):
    try:
        session = ACTIVE_SESSIONS[int(session_id)]
    except KeyError as e:
        return str(e), 404
    advance_session(session)
    board = session.state[:].tolist()
    winner = session.state.winner
    state = {
        'board': board,
        'winner': winner
    }
    return json.dumps(state)


def main():
    app.run()


if __name__ == '__main__':
    main()
