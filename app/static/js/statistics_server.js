(function generateStructure() {
    var blocks = [
        {
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
                },
                {
                    type: 'wide', 
                    id: 'users-online-list'
                }
            ]
        },
        {
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
        }
    ];

    var html = grid.generate(blocks, 3);
    $('#details').html(html);
})();

(function updateUsers() {

    function updateUserList(id, users) {
        var usersLinks = users.map(function(user) {
            return '<a href="/profile?user={0}">{1}</a> '.format(user,user);
        }).join('');

        $('#' + id).html(usersLinks);
    }

    function onUpdateUsersRequest(response) {
        if (response.status !== 'ok') {
            // TODO: notify
            return;
        }

        grid.update(response.data, {"users-online-list" : updateUserList});
    }

    $.ajax({
        type: 'GET',
        url: "/statistics/getUsersStatistics",
        contentType: 'application/json'
    }).done(onUpdateUsersRequest);
})();

(function updateUsersRatingChart() {

    function updateUsersRating(id, data){
       data.unshift([1000, 0]) // Hack to scale x axis
       data.push([2500,0]);

       var xElo = data.map(function(el){return el[0];});
       var yCount = data.map(function(el){return el[1];});

       $.jqplot(id, [data], {
            title: "Users rating destribution",
            captureRightClick: true,
            seriesDefaults: {
                renderer: $.jqplot.BarRenderer,
                rendererOptions: {
                    barWidth: 20,
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
                      // labelPosition: 'middle',
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

    function onUpdateUsersRatingRequest(response)
    {
        if (response.status !== 'ok') {
            // TODO: notify
            return;
        }

        grid.update(response.data, {"users-rating-destribution" : updateUsersRating});
    }

    $.ajax({
        type: 'GET',
        url: "/statistics/getUsersByRating",
        contentType: 'application/json',
    }).done(onUpdateUsersRatingRequest);
})();

(function updateBlundersRatingChart() {

    function updateBlundersRating(id, data){
       data.unshift([1000, 0]) // Hack to scale x axis
       data.push([3000,0]);

       var xElo = data.map(function(el){return el[0];});
       var yCount = data.map(function(el){return el[1];});

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
                      // labelPosition: 'middle',
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

    function onUpdateBlundersRatingRequest(response)
    {
        if (response.status !== 'ok') {
            // TODO: notify
            return;
        }

        grid.update(response.data, {"blunders-rating-destribution" : updateBlundersRating});
    }

    $.ajax({
        type: 'GET',
        url: "/statistics/getBlundersByRating",
        contentType: 'application/json',
    }).done(onUpdateBlundersRatingRequest);
})();


(function updateBlunders() {
    function onUpdateBlundersRequest(response) {
        grid.update(response.data);
    }

    $.ajax({
        type: 'GET',
        url: "/statistics/getBlundersStatistics",
        contentType: 'application/json',
    }).done(onUpdateBlundersRequest);
})();