(function() {
	var moveSpeed = 500;
	var board;
	var game;
	var additionalHistory = [];
	var animationLocked = false;
	var blunder;
	var firstMoveIndex = null;

	var finished = false;

	var setStatus = function(status) {
		if (status === 'playing') {
			finished = false;
			$("#nextBlunder").html('<i class="fa fa-exclamation-circle"></i> Give up');
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
		var move = game.move({
			from: source,
			to: target,
			promotion: 'q' // NOTE: always promote to a queen for example simplicity
		});

		// illegal move
		if (move === null) return 'snapback';

		var bestMove = blunder.pv[game.history().length - 2];

		if (move.san !== bestMove) {
			setStatus('failed');
		} else if (game.history().length - 1 === blunder.pv.length) {
			setStatus('finished');
		} else {
			var aiAnswer = blunder.pv[game.history().length - 1];
			setTimeout(function() {
				makeMove(board, aiAnswer);
				lockAnimation();
			}, 400);
		}

		additionalHistory = [];

		updateMoves();
	};

	var onSnapEnd = function() {
		board.position(game.fen());
	};

	board = new ChessBoard('board', {
		draggable: true,
		position: 'start',
		moveSpeed: moveSpeed,
		onDrop: onDrop,
		onDragStart: onDragStart,
		onSnapEnd: onSnapEnd
	});
	game = new Chess();

	function updateMoves() {
		if (!finished) {
			if (game.turn() == 'w') {
				$('#status').html('<span id="whiteTurnStatus">White&nbspto&nbspmove</span>');
			} else {
				$('#status').html('<span id="blackTurnStatus">Black&nbspto&nbspmove</span>');
			}
		}

		var orig = game.history();
		var moves = orig.concat(additionalHistory);

		var moveNumber = firstMoveIndex;
		var text = '';

		var whiteMove = true;
		if ((orig.length % 2 === 0) !== (game.turn() === 'w')) {
			text = firstMoveIndex + '.&nbsp;...';
			whiteMove = false;
			++moveNumber;
		}

		var discardLevel = 1;
		var discards = [];
		moves.forEach(function(el) {
			if (whiteMove) {
				text += '<span class="spacer"></span> ' + moveNumber + '.&nbsp';
				++moveNumber;				
			}

			var mclass = 'move';
			if (discardLevel == orig.length) {
				mclass = 'currentMove';
			}

			id = 'moveLink' + moveNumber + (whiteMove? 'w': 'b');
			text += '<a id="' + id + '" class="' + mclass + '" href="#">' + el + '</a>';
			discards.push({id: id, level: discardLevel});

			whiteMove = !whiteMove;
			++discardLevel;
		});

		$('#moves').html(text.replace(/^<span class="spacer"><\/span>/,""));

		discards.forEach(function(e) {
			$("#" + e.id).on('click', undoer(orig.length - e.level));
		});
	}

	function makeMove(board, move) {
		pmove = game.move(move);
		board.move(pmove.from + '-' + pmove.to);

		updateMoves();
	}

	function onBlunderRequest(data) {
		setStatus('playing');
		blunder = data;
		matches = data.fen.match(/\d+/g);
		firstMoveIndex = Math.round(matches[matches.length - 1] / 2);

		additionalHistory = [];

		board.position(data.fen, false);
		game.load(data.fen);
		makeMove(board, data.blunderMove);
	}

	function getRandomBlunder() {
		$.ajax({
	        type: 'GET',
	        url: "http://localhost/grb", // TODO: FIX THIS
		}).done(onBlunderRequest);
	}

	getRandomBlunder();

	$('#nextBlunder').on('click', function() {
		getRandomBlunder();	
	});

	$('#goToGame').on('click', function() {
		window.open('http://www.google.com/search?q=' + blunder.fen);
	});

	function undoer(num) {
		return function() {
			if (animationLocked) return;
			lockAnimation();

			for (var i = 0; i < num; ++i) {
				undoMove('no lock');
			}

			if (num < 0) {
				for (var i = 0; i < -num; ++i) {
					game.move(additionalHistory.shift());
				}
			}

			updatePos();
		}
	}

	function updatePos() {
		board.position(game.fen());
		updateMoves();
	}

	function undoMove(noLock) {
		if (game.history().length <= 1) return;
		if (noLock === undefined) {
			if (animationLocked) return;
			lockAnimation();
		}

		lastMove = game.history()[game.history().length - 1];
		game.undo();
		additionalHistory.unshift(lastMove);

		if (noLock === undefined) {
			updatePos();
		}
	}

	$('#firstMove').on('click', function() {
		undoer(game.history().length - 1)();
	});

	$('#previousMove').on('click', function(){undoMove();});

	$('#flip').on('click', function(){board.flip();});

	$('#nextMove').on('click', function() {
		if (additionalHistory.length === 0) return;
		if (animationLocked) return;
		lockAnimation();
		
		var move = additionalHistory.shift();
		makeMove(board, move);
	});

	$('#lastMove').on('click', function() {
		if (additionalHistory.length === 0) return;
		if (animationLocked) return;
		lockAnimation();

		while (additionalHistory.length != 0) {
			game.move(additionalHistory.shift());
		};

		updatePos();
	});

	$('#getFen').on('click', function() {
		window.prompt("Copy to clipboard: Ctrl+C, Enter", game.fen());
	});
})();