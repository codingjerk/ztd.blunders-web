var cosPoints = []; 
for (var i=0; i<2*Math.PI; i+=0.1){ 
    cosPoints.push([i, Math.cos(i)]); 
} 

$('#temp-block').css('width', '100%');
$('#temp-block').css('height', '200px');
$('#temp-block2').css('width', '100%');
$('#temp-block2').css('height', '200px');

var plot2 = $.jqplot('temp-block', [cosPoints], {  
      series:[{showMarker:false}],
      axes:{
        xaxis:{
          labelRenderer: $.jqplot.CanvasAxisLabelRenderer
        },
        yaxis:{
          labelRenderer: $.jqplot.CanvasAxisLabelRenderer
        }
      }
  });

var plot2 = $.jqplot('temp-block2', [cosPoints], {  
      series:[{showMarker:false}],
      axes:{
        xaxis:{
          labelRenderer: $.jqplot.CanvasAxisLabelRenderer
        },
        yaxis:{
          labelRenderer: $.jqplot.CanvasAxisLabelRenderer
        }
      }
  });

(function() {
    
})();