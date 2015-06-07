(function generateStructure() {
    var blocks = [{
        caption: 'Blunders',
        rows: [
            {
                type: 'chart', 
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
                type: 'chart', 
                id: 'blunder-count-statistics'
            }
        ]
    }];

    var html = grid.generate(blocks);
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
        var chart = data.mapNear(0, utils.fixDate);
        
        $.jqplot(id, [data], {
            series: [{
                showMarker: false,
                rendererOptions: {
                    smooth: true
                }
            }],
            axes: {
                xaxis: {
                    renderer: $.jqplot.DateAxisRenderer
                }
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
        var failed = data.failed.mapNear(0, utils.fixDate);
        var solved = data.solved.mapNear(0, utils.fixDate);

        $.jqplot(id, [failed, solved], {
            stackSeries: true,
            captureRightClick: true,
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
                    autoscale: true 
                },
                yaxis: {
                    padMin: 0
                }
            },
            legend: {
                show: true,
                location: 'e',
                placement: 'inside'
            }
        });
    }
})();