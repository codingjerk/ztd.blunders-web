(function generateStructure() {
    var blocks = [
        {
            id: 'users-block',
            caption: 'Users',
            rows: [
                {
                    type: 'wide', 
                    id: 'users-rating-destribution'
                },
                {
                    type: 'cell',
                    label: 'Registered',
                    id: 'users-registered-value',
                    additional: 'users'
                },
                {
                    type: 'cell',
                    label: 'Online',
                    id: 'users-online-value',
                    additional: 'users'
                },
                {
                    type: 'cell',
                    label: 'Active',
                    id: 'users-active-value',
                    additional: 'users'
                }
            ]
        },
        {
            id: 'top-block',
            caption: 'Top 10',
            rows: [
                {
                    type: 'wide',
                    id: 'users-top-list'
                }
            ]
        },
        {
            id: 'blunders-block',
            caption: 'Blunders',
            rows: [
                {
                    type: 'wide', 
                    id: 'blunders-rating-destribution'
                },
                {
                    type: 'cell',
                    label: 'Total',
                    id: 'total-blunders-value',
                    additional: 'blunders'
                }
            ]
        },
        {
            id: 'online-block',
            caption: 'Online',
            rows: [
                {
                    type: 'wide', 
                    id: 'users-online-list'
                }
            ]
        }
    ];

    var html = grid.generate(blocks);
    $('#details').html(html);
})();

(function updateUsersStatistics() {
    function updateUsersOnlineList(id, users) {
        var usersLinks = users.map(function(user) {
            return '<a href="/profile?user={0}">{1}</a> '.format(user,user);
        }).join('');

        $('#' + id).html(usersLinks);
    }

    function updateUsersTopList(id, users) {
        var usersList = users.map(function(user) {
            var username = user.username;
            var elo = user.elo;
            return '<tr><td><a href="/profile?user={0}">{1}</a></td><td>{2}</td></tr>'.format(username, username, elo);
        }).join('');

        var content = '<table>{0}</table>'.format(usersList);
        $('#' + id).html(content);
    }

    function onUpdateUsersRequest(response) {
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }

        grid.update(response.data, {  "users-online-list" : updateUsersOnlineList,
                                      "users-top-list":     updateUsersTopList    });
    }

    $.ajax({
        type: 'GET',
        url: "/statistics/getUsersStatistics",
        contentType: 'application/json'
    }).done(onUpdateUsersRequest);
})();

(function updateUsersRatingChart() {
    function updateUsersRating(id, data){
        data.sort();

        var xElo = data.map(function(el){return el[0];});
        var yCount = data.map(function(el){return el[1];});

        utils.normalizeTicks(xElo, 50);

        $.jqplot(id, [data], {
            title: "Users rating destribution",
            captureRightClick: true,
            seriesDefaults: {
                renderer: $.jqplot.BarRenderer,
                rendererOptions: {
                    barWidth: 10,
                    barMargin: 1,
                    highlightMouseDown: true   
                },
                pointLabels: {
                    show: true
                }
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions: {
                        formatString:'%d',
                        angle: 90
                    },
                    ticks: xElo
                },
                yaxis: {
                    padMin: 0,
                    tickInterval: 1,
                    min: 0
                }
            }
        });
    }

    function onUpdateUsersRatingRequest(response)
    {
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }

        grid.update(response.data, {"users-rating-destribution" : updateUsersRating});
    }

    $.ajax({
        type: 'GET',
        url: "/statistics/getUsersByRating",
        contentType: 'application/json'
    }).done(onUpdateUsersRatingRequest);
})();

(function updateBlundersRatingChart() {
    function updateBlundersRating(id, data) {
        // Sorting data, beacuse server returns unsorted data
        // and jqplot doesn't work with unsorted data well
        data.sort();

        var xElo = data.map(function(el) {
            return el[0];
        });

        var yCount = data.map(function(el) {
            return el[1];
        });

        utils.normalizeTicks(xElo, 50);

        $.jqplot(id, [data], {
            title: "Blunders rating destribution",
            captureRightClick: true,
            seriesDefaults: {
                renderer: $.jqplot.BarRenderer,
                rendererOptions: {
                    barWidth: 10,
                    barMargin: 1,
                    highlightMouseDown: true   
                },
                pointLabels: {
                    show: true
                }
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions: {
                        formatString:'%d',
                        angle: 90
                    },
                    ticks: xElo
                },
                yaxis: {
                    padMin: 0,
                    tickInterval: 1
                }
            }
        });
    }

    function onUpdateBlundersRatingRequest(response) {
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }

        grid.update(response.data, {"blunders-rating-destribution" : updateBlundersRating});
    }

    $.ajax({
        type: 'GET',
        url: "/statistics/getBlundersByRating",
        contentType: 'application/json'
    }).done(onUpdateBlundersRatingRequest);
})();


(function updateBlunders() {
    function onUpdateBlundersRequest(response) {
        grid.update(response.data);
    }

    $.ajax({
        type: 'POST',
        url: "/statistics/getBlundersStatistics",
        contentType: 'application/json'
    }).done(onUpdateBlundersRequest);
})();

(function setupSpoilers() {
    grid.setupSpoiler('users-block');
    grid.setupSpoiler('top-block');
    grid.setupSpoiler('blunders-block');
    grid.setupSpoiler('online-block');
})();

