var figures = {{figuresJSON | safe}};
  var ids = {{ids | safe}};
  for(var i in figures) {
      Plotly.plot(ids[i],
          figures[i].data,
          figures[i].layout || {});
  }
