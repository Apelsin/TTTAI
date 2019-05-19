let view = new BoardView(document.getElementById('main-game-board'), Marks.OMARK);
let win_field = document.getElementById('win-field')

let last_good_board = null;

async function onValidGameStateResponse(response) {
    let data = await response.json();
    let board = data['board'].flat();
    let winner = data['winner'];
    view.setBoard(board);
    last_good_board = board;
    let board_full = board.every((c) => c !== 0);
    if(winner != null)
    {
        winner = Marks.getLabel(winner);
        view.setWinner(winner);
        win_field.innerHTML = `${winner} wins!`;
    }
    else if(board_full)
        win_field.innerHTML = 'Draw.';
    if(winner != null || board_full)
        for(e of document.getElementsByClassName('hide-until-win'))
            e.classList.remove('hidden');

}

function revertBoard() {
    view.setBoard(last_good_board)
}

async function handleMarked(e) {
    let form = new FormData();
    form.append('verb', 'set-mark');
    let args = {
        'row': e.detail.row,
        'column': e.detail.column,
        'mark': e.detail.mark
    };
    form.append('args', JSON.stringify(args))
    let response = await fetch(
        `/session-data/${WEBGAME_VARS["session-id"]}`,
        {
            method: 'POST',
            body: form
        });
    if(response.ok)
        await onValidGameStateResponse(response);
    else
        revertBoard();
}

async function setup()
{
    view.element.addEventListener('marked', handleMarked);
    let response = await fetch(`/session-data/${WEBGAME_VARS["session-id"]}`);
    if(response.ok)
        await onValidGameStateResponse(response);
    else
        revertBoard();
}

setup();