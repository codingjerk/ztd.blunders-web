(function generateStructure() {
    var blocks = [
        {
            caption: 'Blunders',
            rows: [
                {
                    type: 'wide', 
                    id: 'rating-statistic'
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
                    id: 'blunder-count-statistic'
                }
            ]
        }
    ];

    var html = grid.generate(blocks);
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
        url: "/api/user/blunders-count",
        contentType: 'application/json',
        data: JSON.stringify({
            username: $.url('?user')
        })
    }).done(onUpdateProfileRequest);
})();

(function updateRatingChart() {
    $.ajax({
        type: 'POST',
        url: "/api/user/rating-by-date",
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

        grid.update(response.data,  {'rating-statistic': drawRatingChart});
    } 

    function drawRatingChart(id, data) {
        if (data.length === 0) {
            utils.insertTooFewDataMessage(id, 'There will be your rating chart');

            return;
        }

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
        url: "/api/user/blunders-by-date",
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
        
        grid.update(response.data, {'blunder-count-statistic': drawBlunderChart});
    } 

    function drawBlunderChart(id, data) {
        if (data.total.length === 0) {
            utils.insertTooFewDataMessage(id, 'There will be your game history');

            return;
        }

        var failed = data.failed.mapIndex(0, utils.fixDate);
        var solved = data.solved.mapIndex(0, utils.fixDate);

	function sortDate(a, b) {
		return new Date(a[0]) - new Date(b[0]);
	}

	failed.sort(sortDate);
	solved.sort(sortDate);

        var firstDate = Math.min(
		failed[0][0] || (new Date()), 
		solved[0][0] || (new Date())
	);
        var lastDate = Math.max(
		failed[failed.length - 1][0] || 0, 
		solved[solved.length - 1][0] || 0
	);

        var oneHourInMs = 1000 * 60 * 60;

        var prevDate = new Date(firstDate - 23 * oneHourInMs);
        var nextDate = new Date(lastDate + 24 * oneHourInMs);

        failed.unshift([prevDate, 0]);
        failed.push([nextDate, 0]);

        solved.unshift([prevDate, 0]);
        solved.push([nextDate, 0]);

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
