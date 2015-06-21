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

function createItemGrid(columnsNum, rowsNum, data, model) {
    var rows = data.chunk(columnsNum).map(function(part){
        var row = part.map(function(item){
            return '<td>{0}</td>'.format(model(item));
        }).join('');

        return '<tr>{0}</tr>'.format(row);
    }).join('');

    var content = '<table>{0}</table>'.format(rows);
    return content;
}

(function setupBlunderHistoryPager() {
    var columnsRow = 3;
    var rowsNum = 2;
    var itemsOnPage = columnsRow * rowsNum;
    
    var id = 'blunder-history';

    function pieceTheme(piece) {
        return './static/third-party/chessboardjs/img/chesspieces/alpha/' + piece + '.png';
    }

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

            /*response.data.blunders.sort(function(a, b){
                    var aDate = new Date(a);
                    var bDate = new Date(b);
                    return (aDate > bDate);
                }); // descending order*/

            var content = createItemGrid(columnsRow, rowsNum, response.data.blunders, function(item){
                var style = (item.result) ? 'blunder-history-board-win' : 'blunder-history-board-fail';
                var title = 'Date: {0}, Spent time: {1}'.format(item.date_start, utils.timePrettyFormat(item.spent_time));
                return '<div class="{0}" id="board-history-{1}" title="{2}" style="width: 180px"></div>'.format(style, item.blunder_id, title);
            })

            grid.updatePager(id, response.data.total, content);

            response.data.blunders.forEach(function(b) {
                var board = new ChessBoard('board-history-' + b.blunder_id,{
                    draggable: false,
                    position: b.fen,
                    pieceTheme: pieceTheme
                });
            })
        });
    });
})();

(function setupBlunderFavorites() {
    var columnsRow = 3;
    var rowsNum = 2;
    var itemsOnPage = columnsRow * rowsNum;
    
    var id = 'blunder-favorites';

    function pieceTheme(piece) {
        return './static/third-party/chessboardjs/img/chesspieces/alpha/' + piece + '.png';
    }

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

            var content = createItemGrid(columnsRow, rowsNum, response.data.blunders, function(item){
                var style = 'blunder-favorites-board';
                return '<div class="{0}" id="board-favorite-{1}" style="width: 180px"></div>'.format(style, item.blunder_id);
            })

            grid.updatePager(id, response.data.total, content);

            response.data.blunders.forEach(function(b) {
                var board = new ChessBoard('board-favorite-' + b.blunder_id, {
                    draggable: false,
                    position: b.fen,
                    pieceTheme: pieceTheme
                });
            })
        });
    });
})();