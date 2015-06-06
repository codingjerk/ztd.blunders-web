var cosPoints = []; 
for (var i=0; i<50*Math.PI; i+=0.1){ 
    cosPoints.push([i, Math.cos(i)]); 
} 

(function() {

    function drawRatingChart(e) {
        chart = e.value[0].value

        for (var i = 0; i < chart.length; ++i) {
            chart[i][0] = new Date(chart[i][0])
        }

        $.jqplot(e.id, [chart], {
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

    function updateProfile()
    {
        function onUpdateProfileRequest(response) {
            if (response.status !== 'ok') {
                // TODO: notify
                return;
            }

            grid.update(response.data, {});
        }

        function onUpdateRatingChartRequest(response) {
            if (response.status !== 'ok') {
                // TODO: notify
                return;
            }

            grid.update(response.data,  {'rating-statistics': drawRatingChart});
        }

        $.ajax({
            type: 'POST',
            url: "/getUserProfile",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $.url('?user'),
            })
        }).done(onUpdateProfileRequest);

        $.ajax({
            type: 'POST',
            url: "/statistics/getRatingByDate",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $.url('?user'),
            })
        }).done(onUpdateRatingChartRequest);
    }

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
        ]
    }];

    var html = grid.generate(blocks);
    $('#details').html(html);

    updateProfile();

})();