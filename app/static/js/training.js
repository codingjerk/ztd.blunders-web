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

	String.prototype.format = function() {
		var str = this;
		for (var i = 0; i < arguments.length; i++) {
			var reg = new RegExp("\\{" + i + "\\}", "gm");
			str = str.replace(reg, arguments[i]);
		}
		return str;
	}

	function getPv(index) {
		var result; 

		if (index === 'user') {
			result = multiPv[1];
			result.tag = 'moves';
		} else if (index === 'original') {
			result = multiPv[0];
			result.tag = 'rightMoves';
		} else if (index === 'active') {
			return getPv(multiPv.activeIndex);
		} else {
			result = multiPv[index];
		}

		result.index = index;

		return result;
	}

	var onResultAprooved = function(data) {
		$('#rating').html('(' + data.elo + '&nbsp' + data.delta + ')');
	}

	var sendResult = function() {
		$.ajax({
			type: 'POST',
			url: "/validateBlunder",
			contentType: 'application/json',
			data: JSON.stringify({
				id: blunder.id,
				line: getPv('user')
			})
		}).done(onResultAprooved);
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
		    game.history().length < visitedMoveCounter ||
		    game.turn() !== piece[0]) 
		{
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

		var gameLength = game.history().length;

		var bestMove = getPv(0)[gameLength - 1];

		if (move.san !== bestMove) {
			sendResult();

			setStatus('failed');
			updatePv(getPv('original'));

			return;
		}

		if (gameLength === getPv(0).length) {
			sendResult();

			setStatus('finished');
			return;
		}

		var aiAnswer = getPv(0)[gameLength];
		setTimeout(function() {
			makeMove(board, aiAnswer, true);
			lockAnimation();
		}, 400);
	};

	var onSnapEnd = function(source, target, piece) {
		board.position(game.fen());
	};

	var gotoRoot = function() {
		$('.highlight').removeClass('highlight');

		game.load(blunder.fenBefore);
		board.position(game.fen(), false);

		updatePv(getPv('active'), getPv('active').length);
	};

	var gotoMove = function(pv, cursor, cutMoveNumber) {
		if (animationLocked === true) return;

		var previousPv = getPv('active');
		multiPv.activeIndex = pv.index;
		updatePv(previousPv);

		game.load(blunder.fenBefore);

		var lastMove;
		for (var i = 0; i <= cursor; ++i) {
			var move = pv[i];
			lastMove = game.move(move);
		}

		hightlightMove(lastMove);
		
		lockAnimation();
		board.position(game.fen());

		updatePv(pv, cutMoveNumber);
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
				style += ' currentMove';
			}
			
			if (i % 2 == 0) {
				var moveNumber = Math.floor(i / 2) + 1 + firstMoveIndex;
				text += moveNumber + '.&nbsp';
			}

			var NAG = '';
			if (i == 0) NAG = '?';
			else if (i == 1) NAG = '!';

			if (pv[i] !== getPv('original')[i]) {
				NAG = "??";
				style += ' badMove';
			}

			if (i == 0 && firstMoveTurn === 'b') {
				text += '...';
			}

			text += '<a class="{0}" id="{1}" href="#">{2}{3}</a>'.format(style, pv.tag + "_child_" + i, move, NAG);
		}

		$('#' + pv.tag).html(text);

		for (var i = 0; i < cutMoveNumber; ++i) {
			$('#' + pv.tag + "_child_" + i).on('click', (function(pv, cutter) {
				return function() {
					gotoMove(pv, cutter, cutMoveNumber);
				};
			})(pv, i));
		}
	}

	function hightlightMove(move) {
		$('.highlight').removeClass('highlight');

		$('#board').find('.square-' + move.from).addClass('highlight');
		$('#board').find('.square-' + move.to).addClass('highlight');
	}

	function makeMove(board, move, aiMove) {
		pmove = game.move(move);
		if (pmove !== null) {
			++visitedMoveCounter;

			hightlightMove(pmove);
			
			if (aiMove) {
				lockAnimation();
				board.position(game.fen());
			}

			if (!finished) {
				multiPv[1] = game.history();
			}

			updatePv(getPv('user'), visitedMoveCounter);
			updateStatus();
		}

		return pmove;
	}

	function onBlunderRequest(data) {
		setStatus('playing');

		blunder = data;

		multiPv = [];
		multiPv.push([blunder.blunderMove].concat(blunder.forcedLine));
		multiPv.activeIndex = 'user';

		matches = data.fenBefore.match(/\d+/g);
		firstMoveIndex = +matches[matches.length - 1];

		console.log(multiPv[0])
		console.log('Elo:', blunder.elo)

		visitedMoveCounter = 0;

		board.position(data.fenBefore, false);
		game.load(data.fenBefore);
		firstMoveTurn = game.turn();

		makeMove(board, data.blunderMove, true);
	}

	function getRandomBlunder() {
		$.ajax({
			type: 'GET',
			url: "/getRandomBlunder"
		}).done(onBlunderRequest);
	}

	function pieceTheme(piece) {
		return './static/third-party/chessboardjs/img/chesspieces/alpha/' + piece + '.png';
	}

	board = new ChessBoard('board', {
		draggable: true,
		position: 'start',
		pieceTheme: pieceTheme,
		moveSpeed: moveSpeed,
		onDrop: onDrop,
		onDragStart: onDragStart,
		onSnapEnd: onSnapEnd
	});
	game = new Chess();

	getRandomBlunder();

	function updateRating() {
		$.ajax({
			type: 'GET',
			url: "/getRating"
		}).done(function(data) {
			$('#rating').html('(' + data.rating + ')');
		});
	}

	updateRating();

	$('#nextBlunder').on('click', function() {
		if (!finished) sendResult();

		getRandomBlunder();	
	});

	$('#goToGame').on('click', function() {
		window.open('http://www.google.com/search?q=' + blunder.fenBefore);
	});

	$('#flip').on('click', function(){
		highlighted = $('.highlight');
		squares = [];
		for (var i = 0; i < highlighted.length; ++i) {
			squares.push(highlighted[i].getAttribute('data-square'));
		}

		board.flip();

		squares.forEach(function(square) {
			$('#board').find('.square-' + square).addClass('highlight');
		});
	});

	$('#getFen').on('click', function() {
		window.prompt("Copy to clipboard: Ctrl+C, Enter", game.fen());
	});

	$('#firstMove').on('click', function() {
		gotoRoot();
	});

	$('#previousMove').on('click', function() {
		if (game.history().length <= 1) gotoRoot();
		else gotoMove(getPv('active'), game.history().length - 2, getPv('active').length);
	});

	$('#nextMove').on('click', function() {
		if (game.history().length >= getPv('active').length) return;
		gotoMove(getPv('active'), game.history().length, getPv('active').length);
	});

	$('#lastMove').on('click', function() {
		gotoMove(getPv('active'), getPv('active').length - 1, getPv('active').length);
	});

	$('footer>ul>li>a,nav>ul>li>a,nav>ul>li>ul>li>a').on('click', function() {
        return confirm('Are you sure?');
	});
})();