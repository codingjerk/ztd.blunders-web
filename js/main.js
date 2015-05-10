(function() {
	var moveSpeed = 500;
	var board;
	var game;
	var animationLocked = false;
	var blunder;
	var firstMoveIndex = null;
	var firstMoveTurn = null;
	var visitedMoveCounter = 0;

	var multiPv = null;

	var finished = false;

	function getPv(index) {
		var result; 

		if (index === 'user') {
			result = game.history();
			result.tag = 'moves';
		} else if (index === 'original') {
			result = multiPv[0];
			result.tag = 'rightMoves';
		} else {
			result = multiPv[index];
		}

		result.index = index;

		return result;
	}

	var setStatus = function(status) {
		if (status === 'playing') {
			finished = false;
			$("#nextBlunder").html('<i class="fa fa-exclamation-circle"></i> Give up');
			$("#rightMoves").html('');
		} else if (status === 'failed') {
			finished = true;
			$("#nextBlunder").html('<i class="fa fa-lg fa-caret-right"></i> Next blunder');
			$("#status").html('<span id="failedStatus"><i class="fa fa-times-circle"></i> Failed!</span>');
		} else if (status === 'finished') {
			finished = true;
			$("#nextBlunder").html('<i class="fa fa-lg fa-caret-right"></i> Next blunder');
			$("#status").html('<span id="successStatus"><i class="fa fa-check-circle"></i> Success!</span>');
		}
	}

	var updateStatus = function() {
		if (!finished) {
			if (game.turn() == 'w') {
				$('#status').html('<span id="whiteTurnStatus">White&nbspto&nbspmove</span>');
			} else {
				$('#status').html('<span id="blackTurnStatus">Black&nbspto&nbspmove</span>');
			}
		}
	}

	var lockAnimation = function(time) {
		if (time === undefined) {
			time = moveSpeed + 20;
		}

		animationLocked = true;
		setTimeout(function() {
			animationLocked = false;
		}, time);
	};

	var onDragStart = function(source, piece, position, orientation) {
		if (animationLocked === true ||
			finished === true ||
			game.game_over() === true ||
		   (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
		   (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
				return false;
		}
	};

	var onDrop = function(source, target) {
		// see if the move is legal
		var move = makeMove(board, {
			from: source,
			to: target,
			promotion: 'q' // NOTE: always promote to a queen for example simplicity
		}, false);

		if (move === null) return 'snapback';

		var bestMove = blunder.pv[game.history().length - 2];

		if (move.san !== bestMove) {
			setStatus('failed');

			updatePv(getPv('original'));
		} else if (game.history().length - 1 === blunder.pv.length) {
			setStatus('finished');
		} else {
			var aiAnswer = blunder.pv[game.history().length - 1];
			setTimeout(function() {
				makeMove(board, aiAnswer, true);
				lockAnimation();
			}, 400);
		}
	};

	var onSnapEnd = function(source, target, piece) {
		board.position(game.fen());
	};

	function updatePv(pv, cutMoveNumber) {
		if (cutMoveNumber === undefined) {
			cutMoveNumber = pv.length;
		}

		text = '';

		for (var i = 0; i < cutMoveNumber && i < pv.length; ++i) {
			var move = pv[i];

			if (i !== 0 && i % 2 == 0) {
				text += '<span class="spacer"></span> ';
			}

			var style = 'move';
			if (i === game.history().length - 1 && multiPv.activeIndex === pv.index) {
				style = 'currentMove';
			}

			console.log(multiPv.activeIndex);
			console.log(pv.index);
			
			if (i % 2 == 0) {
				var moveNumber = Math.floor(i / 2) + 1 + firstMoveIndex;
				text += moveNumber + '.&nbsp';
			}

			var NAG = '';
			if (i == 0) NAG = '?';
			else if (i == 1) NAG = '!';

			if (pv[i] !== getPv('original')[i]) NAG = "??";

			if (i == 0 && firstMoveTurn === 'b') {
				text += '...';
			}

			text += '<a class="' + style + '" id="' + pv.tag + "_child_" + i + '" href="#">' + move + NAG + '</a>';
		}

		$('#' + pv.tag).html(text);

		for (var i = 0; i < cutMoveNumber; ++i) {
			$('#' + pv.tag + "_child_" + i).on('click', (function(pv, cutter) {
				return function() {
					var previousPvIndex = multiPv.activeIndex;
					multiPv.activeIndex = pv.index;

					if (previousPvIndex !== pv.index) {
						updatePv(getPv(previousPvIndex));
					}

					game.load(blunder.fenBefore);

					for (var i = 0; i <= cutter; ++i) {
						var move = pv[i];
						game.move(move);
					}

					board.position(game.fen());

					updatePv(pv, cutMoveNumber);
				};
			})(pv, i));
		}
	}

	function makeMove(board, move, aiMove) {
		pmove = game.move(move);
		if (pmove !== null) {
			++visitedMoveCounter;
			
			if (aiMove) {
				board.position(game.fen());
			}

			updatePv(getPv('user'), visitedMoveCounter);
			updateStatus();
		}

		return pmove;
	}

	function onBlunderRequest(data) {
		setStatus('playing');
		blunder = data;
		blunder.pv = blunder.pv.slice(0, 3);
		multiPv = [];
		multiPv.push([blunder.blunderMove].concat(blunder.pv));
		multiPv.activeIndex = 'user';

		console.log(multiPv);
		matches = data.fenBefore.match(/\d+/g);
		firstMoveIndex = +matches[matches.length - 1];

		visitedMoveCounter = 0;

		board.position(data.fenBefore, false);
		game.load(data.fenBefore);
		firstMoveTurn = game.turn();

		makeMove(board, data.blunderMove, true);
	}

	function getRandomBlunder() {
		$.ajax({
	        type: 'GET',
	        url: "http://localhost/grb", // TODO: FIX THIS
		}).done(onBlunderRequest);
	}

	board = new ChessBoard('board', {
		draggable: true,
		position: 'start',
		moveSpeed: moveSpeed,
		onDrop: onDrop,
		onDragStart: onDragStart,
		onSnapEnd: onSnapEnd
	});
	game = new Chess();

	getRandomBlunder();

	$('#nextBlunder').on('click', function() {
		getRandomBlunder();	
	});

	$('#goToGame').on('click', function() {
		window.open('http://www.google.com/search?q=' + blunder.fenBefore);
	});

	$('#flip').on('click', function(){
		board.flip();
	});

	$('#getFen').on('click', function() {
		window.prompt("Copy to clipboard: Ctrl+C, Enter", game.fen());
	});

	$('#firstMove').on('click', function() {
		// TODO
	});

	$('#previousMove').on('click', function(){
		// TODO
	});

	$('#nextMove').on('click', function() {
		// TODO
	});

	$('#lastMove').on('click', function() {
		// TODO
	});
})();