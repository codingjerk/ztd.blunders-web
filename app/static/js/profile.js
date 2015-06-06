var cosPoints = []; 
for (var i=0; i<50*Math.PI; i+=0.1){ 
    cosPoints.push([i, Math.cos(i)]); 
} 

(function() {
    function drawRatingChart(e) {
        var chart = e.value[0];
        for (var i = 0; i < chart.length; ++i) {
            var point = chart[i];

            chart[i] = [new Date(point[0]), point[1]];
        }

        console.log(chart);

        $.jqplot(e.id, [chart], {
            series: [{showMarker: false}],
            axes: {
                xaxis: {
                    renderer: $.jqplot.DateAxisRenderer 
                }
            }
        });
    }

    var blocks = [{
        caption: 'Blunders',
        rows: [
            {
                type: 'chart', 
                id: 'rating-chart'
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
            }
        ]
    }];

    var html = grid.generate(blocks);
    $('#details').html(html);

    function onRequest(response) {
        if (response.status !== 'ok') {
            // TODO: notify
            return;
        }

        grid.update(response.data, {'rating-chart': drawRatingChart});
    }

    $.ajax({
        type: 'POST',
        url: "/getUserProfile",
        contentType: 'application/json',
        data: JSON.stringify({
            username: $.url('?user'),
        })
    }).done(onRequest);

})();