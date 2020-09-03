state = new gameState();

function mouseDownHandler(event) {
    let clickX = event.pageX - c.offsetLeft,
        clickY = event.pageY - c.offsetTop;
    let gridPos = screenPosToGridPos(clickX, clickY);
    if (state.myTurn) {
        state.place_stone(gridPos['x']);
    }
    drawBoard(state.board);
}

drawBoard(state.board);

c.addEventListener('mousedown', mouseDownHandler);
