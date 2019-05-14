const Marks = new Enum({ BLANK: 0, OMARK: 1, XMARK: 2 });
const MarkSymbols = {
    [Marks.BLANK]: ' ',
    [Marks.OMARK]: 'O',
    [Marks.XMARK]: 'X',
};

class BoardView
{
    constructor(element) {
        this.element = element;
    }

    setBoard(board) {
        for(let i = 0; i < board.length; i++) {
            let cell = this.element.children[i];
            //let cell_contents = cell.getElementsByClassName('cell-contents')[0];
            cell.innerHTML = board[i];
        }
    }
}