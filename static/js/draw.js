let c = document.getElementById("canvas");
let ctx = c.getContext("2d");

ctx.fillStyle = "#0a0e8b";
ctx.fillRect(0, 0, c.width, c.height);

function drawBoard(board) {
    for (let x = 0; x <= MAX_X; x++) {
        for (let y = 0; y <= MAX_Y; y++) {
            if (board[y][x] === "r") {
                ctx.fillStyle = "#F00";
            } else if (board[y][x] === "y") {
                ctx.fillStyle = "#FF0";
            } else {
                ctx.fillStyle = "#FFF";
            }
            ctx.beginPath();
            ctx.arc(x * 100 + 50, y * 100 + 50, 44, 0, 2 * Math.PI);
            ctx.fill();
        }
    }
}