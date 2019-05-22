from flask import Flask, Blueprint, render_template, redirect, request, url_for
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
    def __init__(self):
        self.state = State()
        self.mark = None


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
    ACTIVE_SESSIONS[sid] = ACTIVE_SESSIONS.get(sid, SessionData())
    return redirect(url_for('main.session', session_id=sid))


@bp.route('/session/<session_id>')
def session(session_id):
    if int(session_id) not in ACTIVE_SESSIONS:
        return 'Not found.', 404  # TODO
    return render_template(
        'game.html',
        board_marks=EMPTY_BOARD,
        session_id=session_id)


@bp.route('/session-data/<session_id>', methods=['GET'])
def session_data(session_id):
    try:
        session = ACTIVE_SESSIONS[int(session_id)]
    except KeyError as e:
        return 'Not found.', 404  # TODO
    board = session.state[:].tolist()
    winner = session.state.winner
    state = {
        'board': board,
        'winner': winner
    }
    return json.dumps(state)


@bp.route('/session-data/<session_id>', methods=['POST'])
def session_data_submit(session_id):
    try:
        session = ACTIVE_SESSIONS[int(session_id)]
    except KeyError as e:
        return str(e), 404
    try:
        verb = request.form.get('verb')
        if verb.lower() == 'set-mark':
            args = json.loads(request.form.get('args'))
            player_mark = Mark(args['mark'])
            row = args['row']
            col = args['column']

            next_mark = Mark.get_next(player_mark)
            if session.mark is None:
                session.mark = next_mark
            else:
                wrong_mark = session.mark != next_mark
                overwrite = session.state.get_mark(row, col) != Mark.EMPTY
                if wrong_mark or overwrite:
                    raise Exception('Illegal board move!')
            session.state.set_mark(row, col, player_mark)
            if session.state.winner is None:
                try:
                    next_board_state = calculate_next_state_for(
                        STATE_CACHE, session.state, session.mark)
                    session.state = next_board_state
                except ValueError:
                    pass

    except Exception as e:
        raise e
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
