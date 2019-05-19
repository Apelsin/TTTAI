let view = new BoardView(document.getElementById('main-game-board'), Marks.OMARK);
let last_good_board = null;

async function onValidGameStateResponse(response) {
    let data = await response.json();
    let board = data['board'].flat();
    //let winner = Marks.getLabel(data['winner']);
    view.setBoard(board);
    last_good_board = board;
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