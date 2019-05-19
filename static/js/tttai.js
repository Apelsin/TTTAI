const Marks = new Enum({ BLANK: 0, OMARK: 1, XMARK: 2 });
const MarkSymbols = {
    [Marks.BLANK]: ' ',
    [Marks.OMARK]: 'O',
    [Marks.XMARK]: 'X',
};

class BoardView
{
    constructor(element, mark) {
        this.element = element;
        this.mark = mark;
        this.winner = null;
        this.numberOfColumns = 3;
        for(let i = 0; i < element.children.length; i++) {
            let cell = this.element.children[i];
            cell.addEventListener('click', (e) => this.handleCellClicked(i, e));
        }
    }

    handleCellClicked(cell_index, e) {
        if(this.winner != null)
            return;
        this.setMark(cell_index, this.mark);
        event = new CustomEvent('marked', {
            detail : {
                cellIndex: cell_index,
                row: Math.floor(cell_index / this.numberOfColumns),
                column: cell_index % this.numberOfColumns,
                mark: this.mark
            }
        });
        this.element.dispatchEvent(event);
    }

    setBoard(board) {
        for(let i = 0; i < board.length; i++) {
            let cell = this.element.children[i];
            cell.innerHTML = MarkSymbols[board[i]];
        }
    }

    setWinner(winner) {
        this.winner = winner;
    }

    setMark(index, mark) {
        let cell = this.element.children[index];
        cell.innerHTML = MarkSymbols[mark];
    }
}