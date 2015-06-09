(function generateStructure() {
    var blocks = [
        {
            caption: 'Blunders',
            rows: [
                {
                    type: 'wide', 
                    id: 'rating-statistics'
                },
                {
                    type: 'cell',
                    label: 'Failed',
                    id: 'failed-blunders-value',
                    additional: 'all time'
                },
                {
                    type: 'cell',
                    label: 'Total',
                    id: 'total-blunders-value',
                    additional: 'all time'
                },
                {
                    type: 'cell',
                    label: 'Solved',
                    id: 'solved-blunders-value',
                    additional: 'all time'
                },
                {
                    type: 'wide', 
                    id: 'blunder-count-statistics'
                }
            ]
        },
        {
            caption: 'History',
            rows: [
                {
                    type: 'wide', 
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
            // TODO: notify
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

(function updateRatingChart() {
    $.ajax({
        type: 'POST',
        url: "/statistics/getRatingByDate",
        contentType: 'application/json',
        data: JSON.stringify({
            username: $.url('?user')
        })
    }).done(onUpdateRatingChartRequest);

    function onUpdateRatingChartRequest(response) {
        if (response.status !== 'ok') return; // TODO: notify
        grid.update(response.data,  {'rating-statistics': drawRatingChart});
    } 

    function drawRatingChart(id, data) {
        var chart = data.mapIndex(0, utils.fixDate);
        
        $.jqplot(id, [data], {
            title: "User rating dynamics",
            series: [{
                showMarker: false,
                rendererOptions: {
                    smooth: true
                }
            }],
            axes: {
                xaxis: {
                    renderer: $.jqplot.DateAxisRenderer,
                    tickInterval: 'day'
                }
            },
            cursor:{ 
                show: true,
                zoom:true, 
                showTooltip:false,
                clickReset:true
            } 
        });
    }
})();

(function updateBlunderChart() {
    $.ajax({
        type: 'POST',
        url: "/statistics/getBlundersByDate",
        contentType: 'application/json',
        data: JSON.stringify({
            username: $.url('?user')
        })
    }).done(onUpdateBlunderChartRequest);

    function onUpdateBlunderChartRequest(response) {
        if (response.status !== 'ok') return; // TODO: notify
        grid.update(response.data, {'blunder-count-statistics': drawBlunderChart});
    } 

    function drawBlunderChart(id, data) {
        var failed = data.failed.mapIndex(0, utils.fixDate);
        var solved = data.solved.mapIndex(0, utils.fixDate);

        $.jqplot(id, [failed, solved], {
            title: "Blunder success / failed dynamics",
            stackSeries: true,
            captureRightClick: true,
            seriesColors: ["rgb(217, 83, 79)", "#1fa67a"],
            seriesDefaults: {
                renderer: $.jqplot.BarRenderer,
                rendererOptions: {
                    barMargin: 1,
                    highlightMouseDown: true   
                },
                pointLabels: {
                    show: true
                }
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.DateAxisRenderer,
                    tickInterval: 'day'
                },
                yaxis: {
                    padMin: 0
                }
            },
            legend:{ 
                show:true,
                    renderer: $.jqplot.EnhancedLegendRenderer,
                    location: 'n' ,
                    placement : "outsideGrid",
                    marginTop : "0px",
                    rendererOptions: {
                        numberRows: 1
                    },
                    labels: [ 'Failed to solve', 'Successfully solved']
            },
        });
    }
})();

(function updateBlunderHistory() {
    var blundersPerPage = 10;

    var content = '<div id="blunder-history-content"></div><div id="blunder-history-paginator"></div>';
    $("#blunder-history").html(content);

    $("#blunder-history-paginator").pagination({
        items: 1,
        itemsOnPage: blundersPerPage,
        cssStyle: 'light-theme',
        onPageClick: function(pageNumber, event) {
            getContent(pageNumber, blundersPerPage);
        }
    });

    getContent(1, blundersPerPage);

    function getContent(page, limit) {
        $.ajax({
            type: 'POST',
            url: "/statistics/getBlundersHistory",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $.url('?user'),
                offset: (page - 1) * limit,
                limit: limit
            })
        }).done(onUpdateBlunderHistory);
    }

    function onUpdateBlunderHistory(response) {
        var blunders = response.data.blunders;

        var rows = utils.map(blunders, function(b) {
            return '<tr><td>{0}</td><td>{1}</td></tr>'.format(b.blunder_id, b.result);
        }).join('');

        var content = '<table>{0}</table>'.format(rows);
        $("#blunder-history-content").html(content);

        $("#blunder-history-paginator").pagination("updateItems", response.data.total);
    }
})();