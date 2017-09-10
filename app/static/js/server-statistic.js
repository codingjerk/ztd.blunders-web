(function generateStructure() {
    var blocks = [
        {
            id: 'users-block',
            caption: 'Users',
            rows: [
                {
                    type: 'wide',
                    id: 'users-rating-distribution'
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
            id: 'top-block-by-rating',
            caption: 'Top users by rating',
            rows: [
                {
                    type: 'wide',
                    id: 'users-top-by-rating'
                }
            ]
        },
        {
            id: 'top-block-by-activity',
            caption: 'Top active users',
            rows: [
                {
                    type: 'wide',
                    id: 'users-top-by-activity'
                }
            ]
        },
        {
            id: 'blunders-block',
            caption: 'Blunders',
            rows: [
                {
                    type: 'wide',
                    id: 'blunders-rating-distribution'
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

(function updateUsersCount() {
    $.ajax({
        type: 'POST',
        url: "/api/global/users-count",
        contentType: 'application/json'
    }).done(function(response) {
        grid.update(response.data);
    });
})();

(function updateUsersTop() {
    function drawUsersTopByRating(id, users) {
        var usersList = users.map(function(user) {
            var username = user.username;
            var elo = user.elo;
            return '<tr><td><a href="/profile?user={0}">{1}</a></td><td class="table-center-cell">{2}</td></tr>'.format(username, username, elo);
        }).join('');

        var header = '<tr> <td><b>Username</b></td> <td class="table-center-cell"><b>Elo</b></td> </tr>'

        var content = '<table>{0}{1}</table>'.format(header, usersList);
        $('#' + id).html(content);
    }

    function drawUsersTopByActivity(id, users) {
        var usersList = users.map(function(user) {
            var username = user.username;
            var totalTries = user.totalTries;
            var successRate = Math.round(100.0*(user.successTries/user.totalTries));
            return '<tr><td><a href="/profile?user={0}">{1}</a></td><td class="table-center-cell">{2}</td><td class="table-center-cell">{3}%</td></tr>'.format(username, username, totalTries, successRate);
        }).join('');

        var header = '<tr> <td><b>Username</b></td> <td class="table-center-cell"><b>Last week</b></td> <td class="table-center-cell"><b>Success rate</b></td> </tr>'

        var content = '<table>{0}{1}</table>'.format(header, usersList);
        $('#' + id).html(content);
    }

    $.ajax({
        type: 'POST',
        url: "/api/global/users-top",
        contentType: 'application/json'
    }).done(function(response) {
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }

        grid.update(response.data, {"users-top-by-rating": drawUsersTopByRating, "users-top-by-activity": drawUsersTopByActivity});
    });
})();

(function updateUsersOnline() {
    function drawUsersOnlineList(id, users) {
        var usersLinks = users.map(function(user) {
            return '<a href="/profile?user={0}">{1}</a> '.format(user,user);
        }).join('');

        $('#' + id).html(usersLinks);
    }

    $.ajax({
        type: 'POST',
        url: "/api/global/users-online",
        contentType: 'application/json'
    }).done(function(response) {
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }

        grid.update(response.data, {"users-online-list": drawUsersOnlineList});
    });
})();

(function updateUsersRatingChart() {
    function updateUsersRating(id, data){
        data.sort();

        var xElo = data.map(function(el){return el[0];});
        var yCount = data.map(function(el){return el[1];});

        utils.normalizeTicks(xElo, 50);

        $.jqplot(id, [data], {
            title: "Users rating distribution",
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

        grid.update(response.data, {"users-rating-distribution" : updateUsersRating});
    }

    $.ajax({
        type: 'POST',
        url: "/api/global/users-by-rating",
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
            title: "Blunders rating distribution",
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

        grid.update(response.data, {"blunders-rating-distribution" : updateBlundersRating});
    }

    $.ajax({
        type: 'POST',
        url: "/api/global/blunders-by-rating",
        contentType: 'application/json'
    }).done(onUpdateBlundersRatingRequest);
})();


(function updateBlundersCount() {
    function onUpdateBlundersRequest(response) {
        grid.update(response.data);
    }

    $.ajax({
        type: 'POST',
        url: "/api/global/blunders-count",
        contentType: 'application/json'
    }).done(onUpdateBlundersRequest);
})();

(function setupSpoilers() {
    grid.setupSpoiler('users-block');
    grid.setupSpoiler('top-block-by-rating');
    grid.setupSpoiler('top-block-by-activity');
    grid.setupSpoiler('blunders-block');
    grid.setupSpoiler('online-block');
})();
