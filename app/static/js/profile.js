(function generateStructure() {
    var blocks = [
        {
            caption: 'Blunders history',
            rows: [
                {
                    type: 'pager', 
                    id: 'blunder-history'
                }
            ]
        },
        {
            caption: 'Favorites',
            rows: [
                {
                    type: 'pager', 
                    id: 'blunder-favorites'
                }
            ]
        },
        {
            caption: 'Comments',
            rows: [
                {
                    type: 'pager', 
                    id: 'user-comments'
                }
            ]
        }
    ];

    var html = grid.generate(blocks, 3);
    $('#details').html(html);
})();

(function updateProfile() {
    function onUpdateProfileRequest(response) {
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }

        grid.update(response.data);
    }

    $.ajax({
        type: 'POST',
        url: "/getUserProfile",
        contentType: 'application/json',
        data: JSON.stringify({
            username: $.url('?user')
        })
    }).done(onUpdateProfileRequest);
})();

function generateTable(columnsNum, rowsNum, data, viewGenerator) {
    var rows = data.chunk(columnsNum).map(function(part) {
        var row = part.map(function(item) {
            return '<td>{0}</td>'.format(viewGenerator(item));
        }).join('');

        return '<tr>{0}</tr>'.format(row);
    }).join('');

    var content = '<table>{0}</table>'.format(rows);
    return content;
}

function id(x) {
    return x;
}

function sortByDate(data, options) {
    var opts = options || {};
    var address = opts.address || id;
    var orderFactor = (opts.reverse === true)? -1: +1;

    data.sort(function(elA, elB) {
        var aDate = new Date(address(elA));
        var bDate = new Date(address(elB));

        return (aDate - bDate) * orderFactor;
    });
}

function pieceTheme(piece) {
    return './static/third-party/chessboardjs/img/chesspieces/alpha/' + piece + '.png';
}

(function setupBlunderHistoryPager() {
    var columnsRow = 3;
    var rowsNum = 2;
    var itemsOnPage = columnsRow * rowsNum;
    
    var id = 'blunder-history';

    grid.setupPager(id, itemsOnPage, function(page) {
        $.ajax({
            type: 'POST',
            url: "/statistics/getBlundersHistory",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $.url('?user'),
                offset: (page - 1) * itemsOnPage,
                limit: itemsOnPage
            })
        }).done(function(response) {
            if (response.status !== 'ok') {
                notify.error(response.message);
                return;
            }

            sortByDate(response.data.blunders, {
                address: function(blunder) {
                    return blunder.date_start;
                },
                reverse: true
            });

            var content = generateTable(columnsRow, rowsNum, response.data.blunders, function(item) {
                var style = (item.result) ? 'blunder-history-board-win' : 'blunder-history-board-fail';
                var title = 'Date: {0}, Spent time: {1}'.format(item.date_start, utils.timePrettyFormat(item.spent_time));
                return '<div class="{0}" id="board-history-{1}" title="{2}" style="width: 180px"></div>'.format(style, item.blunder_id, title);
            });

            grid.updatePager(id, response.data.total, content);

            response.data.blunders.forEach(function(b) {
                var board = new ChessBoard('board-history-' + b.blunder_id, {
                    draggable: false,
                    position: b.fen,
                    pieceTheme: pieceTheme
                });
            });
        });
    });
})();

(function setupBlunderFavorites() {
    var columnsRow = 3;
    var rowsNum = 2;
    var itemsOnPage = columnsRow * rowsNum;
    
    var id = 'blunder-favorites';

    grid.setupPager(id, itemsOnPage, function(page) {
        $.ajax({
            type: 'POST',
            url: "/statistics/getBlundersFavorites",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $.url('?user'),
                offset: (page - 1) * itemsOnPage,
                limit: itemsOnPage
            })
        }).done(function(response) {
            if (response.status !== 'ok') {
                notify.error(response.message);
                return;
            }

            sortByDate(response.data.blunders, {
                address: function(blunder) {
                    return blunder.assign_date;
                },
                reverse: true
            });

            var content = generateTable(columnsRow, rowsNum, response.data.blunders, function(item) {
                var style = 'blunder-favorites-board';
                return '<div class="{0}" id="board-favorite-{1}" style="width: 180px"></div>'.format(style, item.blunder_id);
            });

            grid.updatePager(id, response.data.total, content);

            response.data.blunders.forEach(function(b) {
                var board = new ChessBoard('board-favorite-' + b.blunder_id, {
                    draggable: false,
                    position: b.fen,
                    pieceTheme: pieceTheme
                });
            });
        });
    });
})();

(function setupComments() {
    var itemsOnPage = 5;
    
    var id = 'user-comments';

    grid.setupPager(id, itemsOnPage, function(page) {
        $.ajax({
            type: 'POST',
            url: "/statistics/getCommentsByUser",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $.url('?user'),
                offset: (page - 1) * itemsOnPage,
                limit: itemsOnPage
            })
        }).done(function(response) {
            if (response.status !== 'ok') {
                notify.error(response.message);
                return;
            }

            var commentMaker = function(comment) {
                return '<div class="blunder-comment">{0}</div>'.format(utils.escapeHtml(comment.text));
            };

            var rows = '';
            for (var blunder_id in response.data.blunders) {
                var blunder = response.data.blunders[blunder_id];

                var style = 'comments-board';
                var boardContent = '<div class="{0}" id="board-comment-{1}" style="width: 180px"></div>'.format(style, blunder_id);
                
                var commentContent = blunder.comments.map(commentMaker).join('');

                rows += '<tr><td>{0}</td><td class="blunder-comment-cell">{1}</td></tr>'.format(boardContent, commentContent);
            }

            var content = '<table>{0}</table>'.format(rows);

            grid.updatePager(id, response.data.total, content);

            for (blunder_id in response.data.blunders) { // Defined upper
                blunder = response.data.blunders[blunder_id]; // Defined upper

                var board = new ChessBoard('board-comment-{0}'.format(blunder_id), {
                    draggable: false,
                    position: blunder.fen,
                    pieceTheme: pieceTheme
                });
            }
        });
    });
})();