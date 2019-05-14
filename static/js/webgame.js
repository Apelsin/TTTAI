let view = new BoardView(document.getElementById('main-game-board'));

async function stuff()
{
    let response = await fetch(`/session-data/${WEBGAME_VARS["session-id"]}`);
    let data = await response.json();
    let raw_board = data['board'];
    //let winner = Marks.getLabel(data['winner']);
    let flat = raw_board.flat();
    let board_state = flat.map(e => MarkSymbols[e.toString()]);
    view.setBoard(board_state);
}

stuff();