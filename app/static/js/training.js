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
		if (data.status !== 'ok') {
			updateRating();
			return;
		}

		$('#rating').html('(' + data.elo + '&nbsp' + data.delta + ')');
		
		getBlunderInfo(blunder.id);
		if (finished) showComments();
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
		if (data.status !== 'ok') {
			// TODO: Show warning!
			return;
		}

		blunder = data;

		hideComments();
		getBlunderInfo(blunder.id);
			
		setStatus('playing');

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

	function buildCommentReplies(comments, parent_id) {
		var result = '';

		comments.forEach(function(c) {
			if (c.parent_id === parent_id) {
				result += commentBuilder(c, comments);
			}
		});

		return result;
	}

	function commentOnLike(comment_id) {
		return function() {
			console.log('Liking comment ', comment_id);
		}
	}

	function commentOnDislike(comment_id) {
		return function() {
			console.log('Disliking comment ', comment_id);
		}
	}

	function commentOnReply(comment_id) {
		return function() {
			console.log('Replying on ', comment_id);
		}
	}

	function commentBuilder(data, comments) {
		const header = '<div class="comment-header"><span class="comment-username">{0}</span> <span class="comment-date">{1}</span></div>';
		const body = '<div class="comment-body">{2}</div>';
		const controls = '<div class="comment-controls">{3} {4}</div>';
		const subcomments = '<ul class="comment-responses">{5}</ul>';

		const likeButton = '<a href="#" class="comment-like-button" id="comment-like-button-{0}"><i class="fa fa-thumbs-up"></i></a>'.format(data.id);
		const dislikeButton = '<a href="#" class="comment-dislike-button" id="comment-dislike-button-{0}"><i class="fa fa-thumbs-down"></i></a>'.format(data.id);
		
		const votesCount = data.likes - data.dislikes;

		var votesClass = "";
		if (votesCount > 0) {
			votesClass = 'green';
		} else if (votesCount < 0) {
			votesClass = 'red';
		}

		const voteData = '<span class="{0}">{1}</span>'.format(votesClass, votesCount);

		const commentRating = '<span class="comment-rating">{0} {1} {2}</span>'.format(dislikeButton, voteData, likeButton);

		const comment = '<li class="comment">' + header + body + controls + subcomments + '</li>';

		const replyButton = '<a id="comment-reply-button-{0}" href="#"><i class="fa fa-reply fa-rotate-90"></i> Reply</a>'.format(data.id);

		const subcommentsData = buildCommentReplies(comments, data.id);

		return comment.format(data.username, data.date, data.text, replyButton, commentRating, subcommentsData);
	}

	function onInfoRequest(data) {
		if (data.status === 'error') {
			// @TODO: Show Notifiy.Js
			return
		}

		if (data.myFavorite) {
			$('#favorite-icon').removeClass('fa-star-o').addClass('fa-star').addClass('active-star-icon');
		} else {
			$('#favorite-icon').removeClass('fa-star').addClass('fa-star-o').removeClass('active-star-icon');
		}

		$('#favorites').html(data.favorites);
		$('#likes').html(data.likes);
		$('#dislikes').html(data.dislikes);

		const successRate = (data.totalTries != 0)? (data.successTries * 100 / data.totalTries): 0; 

		$('#blunder-rating').html(data.elo);
		$('#success-played').html(data.successTries);
		$('#total-played').html(data.totalTries);
		$('#success-rate').html(successRate.toFixed(2));

		const htmlData = buildCommentReplies(data.comments, 0);
		$('#comments').html(htmlData);
		$('#comments-counter').html(data.comments.length);

		data.comments.forEach(function(comment) {
			$('#comment-like-button-' + comment.id).on('click', commentOnLike(comment.id));
			$('#comment-dislike-button-' + comment.id).on('click', commentOnDislike(comment.id));
			$('#comment-reply-button-' + comment.id).on('click', commentOnReply(comment.id));
		});
	}

	function getRandomBlunder() {
		$.ajax({
			type: 'POST',
			url: "/getRandomBlunder"
		}).done(onBlunderRequest);
	}

	function getBlunderInfo(blunder_id) {
		$.ajax({
			type: 'POST',
			url: "/getBlunderInfo",
			contentType: 'application/json',
			data: JSON.stringify({
				blunder_id: blunder_id
			})
		}).done(onInfoRequest);		
	}

	function voteBlunder(blunder_id, vote) {
		$.ajax({
			type: 'POST',
			url: "/voteBlunder",
			contentType: 'application/json',
			data: JSON.stringify({
				blunder_id: blunder_id,
				vote: vote
			})
		}).done(onInfoRequest);
	}

	function favoriteBlunder(blunder_id) {
		$.ajax({
			type: 'POST',
			url: "/favoriteBlunder",
			contentType: 'application/json',
			data: JSON.stringify({
				blunder_id: blunder_id
			})
		}).done(onInfoRequest);
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
			if (data.status !== 'ok') {
				// TODO: Show warning!
				return;
			}

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

	function showComments() {
		$('#comments').removeClass('hidden').addClass('visible');
		$('#comments-icon').removeClass('fa-angle-down').addClass('fa-angle-up');
	}

	function hideComments() {
		$('#comments').removeClass('visible').addClass('hidden');
		$('#comments-icon').removeClass('fa-angle-up').addClass('fa-angle-down');
	}

	function switchComments() {
		if ($('#comments').hasClass('hidden'))
			showComments();
		else
			hideComments();
	}

	$('#comments-spoiler').on('click', function() {
		switchComments();
	});

	$('#likeButton').on('click', function() {
		voteBlunder(blunder.id, 1);
	});

	$('#dislikeButton').on('click', function() {
		voteBlunder(blunder.id, -1);
	});

	$('#favoriteButton').on('click', function() {
		favoriteBlunder(blunder.id);
	});

})();