TESTER = document.getElementById('tester');
Plotly.newPlot( TESTER, [{
  x: [1, 2, 3, 4, 5],
  y: [1, 2, 4, 8, 16] }], {
    margin: { t: 0 } } );


var data = [{
      values: [0.5, 0.5],
      labels: ['FG Percent'],
      domain: {column: 0},
      name: 'Field Goal Percentage',
      hoverinfo: 'label+percent+name',
      hole: .4,
      type: 'pie'
    }];

var layout = {
      title: 'Field Goal Percentage',
      annotations: [
        {
          font: {
            size: 20
          },
          showarrow: false,
          text: 'GHG',
          x: 0.17,
          y: 0.5
        },
      ],
      height: 400,
      width: 400,
      showlegend: false,
      grid: {rows: 1, columns: 2}
    };

Plotly.newPlot('myDiv', data, layout);
