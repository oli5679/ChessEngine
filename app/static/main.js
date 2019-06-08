

$(document).ready(function () {
    var board,
    game = new Chess();
  
    // reset game
    $.ajax({
        url: "http://0.0.0.0:5000/reset",
        success: function( response ) {
            console.log(response); // server response
            console.log('Reset engine')
        }
    });

    // start with e2e4 - for now engine is always white
    $.ajax({
        url: 'http://0.0.0.0:5000/move',
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify( { "move": "e2e4" } ),
        success: function( data, textStatus, jQxhr ){
            console.log(data);
            console.log('played e2e4')
        },
        error: function( jqXhr, textStatus, errorThrown ){
            console.log( errorThrown );
        }
    });

    


  // do not pick up pieces if the game is over
  // only pick up pieces for White
  var onDragStart = function(source, piece, position, orientation) {
    if (game.in_checkmate() === true || game.in_draw() === true ||
      piece.search(/^b/) !== -1) {
      return false;
    }
  };
  
  var playAI = function() {
    var possibleMoves = game.moves();
  
    // game over
    if (possibleMoves.length === 0) return;
  
    var response = $.ajax({url: "demo_test.txt", success: function(result){
        $("#div1").html(result);
      }});;
    game.move(possibleMoves[randomIndex]);
    board.position(game.fen());
  };
  
  var onDrop = function(source, target) {
    // see if the move is legal
    var move = game.move({
      from: source,
      to: target,
      promotion: 'q' // NOTE: always promote to a queen for example simplicity
    });
      
      var move_string = source + target;
      console.log(move);

      
  
    // illegal move
    if (move === null) return 'snapback';
  
    // make random legal move for black
    window.setTimeout(makeRandomMove, 250);
  };
  
  // update the board position after the piece snap
  // for castling, en passant, pawn promotion
  var onSnapEnd = function() {
    board.position(game.fen());
  };
  
  var cfg = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd
  };
  board = ChessBoard('board', cfg);
});