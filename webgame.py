from flask import Flask, Blueprint, render_template, redirect, url_for
from tictactoe import State, Mark
from tictactoe.cache import StateCache
from tictactoe.ai import calculate_next_state_for
import json
from random import randint
import os

FLASK_APPLICATION_ROOT = os.environ.get('FLASK_APPLICATION_ROOT', '')
EMPTY_BOARD = list(State()[:].flatten())  # No touchy
ACTIVE_SESSIONS = {}
STATE_CACHE = StateCache()
STATE_CACHE.load('state-cache.json')


class SessionData:
    def __init__(self, starting_mark):
        self.state = State()
        self.mark = starting_mark


# Used in order to prepend the FLASK_APPLICATION_ROOT prefix
bp = Blueprint('main',
               __name__,
               template_folder='templates',
               static_folder='static')


@bp.context_processor
def globals_processor():
    def flask_application_root():
        return FLASK_APPLICATION_ROOT
    return {'FLASK_APPLICATION_ROOT': flask_application_root}


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/start-new-game')
def start_new_game():
    sid = randint(10000, 99999)
    ACTIVE_SESSIONS[sid] = ACTIVE_SESSIONS.get(sid, SessionData(Mark.OMARK))
    return redirect(url_for('main.session', session_id=sid))


@bp.route('/session/<session_id>')
def session(session_id):
    if int(session_id) not in ACTIVE_SESSIONS:
        return f'not found.', 404  # TODO
    return render_template(
        'game.html',
        board_marks=EMPTY_BOARD,
        session_id=session_id)


def advance_session(session):
    next_board_state = calculate_next_state_for(
        STATE_CACHE, session.state, session.mark)
    session.state = next_board_state
    session.mark = Mark.get_next(session.mark)


@bp.route('/session-data/<session_id>')
def session_data(session_id):
    if int(session_id) not in ACTIVE_SESSIONS:
        return '', 404  # TODO
    advance_session(session)
    board = session.state[:].tolist()
    winner = session.state.winner
    state = {
        'board': board,
        'winner': winner
    }
    return json.dumps(state)


app = Flask(__name__)
app.register_blueprint(bp, url_prefix=FLASK_APPLICATION_ROOT)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
