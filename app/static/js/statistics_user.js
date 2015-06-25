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
        url: "/statistics/getBlundersStatistics",
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
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }

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
                    renderer: $.jqplot.DateAxisRenderer
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
        if (response.status !== 'ok') {
            notify.error(response.message);
            return;
        }
        
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
                    renderer: $.jqplot.DateAxisRenderer,
                    tickInterval: 'day'
                },
                yaxis: {
                    padMin: 0,
                    min: 0
                }
            },
            legend: {
                show: true,
                renderer: $.jqplot.EnhancedLegendRenderer,
                location: 'n',
                placement: "outsideGrid",
                marginTop: "0px",
                rendererOptions: {
                    numberRows: 1
                },
                labels: ['Failed to solve', 'Successfully solved']
            }
        });
    }
})();
