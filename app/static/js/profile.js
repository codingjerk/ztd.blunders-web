var cosPoints = []; 
for (var i=0; i<50*Math.PI; i+=0.1){ 
    cosPoints.push([i, Math.cos(i)]); 
} 

(function() {
    function drawRatingChart(e) {
        $.jqplot(e.id, e.value, {  
            series: [{showMarker: false}],
            axes: {
                xaxis: {
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer
                },
                yaxis: {
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer
                }
            }
        });
    }

    blocks = [{
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
                additional: 'Last week'
            },
            {
                type: 'cell',
                label: 'Total',
                id: 'total-blunders-value',
                additional: 'Last week'
            },
            {
                type: 'cell',
                label: 'Solved',
                id: 'solved-blunders-value',
                additional: 'Last week'
            }
        ]
    }];

    var html = grid.generate(blocks);
    $('#details').html(html);

    ajaxDummy = [
        {
            id: 'rating-chart',
            value: [cosPoints]
        },
        {
            id: 'failed-blunders-value',
            value: 124
        },
        {
            id: 'total-blunders-value',
            value: 321
        },
        {
            id: 'solved-blunders-value',
            value: 321-124
        }
    ];

    function onRequest(data) {
        grid.update(data, {'rating-chart': drawRatingChart});
    }

    onRequest(ajaxDummy);
})();