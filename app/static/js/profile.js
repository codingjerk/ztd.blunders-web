var cosPoints = []; 
for (var i=0; i<50*Math.PI; i+=0.1){ 
    cosPoints.push([i, Math.cos(i)]); 
} 

(function() {

    function fixDate(data)
    {
        for (var i = 0; i < data.length; ++i) {
            data[i][0] = new Date(data[i][0])
        }

        return data
    }

    function drawRatingChart(e) {
        chart = fixDate(e.value[0].value)

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

    function drawBlunderChart(e) {
          data = [
                    fixDate(e.value[1].value),
                    fixDate(e.value[2].value)
                 ]
          plot3 = $.jqplot(e.id, data, {
            // Tell the plot to stack the bars.
            stackSeries: true,
            captureRightClick: true,
            seriesDefaults:{
              renderer:$.jqplot.BarRenderer,
              rendererOptions: {
                  // Put a 30 pixel margin between bars.
                  barMargin: 1,
                  // Highlight bars when mouse button pressed.
                  // Disables default highlighting on mouse over.
                  highlightMouseDown: true   
              },
              pointLabels: {show: true}
            },
            axes: {
              xaxis: {
                  renderer: $.jqplot.DateAxisRenderer,
                  autoscale:true 
              },
              yaxis: {
                // Don't pad out the bottom of the data range.  By default,
                // axes scaled as if data extended 10% above and below the
                // actual range to prevent data points right on grid boundaries.
                // Don't want to do that here.
                padMin: 0
              }
            },
            legend: {
              show: true,
              location: 'e',
              placement: 'outside'
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

        function onUpdateRatingChartRequest(response) {
            if (response.status !== 'ok') {
                // TODO: notify
                return;
            }

            grid.update(response.data,  {'rating-statistics': drawRatingChart});
        } 

        function onUpdateBlunderChartRequest(response) {
            if (response.status !== 'ok') {
                // TODO: notify
                return;
            }

            grid.update(response.data,  {'blunder-count-statistics': drawBlunderChart});
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

        $.ajax({
            type: 'POST',
            url: "/statistics/getBlundersByDate",
            contentType: 'application/json',
            data: JSON.stringify({
                username: $.url('?user'),
            })
        }).done(onUpdateBlunderChartRequest);
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
            {
                type: 'chart', 
                id: 'blunder-count-statistics'
            },
        ]
    }];

    var html = grid.generate(blocks);
    $('#details').html(html);

    updateProfile();

})();