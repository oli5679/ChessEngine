

$(document).ready(function () {  
  var board,
  game = new Chess();
  game.move({
    from: 'e2',
    to: 'e4',
  });
  
    // reset game
    $.ajax({
      url: "http://0.0.0.0:5000/reset",
        success: function( response ) {
            console.log(response); // server response
            console.log('Reset engine')
        },
        async: false
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
      },
      async: false
    });

    function makeRandomMove () {
      var possibleMoves = game.moves()
    
      // game over
      if (possibleMoves.length === 0) return
    
      var randomIdx = Math.floor(Math.random() * possibleMoves.length)
      game.move(possibleMoves[randomIdx])
      board.position(game.fen())
    }


  // do not pick up pieces if the game is over
  // only pick up pieces for White
  var onDragStart = function(source, piece, position, orientation) {
    if (game.in_checkmate() === true || game.in_draw() === true ||
      piece.search(/^w/) !== -1) {
      return false;
    }
  };
  
  var playAI = function(move_string) {
    var possibleMoves = game.moves();
  
    // game over
    if (possibleMoves.length === 0) return;
  
    $.ajax({
      url: 'http://0.0.0.0:5000/play',
      dataType: 'json',
      type: 'post',
      contentType: 'application/json',
      data: JSON.stringify( { "move": move_string } ),
      success: function( data, textStatus, jQxhr ){
        console.log(data);
        console.log('got response');
        game.move({
          from: data['from'],
          to: data['to'],
        })
        board.position(game.fen());
        console.log(game.fen());
      },
      error: function( jqXhr, textStatus, errorThrown ){
          console.log( errorThrown );
      },
      async: false
  });
    
  };
  
  var onDrop = function(source, target) {
    // see if the move is legal
    var move = game.move({
      from: source,
      to: target,
      promotion: 'q' // NOTE: always promote to a queen for example simplicity
    });
      
      var move_string = source + target;
      console.log(move_string);

      
  
    // illegal move
    if (move === null) return 'snapback';
  
    // get AI response from black
    playAI(move_string);    
  };
  
  // update the board position after the piece snap
  // for castling, en passant, pawn promotion
  var onSnapEnd = function() {
    board.position(game.fen());
  };
  
  var cfg = {
    draggable: true,
    position: "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1",
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd
  };
  board = ChessBoard('board', cfg);
});