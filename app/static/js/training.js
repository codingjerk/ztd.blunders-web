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

	var counter = utils.counter(1000, function () {
		var totalSeconds = counter.total();

		var formatted = utils.intervalPrettyFormat(totalSeconds);

		$('#spent-time-value').html(formatted);
	});

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

	var onResultAprooved = function(response) {
		if (response.status !== 'ok') {
			updateRating();
			notify.error(response.message);
			return;
		}

		if (response.data) { // Not anonymous
			var data = response.data;

			var deltaClass = '';
			if (data.delta > 0) {
				deltaClass = 'green';
				data.delta = '+{0}'.format(data.delta);
			} else if (data.delta < 0) {
				deltaClass = 'red';
			}

			$('#rating').html('({0}&nbsp<span class={1}>{2}</span>)'.format(data.elo, deltaClass, data.delta));
		}


		if (finished) {
			getBlunderInfo(blunder.id);
			showComments();
		}
	};

	var sendResult = function(callback) {
		history.replaceState({}, null, '/explore/' + blunder.id);
		grid.updateSpoiler('help-block', false);

		sync.ajax({
            id: 'loading-spin',
            url: '/api/blunder/validate',
            data: {
				id: blunder.id,
				line: getPv('user'),
				spentTime: counter.total(),
				type: 'rated'
			},
            onDone: function(response) {
				onResultAprooved(response);
				if (callback !== undefined) {
					callback(response);
				}
			}
        });

		counter.stop();
	};

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
	};

	var updateStatus = function() {
		if (!finished) {
			if (game.turn() == 'w') {
				$('#status').html('<span id="whiteTurnStatus">White&nbspto&nbspmove</span>');
			} else {
				$('#status').html('<span id="blackTurnStatus">Black&nbspto&nbspmove</span>');
			}
		}
	};

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

	var getMoveByIndex = function(pv, moveIndex) {
		var game = new Chess(blunder.fenBefore);

		var result = null;
		for (var i = 0; i < moveIndex; ++i) {
			result = game.move(pv[i]);
		}

		return result;
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
			setStatus('failed');
			sendResult();

			updatePv(getPv('original'));

			var bestMoveAsObject = getMoveByIndex(getPv('original'), gameLength);
			highlightAtFailure(bestMoveAsObject, move);

			return;
		}

		if (gameLength === getPv(0).length) {
			setStatus('finished');
			sendResult();

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

		highlightMove(lastMove);

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

			if (i !== 0 && i % 2 === 0) {
				text += '<span class="spacer"></span> ';
			}

			var style = 'move';
			if (i === game.history().length - 1 && multiPv.activeIndex === pv.index) {
				style += ' currentMove';
			}

			if (i % 2 === 0) {
				var moveNumber = Math.floor(i / 2) + 1 + firstMoveIndex;
				text += moveNumber + '.&nbsp';
			}

			var NAG = '';
			if (i === 0) {
				NAG = '?';
			} else if (i === 1) {
				NAG = '!';
			}

			if (pv[i] !== getPv('original')[i]) {
				NAG = "??";
				style += ' badMove';
			}

			if (getPv('user').length > i && pv[i] !== getPv('user')[i]) {
				style += ' goodMove';
			}

			if (i === 0 && firstMoveTurn === 'b') {
				text += '...';
			}

			text += '<a class="{0}" id="{1}">{2}{3}</a>'.format(style, pv.tag + "_child_" + i, move, NAG);
		}

		$('#' + pv.tag).html(text);

		var gotoMaker = function(pv, cutter) {
			return function() {
				gotoMove(pv, cutter, cutMoveNumber);
			};
		};

		for (i = 0; i < cutMoveNumber; ++i) {
			$('#' + pv.tag + "_child_" + i).on('click', gotoMaker(pv, i));
		}
	}

	function highlightMove(move) {
		$('.highlight').removeClass('highlight');
		$('.good-highlight').removeClass('good-highlight');
		$('.bad-highlight').removeClass('bad-highlight');

		$('#board').find('.square-' + move.from).addClass('highlight');
		$('#board').find('.square-' + move.to).addClass('highlight');
	}

	function highlightAtFailure(goodMove, badMove) {
		$('.highlight').removeClass('highlight');
		$('.good-highlight').removeClass('good-highlight');
		$('.bad-highlight').removeClass('bad-highlight');

		$('#board').find('.square-' + goodMove.from).addClass('good-highlight');
		$('#board').find('.square-' + goodMove.to).addClass('good-highlight');

		$('#board').find('.square-' + badMove.from).addClass('bad-highlight');
		$('#board').find('.square-' + badMove.to).addClass('bad-highlight');
	}

	function makeMove(board, move, aiMove) {
		pmove = game.move(move);
		if (pmove !== null) {
			++visitedMoveCounter;

			highlightMove(pmove);

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

	function onBlunderRequest(response) {
		if (response.status !== 'ok') {
			notify.error(response.message);
			return;
		}

		blunder = response.data;

		hideComments();
		getBlunderInfo(blunder.id);

		setStatus('playing');

		multiPv = [];
		multiPv.push([blunder.blunderMove].concat(blunder.forcedLine));
		multiPv.activeIndex = 'user';

		matches = blunder.fenBefore.match(/\d+/g);
		firstMoveIndex = +matches[matches.length - 1];

		visitedMoveCounter = 0;

		board.position(blunder.fenBefore, false);
		game.load(blunder.fenBefore);
		firstMoveTurn = game.turn();

		makeMove(board, blunder.blunderMove, true);

		counter.start();
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

	function voteBlunderComment(blunder_id, comment_id, vote) {
		sync.ajax({
				id: 'loading-spin',
				url: "/api/comment/vote",
				data: {
					blunder_id: blunder_id,
					comment_id: comment_id,
					vote: vote
				},
				onDone: onInfoRequest
		});
	}

	function commentOnReply(comment_id) {
		return function() {
			var buttons = '<a class="submit-comment-button"><i class="fa fa-check"></i> Submit</a>' +
				'<a class="cancel-comment-button"><i class="fa fa-times"></i> Cancel</a>';

			var editField = '<div><textarea rows="2" cols="40"></textarea></div>' + buttons;

			var controls = '#comment-controls-' + comment_id;
			var userinput = '#comment-user-input-' + comment_id;

			$(controls).css('visibility', 'hidden');
			$(userinput).html(editField);

			var textarea = $(userinput + '>div>textarea');

			function closeReplyField() {
				$(controls).css('visibility', 'visible');
				$(userinput).html('');
			}

			function reply() {
				sendComment(blunder.id, comment_id, textarea.val());
				closeReplyField();
			}

			$(userinput + '>.cancel-comment-button').on('click', closeReplyField);

			$(userinput + '>.submit-comment-button').on('click', reply);

			textarea.keyup(function(event) {
				var keyCode = event.keyCode || event.which;

				if (keyCode === 13 && event.ctrlKey) { // Ctrl+Enter key
					reply();
				}
			});
		};
	}

	function commentBuilder(data, comments) {
		var header = '<div class="comment-header"><span class="comment-avatar"><img src="/static/img/default-avatar.png" /></span><span class="comment-username">{0}</span> <span class="comment-date">{1}</span></div>';
		var body = '<div class="comment-body">{2}</div>';
		var controls = '<div id="comment-controls-' + data.id + '" class="comment-controls">{3} {4}</div><div id="comment-user-input-' + data.id + '"></div>';
		var subcomments = '<ul class="comment-responses">{5}</ul>';

		var likeButton = '<a class="comment-like-button" id="comment-like-button-{0}"><i class="fa fa-thumbs-up"></i></a>'.format(data.id);
		var dislikeButton = '<a class="comment-dislike-button" id="comment-dislike-button-{0}"><i class="fa fa-thumbs-down"></i></a>'.format(data.id);

		var votesCount = data.likes - data.dislikes;

		var votesClass = "";
		if (votesCount > 0) {
			votesClass = 'green';
		} else if (votesCount < 0) {
			votesClass = 'red';
		}

		var voteData = '<span class="{0}">{1}</span>'.format(votesClass, votesCount);

		var commentRating = '<span class="comment-rating">{0} {1} {2}</span>'.format(dislikeButton, voteData, likeButton);

		var comment = '<li class="comment">' + header + body + controls + subcomments + '</li>';

		var replyButton = '<a id="comment-reply-button-{0}"><i class="fa fa-reply fa-rotate-90"></i> Reply</a>'.format(data.id);

		var subcommentsData = buildCommentReplies(comments, data.id);

		return comment.format(
			data.username,
			utils.timePrettyFormat(data.date),
		    utils.escapeHtml(data.text),
			replyButton,
			commentRating,
			subcommentsData
		);
	}

	function onInfoRequest(response) {
		if (response.status === 'error') {
			notify.error(response.message);
			return;
		}

		data = response.data;

		if(data.hasOwnProperty('my')) {
			if (data.my.favorite) {
				$('#favorite-icon').removeClass('fa-star-o').addClass('fa-star').addClass('active-star-icon');
			} else {
				$('#favorite-icon').removeClass('fa-star').addClass('fa-star-o').removeClass('active-star-icon');
			}
		}

		$('#favorites').html(data.favorites);
		$('#likes').html(data.likes);
		$('#dislikes').html(data.dislikes);

		var info = data['game-info'];
		grid.update({
			'white-name-value': info.White,
			'white-elo-value':  info.WhiteElo,
			'black-name-value': info.Black,
			'black-elo-value':  info.BlackElo
		});

		var successRate = (data.history.total !== 0)? (data.history.success * 100 / data.history.total): 0;
		grid.update({
			'blunder-rating': data.elo,
			'success-played': data.history.success,
			'total-played': data.history.total,
			'success-rate': successRate.toFixed(1)
		});

		var rootComment = '<a id="comment-reply-button-0"><i class="fa fa-reply fa-rotate-90"></i> Describe...</a>';
		var rootControls = '<div id="comment-controls-0" class="comment-controls">' + rootComment + '</div><div id="comment-user-input-0"></div>';

		var htmlData = rootControls + "<ul>{0}</ul>".format(buildCommentReplies(data.comments, 0));
		$('#comments').html(htmlData);
		$('#comments-counter').html(data.comments.length);

		$('#comment-reply-button-0').on('click', commentOnReply(0));

		data.comments.forEach(function(comment) {
			$('#comment-like-button-' + comment.id).on('click', function() {
				voteBlunderComment(blunder.id, comment.id, 1);
			});

			$('#comment-dislike-button-' + comment.id).on('click', function() {
				voteBlunderComment(blunder.id, comment.id, -1);
			});

			$('#comment-reply-button-' + comment.id).on('click', commentOnReply(comment.id));
		});
	}

	window.onpopstate = function(event) {
		location.reload();
    };

	function getRatedBlunder() {
		if ($.url('path') !== '/training') {
			history.pushState({}, null, '/training');
		}

		sync.ajax({
            id: 'loading-spin',
            url: '/api/blunder/get',
            data: {type: 'rated'},
            onDone: onBlunderRequest
        });
	}

	function getBlunderInfo(blunder_id) {
		$.ajax({
			type: 'POST',
			url: "/api/blunder/info",
			contentType: 'application/json',
			data: JSON.stringify({
				blunder_id: blunder_id
			})
		}).done(onInfoRequest);
	}

	function voteBlunder(blunder_id, vote) {
		sync.ajax({
            id: 'loading-spin',
            url: '/api/blunder/vote',
            data: {
				blunder_id: blunder_id,
				vote: vote
			},
            onDone: onInfoRequest
        });
	}

	function favoriteBlunder(blunder_id) {
		sync.ajax({
            id: 'loading-spin',
			url: "/api/blunder/favorite",
			data: {
				blunder_id: blunder_id
			},
			onDone: onInfoRequest
		});
	}

	function sendComment(blunder_id, comment_id, text) {
		sync.ajax({
				id: 'loading-spin',
				url: "/api/comment/send",
				data: {
					blunder_id: blunder_id,
					comment_id: comment_id,
					user_input: text
				},
				onDone: onInfoRequest
		});
	}

	function pieceTheme(piece) {
		return '/static/third-party/chessboardjs/img/chesspieces/alpha/' + piece + '.png';
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

	getRatedBlunder();

	function updateRating() {
		$.ajax({
			type: 'GET',
			url: "/api/session/rating"
		}).done(function(data) {
			if (data.status !== 'ok') {
				notify.error(data.message);
				return;
			}

			$('#rating').html('(' + data.rating + ')');
		});
	}

	updateRating();

	function previousMove() {
		if (game.history().length <= 1) gotoRoot();
		else gotoMove(getPv('active'), game.history().length - 2, getPv('active').length);
	}

	function nextMove() {
		if (game.history().length >= getPv('active').length) return;
		gotoMove(getPv('active'), game.history().length, getPv('active').length);
	}

	function showComments() {
		grid.updateSpoiler('comments-block', true);
	}

	function hideComments() {
		grid.updateSpoiler('comments-block', false);
	}

	$('#nextBlunder').on('click', function() {
		if (!blunder) {
			return;
		}

		if (finished) {
			getRatedBlunder();
		} else {
			sendResult(getRatedBlunder);
		}

		// Clearing blunder to know about unloaded state
		blunder = undefined;
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

	$('#previousMove').on('click', previousMove);

	$('#nextMove').on('click', nextMove);

	$('#lastMove').on('click', function() {
		gotoMove(getPv('active'), getPv('active').length - 1, getPv('active').length);
	});

	$('#likeButton').on('click', function() {
		if (!blunder) {
			notify.error('Blunder is not loaded yet');
			return;
		}

		voteBlunder(blunder.id, 1);
	});

	$('#dislikeButton').on('click', function() {
		if (!blunder) {
			notify.error('Blunder is not loaded yet');
			return;
		}

		voteBlunder(blunder.id, -1);
	});

	$('#favoriteButton').on('click', function() {
		if (!blunder) {
			notify.error('Blunder is not loaded yet');
			return;
		}

		favoriteBlunder(blunder.id);
	});

	$(document).keydown(function(event) {
		if (event.target.type === 'textarea') return;

		var keyCode = event.keyCode || event.which;
		var arrow = {left: 37, right: 39};

		if (keyCode == arrow.left) {
			previousMove();
		} else if (keyCode == arrow.right) {
			nextMove();
		}
	});
})();

(function setupRightPanel() {
	var model = [
        {
            id: 'help-block',
            caption: 'Help',
            rows: [
                {
                    type: 'wide',
                    id: 'help'
                }
            ]
        },
        {
            id: 'game-block',
            caption: 'Game',
            cells: 2,
            rows: [
                {
                    type: 'cell',
                    label: 'White',
                    id: 'white-name-value',
                    additional: 'player'
                },
                {
                    type: 'cell',
                    label: 'Black',
                    id: 'black-name-value',
                    additional: 'player'
                },
                {
                    type: 'cell',
                    label: 'White',
                    id: 'white-elo-value',
                    additional: 'Elo'
                },
                {
                    type: 'cell',
                    label: 'Black',
                    id: 'black-elo-value',
                    additional: 'Elo'
                }
            ]
        },
        {
            id: 'blunder-block',
            caption: 'Blunder',
            cells: 3,
            rows: [
                {
                    type: 'cell',
                    label: 'Rating',
                    id: 'blunder-rating',
                    additional: 'Elo'
                },
                {
                    type: 'cell',
                    label: '',
                    id: 'dummy',
                    additional: ''
                },
                {
                    type: 'cell',
                    label: 'Spent',
                    id: 'spent-time-value',
                    additional: 'time'
                },
                {
                    type: 'cell',
                    label: 'Success',
                    id: 'success-played',
                    additional: 'played'
                },
                {
                    type: 'cell',
                    label: 'Total',
                    id: 'total-played',
                    additional: 'played'
                },
                {
                    type: 'cell',
                    label: 'Success rate',
                    id: 'success-rate',
                    additional: 'percents'
                }
            ]
        },
        {
            id: 'comments-block',
            caption: 'Comments',
            rows: [
                {
                    type: 'wide',
                    id: 'comments'
                }
            ]
        }
    ];

    var content = grid.generate(model);
    $('#info-block').html(content);

    grid.setupSpoiler('help-block', true);
    grid.setupSpoiler('comments-block', false);
    grid.setupSpoiler('blunder-block', true);
    grid.setupSpoiler('game-block', true);

    grid.update({'help':
    	'The player has just made a fatal mistake.\n' +
		'Play the best moves to obtain advantage.\n' +
		"There's only one winning variation wins at least 2 pawns."
	});
})();
