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

	var lockAnimation = function() {
		animationLocked = true;
		setTimeout(function() {
			animationLocked = false;
		}, moveSpeed + 20);
	};

	var onDragStart = function(source, piece, position, orientation) {
		if (finished === true ||
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
				text += '<span class="spacer"></span> ' + moveNumber + '.';
				++moveNumber;				
			}

			var mclass = 'move';
			if (discardLevel == orig.length) {
				mclass = 'currentMove';
			}

			id = 'moveLink' + moveNumber + (whiteMove? 'w': 'b');
			text += '&nbsp<a id="' + id + '" class="' + mclass + '" href="#">' + el + '</a>';
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
		console.log(move);
		pmove = game.move(move);
		console.log(pmove);
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

		// Process additional info from server
	}

	// Imitation getting request from server
	textBlunders = [
		{fen: "5qk1/2Q2pp1/6p1/1N1Bp3/pn2P3/3n1P2/6PP/6K1 w - - 2 35", blunderMove: "Nd6", pv: ["Nxd5", "Qc6", "N3b4", "Qxa4", "Qxd6"]},
		/*{fen: "5R2/7p/6k1/1r4p1/8/4K2P/8/8 w - - 0 69", blunderMove: "Kf3"},
		{fen: "3r4/5nkp/4Pr1b/3P4/2N5/6BP/6RK/3R4 b - - 0 45", blunderMove: "Rxe6"},
		{fen: "2r4r/p1p1k3/1p1R3p/1q2PQb1/8/2P5/PP3PP1/1K5R b - - 2 26", blunderMove: "Rce8"},
		{fen: "5rk1/p1p1q2p/1pnr2pQ/4pp1P/8/4B1P1/PPB4R/5RK1 b - - 0 26", blunderMove: "Nd4"},
		{fen: "2q2rk1/5pp1/p2Qpb1p/5N2/8/8/P2B1PPP/2R3K1 b - - 0 27", blunderMove: "Qxc1+"},
		{fen: "1N6/8/4k3/5p2/3p4/5P1p/5K2/8 w - - 0 52", blunderMove: "Na6"},
		{fen: "5r1k/1p2q1pp/p1b5/4P3/2p2r1P/4NN2/PP3PP1/1Q3K1R w - - 0 23", blunderMove: "Ng5"},
		{fen: "8/2pk4/2r1bp2/4p3/1Q1nPpPq/1P1P1P2/R4RBr/1KN5 w - - 1 37", blunderMove: "Qf8"},
		{fen: "7k/p4r1p/1p1pN3/2pP2N1/5P2/P3r3/1PP5/1K5R b - - 3 39", blunderMove: "Re7"},
		{fen: "r6k/1p3p2/4q2p/8/2p5/5QPP/Pp5K/3R4 b - - 0 32", blunderMove: "Rxa2"},
		{fen: "8/6pp/5p2/5P2/R5bk/8/P4K2/8 b - - 1 41", blunderMove: "Kg5"},
		{fen: "r3r1k1/1b3p2/1ppp1q2/p1n1b2p/P3P1p1/1PN1Q1PP/1BPR1P2/3R1BK1 w - h6 0 22", blunderMove: "Rxd6"},
		{fen: "4r1k1/1r3p1p/3pb1q1/3p2nN/3P1QP1/1PN1P3/P2K4/2R4R b - - 9 31", blunderMove: "h6"},
		{fen: "7k/pp2q3/2n4r/2p2Q2/P2pP2r/2P3R1/1P4B1/R5K1 b - - 3 34", blunderMove: "R4h5"},
		{fen: "3k4/Qpp3p1/3p1p1p/P2P1b2/1P6/5BPP/5PK1/4q3 b - - 3 29", blunderMove: "Qxb4"},
		{fen: "5rk1/1Q3n1p/3p2p1/8/2r2P1N/4q3/P5R1/5RK1 w - - 1 35", blunderMove: "Rff2"},
		{fen: "3r1bk1/2R2ppp/2b2r1q/1p1p2R1/3Q3P/PP4P1/1B3PBK/8 b - - 4 33", blunderMove: "Kh8"},
		{fen: "2r4k/4q2p/Q1nn4/2p2rp1/Pp2pP2/6P1/1P2N1BP/2R3NK b - - 8 30", blunderMove: "Nb8"},
		{fen: "1rb2r1k/p5qB/1n6/1pp1p1NQ/3p4/3P2P1/PPn2P1N/4R1K1 w - - 6 28", blunderMove: "Bf5+"},
		{fen: "6k1/RN3pp1/8/8/P6p/1P5n/2r5/7K w - - 0 36", blunderMove: "Nd8"},
		{fen: "r3r3/3B4/b6p/1p1Pk3/pR2PpP1/P1R5/1P3K1P/8 b - - 2 37", blunderMove: "Red8"},*/
	]

	onBlunderRequest(textBlunders[Math.floor(Math.random() * textBlunders.length)])

	$('#nextBlunder').on('click', function() {
		onBlunderRequest(textBlunders[Math.floor(Math.random() * textBlunders.length)])		
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