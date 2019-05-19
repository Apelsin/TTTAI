from flask import Flask, request, render_template, redirect, url_for, abort
from tictactoe import State, Mark
from tictactoe.cache import StateCache
from tictactoe.ai import calculate_next_state_for
import json
from random import randint

app = Flask(__name__)

EMPTY_BOARD = list(State()[:].flatten())  # No touchy


class SessionData:
    def __init__(self, starting_mark):
        self.state = State()
        self.mark = None


ACTIVE_SESSIONS = {}

STATE_CACHE = StateCache()

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


@app.route('/session-data/<session_id>', methods=['GET'])
def session_data(session_id):
    try:
        session = ACTIVE_SESSIONS[int(session_id)]
    except KeyError as e:
        return str(e), 404
    board = session.state[:].tolist()
    winner = session.state.winner
    state = {
        'board': board,
        'winner': winner
    }
    return json.dumps(state)


@app.route('/session-data/<session_id>', methods=['POST'])
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
                if wrong_mark or overwrite :
                    raise Exception('Illegal board move!')
            session.state.set_mark(row, col, player_mark)
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


def main():
    STATE_CACHE.load('state-cache.json')
    app.run(debug=True)


if __name__ == '__main__':
    main()
