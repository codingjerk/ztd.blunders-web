(function generateStructure() {
    var blocks = [
    {
        caption: 'History',
        rows: [
            {
                type: 'pager', 
                id: 'blunder-history'
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

(function setupBlunderHistoryPager() {
    var itemsInRow = 3;
    var itemRows = 2;
    var itemsOnPage = itemsInRow * itemRows;
    
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

            response.data.blunders.sort(function(a, b){return (a.date_start < b.date_start)}); // descending order
            var rows = response.data.blunders.chunk(itemsInRow).map(function(part){
                var row = part.map(function(b){
                    var style = (b.result) ? 'blunder-history-board-win' : 'blunder-history-board-fail';
                    var title = 'Date: {0}, Spent time: {1}'.format(b.date_start, utils.timePrettyFormat(b.spent_time));
                    return '<td><div class="{0}" id="board-{1}" title="{2}" style="width: 180px"></div></td>'.format(style, b.blunder_id, title);
                }).join('');

                return '<tr>{0}</tr>'.format(row);
            }).join('');

            var content = '<table>{0}</table>'.format(rows);

            grid.updatePager(id, response.data.total, content);

            response.data.blunders.forEach(function(b) {
                var board = new ChessBoard('board-' + b.blunder_id,{
                    draggable: false,
                    position: b.fen,
                    pieceTheme: pieceTheme
                });
            })
        });
    });
})();