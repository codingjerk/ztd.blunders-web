(function generateStructure() {
    var blocks = [
        {
            caption: 'Users',
            rows: [
                {
                    type: 'wide', 
                    id: 'user-rating-destribution'
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
                    label: 'Active today',
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
                    id: 'blunder-rating-destribution'
                },
                {
                    type: 'cell',
                    label: 'Total',
                    id: 'total-blunders-value',
                    additional: 'blunders'
                },
                {
                    type: 'cell',
                    label: 'Never seen',
                    id: 'neverseen-blunders-value',
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

        console.log(users)
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

        grid.update(response.data, {"user-rating-destribution" : updateUsersRating});
    }

    $.ajax({
        type: 'GET',
        url: "/statistics/getUsersByRating",
        contentType: 'application/json',
    }).done(onUpdateUsersRatingRequest);
})();