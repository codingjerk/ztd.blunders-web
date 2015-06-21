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
    var itemsOnPage = 10;
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

            var rows = response.data.blunders.map(function(b) {
                var style = (b.result == true)? "row-win": "row-fail";
                return '<tr class={0}><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>'.format(style, b.blunder_id, b.result, b.fen, b.spent_time);
            }).join('');

            var content = '<table>{0}</table>'.format(rows);

            grid.updatePager(id, response.data.total, content);
        });
    });
})();