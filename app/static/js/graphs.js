
// ----------------------------------------------------------------------
// SENTIMENT OVER TIME LINE PLOT
// ----------------------------------------------------------------------
var plotSentimentChart = function(sentimentData){

  var svg = dimple.newSvg("#sentimentChart", "100%", 500);
  var sentimentChart = new dimple.chart(svg);
  var x = sentimentChart.addTimeAxis("x", "Date", "%b %Y", "%b '%y");
  var y = sentimentChart.addMeasureAxis("y", "Score");
  y.tickFormat = ",.2f";

  var scoreSeries = sentimentChart.addSeries(null, dimple.plot.line);
  scoreSeries.data = sentimentData;
  scoreSeries.lineWeight = 4;

  // custom tooltips
  scoreSeries.getTooltipText = function (e) {
    console.log(e);
    return [
      'Sentiment score: ' + d3.format(",.3f")(e.yValue),
      'Date: ' + d3.time.format("%d %B '%y")(e.x)
    ];
  };

  sentimentChart.defaultColors = [
    new dimple.color("#3A5B8A", "#3A5B8A", 1), // Turquoise
    new dimple.color("#779F90", "#779F90", 1), // Blue
    new dimple.color("#BDDADA", "#BDDADA", 1), // Light blue
    new dimple.color("#FDE972", "#FDE972", 1), // Yellow
    new dimple.color("#B6B771", "#B6B771", 1) // Green
  ];

  // Axis formatting.
  x.timePeriod = d3.time.months;
  x.timeInterval = 3;
  x.fontSize = 16;
  y.fontSize = 16;
  y.ticks = 5;
  y.title = "Sentiment Polarity";

  onViewport("#sentimentChart", "active", 600, function(el) {
    sentimentChart.draw(1000);
    x.titleShape.remove();
  });

}


// ----------------------------------------------------------------------
// COMMON LANGUAGES OVER TIME LINE CHART
// ----------------------------------------------------------------------
var plotTimeLangChart = function(timeLangData){
  var svg = dimple.newSvg("#timeLangChart", "100%", 500);
  var timeLangChart = new dimple.chart(svg, timeLangData);
  var x = timeLangChart.addTimeAxis("x", "occurred_at_month", "%b %Y", "%b  '%y");
  var y = timeLangChart.addMeasureAxis("y", "percentage");

  var mySeries = timeLangChart.addSeries("language", dimple.plot.line);
  var legend = timeLangChart.addLegend(60, 10, 500, 20, "right");
  legend.fontSize = 12;

  // Toggle data points here
  mySeries.lineMarkers = false;
  mySeries.lineWeight = 4;

  // Chart margins (l, t, r, b)
  timeLangChart.setMargins(60, 30, 30, 30);

  // custom tooltips
  mySeries.getTooltipText = function (e) {
    return [
      e.aggField
    ];
  };

  // Axis formatting.
  x.timePeriod = d3.time.months;
  x.timeInterval = 3;
  x.fontSize = 16;
  y.fontSize = 16;
  y.ticks = 5;
  y.title = "Percentage of tweets";

  timeLangChart.defaultColors = [
    new dimple.color("#3A5B8A", "#3A5B8A", 1), // Turquoise
    new dimple.color("#779F90", "#779F90", 1), // Blue
    new dimple.color("#BDDADA", "#BDDADA", 1), // Light blue
    new dimple.color("#FDE972", "#FDE972", 1), // Yellow
    new dimple.color("#B6B771", "#B6B771", 1) // Green
  ];

  onViewport("#timeLangChart", "active", 600, function(el) {
    timeLangChart.draw(1000);
    x.titleShape.remove();
  });
};

// ----------------------------------------------------------------------
// SOURCE BAR CHART
// ----------------------------------------------------------------------

var plotSourceChart =  function(sourceData){

  // standard dimple svg definition for a responsive chart
  var svg = dimple.newSvg("#sourceBarChart", '100%', 500);

  // for customClassList see http://dimplejs.org/advanced_examples_viewer.html?id=advanced_bars_sketchy
  var sourceChart = new dimple.chart(svg, sourceData);
  var xAxis = sourceChart.addMeasureAxis("x", "percentage");
  var yAxis = sourceChart.addCategoryAxis("y", "source");
  yAxis.addOrderRule("percentage");
  var mySeries = sourceChart.addSeries("source", dimple.plot.bar);
  xAxis.fontSize = 16;
  yAxis.fontSize = 16;
  xAxis.ticks = 5;
  yAxis.title = '';
  xAxis.title = 'Percentage of Tweets Sampled'

  // Draw without any axes
  // xAxis.hidden = true;
  // yAxis.hidden = true;

  // Set small margins as there is going to be no axes displayed
  sourceChart.setMargins(150, 30, 20, 50);

  sourceChart.defaultColors = [
    new dimple.color("#3A5B8A", "#3A5B8A", 1) // Blue
  ];

  // Set some custom display elements for each series shape
  mySeries.afterDraw = function (s, d) {
    // TODO make this more efficient. Currently afterDraw function loops through each data point
    // and then I do the same again with d3.selectAll

    // toggle Twitter content when clicking on twitter handles
    d3.selectAll("text")
    .filter(function(d){return typeof(d) == "string";})
    .style("cursor", "pointer")
    .each(function(d){
      $(this).attr("id", d).attr("class", "twitter-button").attr("data-toggle", "modal").attr("data-target", "#myModal");})
    .on("click",toggleTwitterContent);

    d3.selectAll("rect")
    .style("cursor", "pointer")
    .on('mouseover', function(d){
    var nodeSelection = d3.select(this).style({opacity:'0.8'});
    })
    .on('mouseout', function(d){
    var nodeSelection = d3.select(this).style({opacity:'1'});
    })
    .each(function(d){
      $(this).attr("id", String($(this).attr("id")).split("__")[0]).attr("class", "twitter-button").attr("data-toggle", "modal").attr("data-target", "#myModal");})
    .on("click",toggleTwitterContent);
  };

  onViewport("#sourceBarChart", "active", 600, function(el) {
    sourceChart.draw(1000);
  });
};


// ----------------------------------------------------------------------
// FREQUENCY OF STRING MATCH OVER TIME LINE CHART
// ----------------------------------------------------------------------
var plotStringMatchChart =  function(stringMatchData){

  console.log(stringMatchData);
  var svg = dimple.newSvg("#timeStringMatchChart", "100%", 500);
  var timeStringMatchChart = new dimple.chart(svg, stringMatchData);
  var x = timeStringMatchChart.addTimeAxis("x", "date", "%Y-%m-%d", "%b %y");
  var y = timeStringMatchChart.addMeasureAxis("y", "count");
  var mySeries = timeStringMatchChart.addSeries("word", dimple.plot.line);

  // Toggle data points here
  mySeries.lineMarkers = false;
  mySeries.lineWeight = 4;

  // Chart margins (l, t, r, b)
  timeStringMatchChart.setMargins(60, 30, 30, 30);

  // custom tooltips
  mySeries.getTooltipText = function (e) {
    return [
      e.aggField[0].charAt(0).toUpperCase() + e.aggField[0].slice(1)
    ];
  };

  timeStringMatchChart.defaultColors = [
    new dimple.color("#3A5B8A", "#3A5B8A", 1), // Turquoise
    new dimple.color("#779F90", "#779F90", 1), // Blue
    new dimple.color("#BDDADA", "#BDDADA", 1), // Light blue
    new dimple.color("#FDE972", "#FDE972", 1), // Yellow
    new dimple.color("#B6B771", "#B6B771", 1) // Green
  ];

  // Axis formatting.
  x.timePeriod = d3.time.months;
  x.timeInterval = 3;
  x.fontSize = 16;
  y.fontSize = 16;
  y.ticks = 5;
  y.title = "Percentage of tweets";

  //Create Y axis label
// svg.append("text")
//     .attr("transform", "rotate(-90)")
//     .attr("y", 0-margin.left)
//     .attr("x",0 - (h / 2))
//     .attr("dy", "1em")
//     .style("text-anchor", "middle")
//     .text("Revenue");

  timeStringMatchChart.draw(1000);
  x.titleShape.remove();
  return timeStringMatchChart;

};

// ----------------------------------------------------------------------
// PROMINENCE OF PROLIFIC TWEETERS OVER TIME
// ----------------------------------------------------------------------
var plotPopularTweeterChart = function(popularTweeterData){
  var svg = dimple.newSvg("#popularTweeterChart", "100%", 500);
  var popularTweeterChart = new dimple.chart(svg, popularTweeterData);
  var x = popularTweeterChart.addTimeAxis("x", "occurred_at_month", "%b %Y", "%b '%y");
  var y = popularTweeterChart.addMeasureAxis("y", "count");
  var s = popularTweeterChart.addSeries("source_user_screen_name", dimple.plot.line);

  var legend = popularTweeterChart.addLegend(60, 10, 500, 20, "right");
  legend.fontSize = 12;

  // Chart margins (l, t, r, b)
  popularTweeterChart.setMargins(60, 60, 30, 30);

  popularTweeterChart.defaultColors = [
    new dimple.color("#3A5B8A", "#3A5B8A", 1), // Blue
    new dimple.color("#779F90", "#779F90", 1), // Turquoise
    new dimple.color("#BDDADA", "#BDDADA", 1), // Light blue
    new dimple.color("#FDE972", "#FDE972", 1), // Yellow
    new dimple.color("#B6B771", "#B6B771", 1) // Green
  ];

  // custom tooltips
  s.getTooltipText = function (e) {
    return [
      'Source: ' + e.aggField,
      'Share count: ' + (e.yValue),
      'Month: ' + d3.time.format("%B '%y")(e.x)
    ];
  };
  s.lineWeight = 4;
  // s.interpolation = "cardinal";

  // Axis formatting.
  x.timePeriod = d3.time.months;
  x.timeInterval = 3;
  x.fontSize = 16;
  y.fontSize = 16;
  y.ticks = 5;
  y.title = "Number of tweets & retweets";

  onViewport("#popularTweeterChart", "active", 600, function(el) {
    popularTweeterChart.draw(1000);
    x.titleShape.remove();
  });

}



// ----------------------------------------------------------------------
// LANGUAGE BAR CHART
// ----------------------------------------------------------------------

// // standard dimple svg definition for a responsive chart
// var svg = dimple.newSvg("#discreteBarChart", "100%", 500);
// var data = {{ langData | safe }}
//
// // for customClassList see http://dimplejs.org/advanced_examples_viewer.html?id=advanced_bars_sketchy
// var chart = new dimple.chart(svg, data);
// var xAxis = chart.addCategoryAxis("x", "language");
// var yAxis = chart.addMeasureAxis("y", "percentage");
// var mySeries = chart.addSeries("language", dimple.plot.bar);
// xAxis.fontSize = 14;
// yAxis.fontSize = 14;
//
//   // Draw without any axes
//   // xAxis.hidden = true;
//   yAxis.hidden = true;
//
//   // Set small margins as there is going to be no axes displayed
//   chart.setMargins(50, 50, 50, 80);
//
//   // Define a custom color palette.  These colours are based on the excellent
//   // set at http://flatuicolors.com/
//   chart.defaultColors = [
//       new dimple.color("#3498db", "#2980b9", 1), // blue
//       new dimple.color("#e74c3c", "#c0392b", 1), // red
//       new dimple.color("#2ecc71", "#27ae60", 1), // green
//       new dimple.color("#9b59b6", "#8e44ad", 1), // purple
//       new dimple.color("#e67e22", "#d35400", 1), // orange
//       new dimple.color("#f1c40f", "#f39c12", 1), // yellow
//       new dimple.color("#1abc9c", "#16a085", 1), // turquoise
//       new dimple.color("#95a5a6", "#7f8c8d", 1)  // gray
//   ];
//
//   // Set some custom display elements for each series shape
//   mySeries.afterDraw = function (s, d) {
//
//     // I've defined the width in terms of the golden ratio as it seems like the sort
//     // of thing a designer would do.
//     var shape = d3.select(s),
//         goldenRatio = 1.61803398875;
//
//     // Add a rectangle to the bar giving a nice style.  The idea was borrowed
//     // from sirocco's question here:
//     // http://stackoverflow.com/questions/25044608/dimplejs-barchart-styling-columns
//     svg.append("rect")
//       .attr("x", shape.attr("x"))
//       .attr("y", shape.attr("y"))
//       .attr("height", shape.attr("height"))
//       .attr("width", (0.5 * shape.attr("width")) / goldenRatio)
//       .style("fill", shape.style("stroke"))
//       .style("opacity", 1)
//       .style("pointer-events", "none");
//
//     // Draw without a border
//     shape.attr("stroke", shape.attr("fill"));
//
//   };
//
// // Override the standard tooltip behaviour
//   mySeries.addEventHandler("mouseover", function (e){
//
//     // Draw the text information in the top left corner
//     svg.selectAll(".dimple-hover-text")
//       .data([e.xValue, String(d3.format(",.f")(e.yValue)) + "%"])
//         .enter()
//         .append("text")
//         .attr("class", "dimple-hover-text")
//         .attr("x", chart._xPixels()  + chart._widthPixels() - 25)
//         .attr("y", function (d, i) { return chart._yPixels() + 20 + i * 25; })
//         .style("text-anchor", "end")
//         .style("font-size", "20px")
//         .style("fill", chart.getColor(e.xValue).fill)
//         .style("pointer-events", "none")
//         .text(function (d) { return d ; } );
//
//     // Put a coloured bar next to the text for no good reason
//     svg.append("rect")
//       .attr("class", "dimple-hover-text")
//       .attr("x", chart._xPixels() + chart._widthPixels() - 15)
//       .attr("y", chart._yPixels())
//       .attr("height", 60)
//       .attr("width", 10)
//       .style("fill", chart.getColor(e.xValue).fill)
//       .style("opacity", 1)
//       .style("pointer-events", "none");
//
//   });
//
//     // Clear the text on exit
//     mySeries.addEventHandler("mouseleave", function (e) {
//       svg.selectAll(".dimple-hover-text").remove();
//     });
//
// chart.draw(1000);

// Add a method to draw the chart on resize of the window - currently not
// working with the custom bar chart styling
// window.onresize = function () {
//     // As of 1.1.0 the second parameter here allows you to draw
//     // without reprocessing data.  This saves a lot on performance
//     // when you know the data won't have changed.
//     chart.draw(0, true);
// };


var sourceChart = plotSourceChart(sourceData);
var timeLangChart = plotTimeLangChart(timeLangData);
var sentimentChart = plotSentimentChart(sentimentData);
plotPopularTweeterChart(popularTweeterData);
