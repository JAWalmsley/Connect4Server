const MAX_Y = 5;
const MAX_X = 6;

/**
 * Creates an empty board
 * @returns {[]} An empty board of size MAX_X x MAX_Y
 */
function emptyGameState() {
    let emptyBoard = [];
    for (let y = 0; y <= MAX_Y; y++) {
        emptyBoard.push([]);
        for (let x = 0; x <= MAX_X; x++) {
            emptyBoard[y].push("");
        }
    }
    return emptyBoard;
}

/**
 * Converts a sequence of x placements into a game board
 * @param notation Sequence of x placements, in chronological order
 * @returns {*[]} A game board representing the notation
 */
function notationToState(notation) {
    let board = emptyGameState();
    let redCurrPlayer = true;
    let players = {true: "r", false: "y"};
    for (let i = 0; i < notation.length; i++) {
        let x = parseInt(notation.charAt(i));
        let y = MAX_Y;
        while (y >= 0) {
            if (board[y][x] === "") {
                board[y][x] = players[redCurrPlayer];
                redCurrPlayer = !redCurrPlayer;
                break;
            } else {
                y--;
            }
        }
    }
    return board
}

/**
 * Turns a screen position in pixels to a position on the game board
 * @param posX Pixel X position
 * @param posY Pixel Y Position
 * @returns {{}} Y, X game board position
 */
function screenPosToGridPos(posX, posY) {
    let c = document.getElementById("canvas");
    let width = c.width / (MAX_X + 1);
    let height = c.height / (MAX_Y + 1);
    return{y: parseInt(posY / height), x: parseInt(posX / width)}
}