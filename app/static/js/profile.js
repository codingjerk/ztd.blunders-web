var cosPoints = []; 
for (var i=0; i<50*Math.PI; i+=0.1){ 
    cosPoints.push([i, Math.cos(i)]); 
} 

(function() {
    function drawChart(id, data) {
        $.jqplot(id, data, {  
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
        for (var i = 0; i < data.length; i++) {
            var element = data[i];

            if (element.id === 'rating-chart') {
                drawChart('rating-chart', element.value);
            } else {
                $('#' + element.id).html(element.value);
            }
        }
    }

    onRequest(ajaxDummy);
})();