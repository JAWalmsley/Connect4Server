class gameState {
    constructor() {
        this.board = emptyGameState();
        this.myTurn = true;
        this.color = 'r';
        this.socket = io();

        this.socket.emit('newgame', {board: this.board});

        let self = this; // 'this' does not work in callback functions
        this.socket.on('gamecreated', function (message) {
            self.gameid = message['gameid'];
            document.getElementById('gameid').innerHTML = message['gameid'];
        });

        this.socket.on('opponentmove', function (message) {
            self.board = message['board'];
            drawBoard(self.board);
            self.findWin();
            self.myTurn = true;
        });
    }

    /**
     * Resets the game board and current turn
     */
    resetGame() {
        this.board = emptyGameState();
    }

    joingame(id) {
        this.socket.emit('joingame', {id: id, oldid: this.gameid});
        this.gameid = id;
        this.myTurn = false;
        this.color = 'y';
        document.getElementById('gameid').innerHTML = this.gameid;
    }

    /**
     * Runs function on all items in board
     * @param action Function to call
     */
    for_every_in_board(action) {
        for (let y = 0; y <= MAX_Y; y++) {
            for (let x = 0; x <= MAX_X; x++) {
                let result = action(this.board[y][x], x, y);
                if (result) {
                    return result
                }
            }
        }
    }

    /**
     * Places stone at the next available height
     * @param x The x position to place the stone
     */
    place_stone(x) {
        let y = this.can_place(x);
        if (y !== -1) {
            this.board[y][x] = this.color;
            this.socket.emit('update', {id: this.gameid, board: this.board});
            this.myTurn = false;
            drawBoard(this.board);
            this.findWin();
        }
    }


    /**
     * Returns the next available y position
     * @param x The x position to search
     * @returns {number} Available y position at given x, -1 if column is full
     */
    can_place(x) {
        let y = MAX_Y;
        while (y >= 0) {
            if (this.board[y][x] === "") {
                return y;
            } else {
                // y goes down as y=0 is at the top
                y--;
            }
        }
        return -1
    }

    /**
     * Determines if a player has won
     * @returns {string} The player that won the game
     */
    findWin() {
        let winner = this.for_every_in_board(function (color, x, y) {
            if (color !== '') {
                // console.log("checking " + x + " " + y + " for win");
                let b = state.board;
                // Top of vertical
                if (y <= MAX_Y - 3 && b[y + 1][x] === color && b[y + 2][x] === color && b[y + 3][x] === color) {
                    console.log(color + " win vertically " + " at " + x + " " + y);
                    return color;
                }
                // Leftmost of horizontal
                else if (x <= MAX_X - 3 && b[y][x + 1] === color && b[y][x + 2] === color && b[y][x + 3] === color) {
                    console.log(color + " win horizontally " + " at " + x + " " + y);
                    return color;
                }
                // Top left of NW - SE diagonal
                else if (x <= MAX_X - 3 && y <= MAX_Y - 3 && b[y + 1][x + 1] === color && b[y + 2][x + 2] === color && b[y + 3][x + 3] === color) {
                    console.log(color + " win NW - SE " + " at " + x + " " + y);
                    return color;
                }
                // Top right of NE - SW diagonal
                else if (x >= 3 && y <= MAX_Y - 3 && b[y + 1][x - 1] === color && b[y + 2][x - 2] === color && b[y + 3][x - 3] === color) {
                    console.log(color + " win NE - SW " + " at " + x + " " + y);
                    return color;
                }
            }
        });
        if (winner) {
            if (winner === 'r') {
                document.getElementById('winner').innerHTML = "Red Wins!";
            } else if (winner === 'y') {
                document.getElementById('winner').innerHTML = "Yellow Wins!";
            }
            this.socket.emit('endgame', {id: this.gameid});
        }
        return winner;
    }
}