
// ----------------------------------------------------------------------
// SENTIMENT OVER TIME SCATTER PLOT
// ----------------------------------------------------------------------
var plotSentimentChart = function(sentimentData){
  // var weekScores = JSON.parse(sentimentData[0].weekScores);
  // var eachScores = JSON.parse(sentimentData[0].individualScores);
  // console.table(weekScores);
  console.table(sentimentData);
  var svg = dimple.newSvg("#sentimentChart", "100%", 500);
  var sentimentChart = new dimple.chart(svg);
  var x = sentimentChart.addTimeAxis("x", "Date", "%d %b %Y", "%b  '%y");
  var y = sentimentChart.addMeasureAxis("y", "Score");
  y.tickFormat = ",.2f";

  var scoreSeries = sentimentChart.addSeries(null, dimple.plot.line);
  scoreSeries.data = sentimentData;
  // var pointSeries = sentimentChart.addSeries("Score", dimple.plot.bubble);
  // pointSeries.data = eachScores;

  // custom tooltips
  scoreSeries.getTooltipText = function (e) {
    return [
      'Polarity: ' + d3.format(",.3f")(e.yValue)
    ];
  };

  // Axis formatting.
  x.timePeriod = d3.time.months;
  x.timeInterval = 1;
  x.fontSize = 14;
  y.fontSize = 14;
  y.title = "Sentiment Polarity";

  sentimentChart.draw(1000);
  x.titleShape.remove();
  // Setting the tickFormat after the chart is drawn will only affect tooltips


}


// ----------------------------------------------------------------------
// COMMON LANGUAGES OVER TIME LINE CHART
// ----------------------------------------------------------------------
var plotTimeLangChart = function(timeLangData){
  var svg = dimple.newSvg("#timeLangChart", "100%", 500);
  var timeLangChart = new dimple.chart(svg, timeLangData);
  var x = timeLangChart.addTimeAxis("x", "occurred_at_week", "%d %b %Y", "%b  '%y");
  var y = timeLangChart.addMeasureAxis("y", "percentage");

  var mySeries = timeLangChart.addSeries("language", dimple.plot.line);


  // Toggle data points here
  mySeries.lineMarkers = false;

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
  x.timeInterval = 1;
  x.fontSize = 14;
  y.fontSize = 14;
  y.title = "Percentage of tweets";


  timeLangChart.defaultColors = [
    new dimple.color("#3498db", "#3498db", 1), // blue
    new dimple.color("#e74c3c", "#c0392b", 1), // red
    new dimple.color("#2ecc71", "#2ecc71", 1), // green
    new dimple.color("#9b59b6", "#9b59b6", 1), // purple
    new dimple.color("#e67e22", "#e67e22", 1), // orange
    new dimple.color("#f1c40f", "#f1c40f", 1), // yellow
    new dimple.color("#1abc9c", "#1abc9c", 1), // turquoise
    new dimple.color("#95a5a6", "#95a5a6", 1)  // gray
  ];

  timeLangChart.draw(1000);
  x.titleShape.remove();
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
  xAxis.fontSize = 14;
  yAxis.fontSize = 14;
  yAxis.title = '';

  // Draw without any axes
  xAxis.hidden = true;
  // yAxis.hidden = true;

  // Set small margins as there is going to be no axes displayed
  sourceChart.setMargins(150, 30, 20, 20);

  // Define a custom color palette.  These colours are based on the excellent
  // set at http://flatuicolors.com/
  sourceChart.defaultColors = [
    new dimple.color("#3498db", "#2980b9", 1), // blue
    new dimple.color("#e74c3c", "#c0392b", 1), // red
    new dimple.color("#2ecc71", "#27ae60", 1), // green
    new dimple.color("#9b59b6", "#8e44ad", 1), // purple
    new dimple.color("#e67e22", "#d35400", 1), // orange
    new dimple.color("#f1c40f", "#f39c12", 1), // yellow
    new dimple.color("#1abc9c", "#16a085", 1), // turquoise
    new dimple.color("#95a5a6", "#7f8c8d", 1)  // gray
  ];

  // Set some custom display elements for each series shape
  mySeries.afterDraw = function (s, d) {

    // I've defined the width in terms of the golden ratio as it seems like the sort
    // of thing a designer would do.
    var shape = d3.select(s),
    goldenRatio = 1.61803398875;

    // Add a rectangle to the bar giving a nice style.  The idea was borrowed
    // from sirocco's question here:
    // http://stackoverflow.com/questions/25044608/dimplejs-barchart-styling-columns
    svg.append("rect")
    .attr("x", shape.attr("x"))
    .attr("y", shape.attr("y"))
    .attr("height", (0.5 * shape.attr("height")) / goldenRatio)
    .attr("width", shape.attr("width"))
    .style("fill", shape.style("stroke"))
    .style("opacity", 1)
    .style("pointer-events", "none");

    // Draw without a border
    shape.attr("stroke", shape.attr("fill"));

    d3.selectAll("text")
    .filter(function(d){return typeof(d) == "string";})
    .style("cursor", "pointer")
    .each(function(d){
      $(this).attr("id", d).attr("class", "twitter-button").attr("data-toggle", "modal").attr("data-target", "#myModal");})
    .on("click",toggleTwitterContent);

    d3.selectAll("rect")
    .style("cursor", "pointer")
    .each(function(d){
      $(this).attr("id", String($(this).attr("id")).split("__")[0]).attr("class", "twitter-button").attr("data-toggle", "modal").attr("data-target", "#myModal");})
    .on("click",toggleTwitterContent);
  };
  // custom tooltips
  mySeries.getTooltipText = function (e) {
    return [
      Math.round(e.xValue * 100)/100 + ' %'
    ];
  };

  sourceChart.draw(1000);
};


// ----------------------------------------------------------------------
// FREQUENCY OF STRING MATCH OVER TIME LINE CHART
// ----------------------------------------------------------------------
var plotStringMatchChart =  function(stringMatchData){

  var svg = dimple.newSvg("#timeStringMatchChart", "100%", 500);
  var timeStringMatchChart = new dimple.chart(svg, stringMatchData);
  var x = timeStringMatchChart.addTimeAxis("x", "occurred_at_week", "%d %b %Y", "%b %y");
  var y = timeStringMatchChart.addMeasureAxis("y", "percentage");
  var mySeries = timeStringMatchChart.addSeries("string", dimple.plot.line);

  // Toggle data points here
  mySeries.lineMarkers = false;

  // Chart margins (l, t, r, b)
  timeStringMatchChart.setMargins(60, 30, 30, 30);

  // custom tooltips
  mySeries.getTooltipText = function (e) {
    return [
      e.aggField[0]
    ];
  };

  // Axis formatting.
  x.timePeriod = d3.time.months;
  x.timeInterval = 1;
  x.fontSize = 14;
  y.fontSize = 14;
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
//   // Override the standard tooltip behaviour
//     mySeries.addEventHandler("mouseover", function (e){
//
//       // Draw the text information in the top left corner
//       svg.selectAll(".dimple-hover-text")
//         .data([e.xValue, String(d3.format(",.f")(e.yValue)) + "%"])
//           .enter()
//           .append("text")
//           .attr("class", "dimple-hover-text")
//           .attr("x", chart._xPixels()  + chart._widthPixels() - 25)
//           .attr("y", function (d, i) { return chart._yPixels() + 20 + i * 25; })
//           .style("text-anchor", "end")
//           .style("font-size", "20px")
//           .style("fill", chart.getColor(e.xValue).fill)
//           .style("pointer-events", "none")
//           .text(function (d) { return d ; } );
//
//       // Put a coloured bar next to the text for no good reason
//       svg.append("rect")
//         .attr("class", "dimple-hover-text")
//         .attr("x", chart._xPixels() + chart._widthPixels() - 15)
//         .attr("y", chart._yPixels())
//         .attr("height", 60)
//         .attr("width", 10)
//         .style("fill", chart.getColor(e.xValue).fill)
//         .style("opacity", 1)
//         .style("pointer-events", "none");
//
//     });
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
