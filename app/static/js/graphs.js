// ----------------------------------------------------------------------
// COMMON LANGUAGES OVER TIME LINE CHART
// ----------------------------------------------------------------------

var svg = dimple.newSvg("#timeLangChart", "100%", 500);
var timeLangChart = new dimple.chart(svg, timeLangData);
var x = timeLangChart.addTimeAxis("x", "occurred_at_week", "%d %b %Y", "%d %b %Y");
var y = timeLangChart.addMeasureAxis("y", "percentage");
var mySeries = timeLangChart.addSeries("language", dimple.plot.line);
mySeries.lineMarkers = true;

// custom tooltips
mySeries.getTooltipText = function (e) {
  return [
    e.aggField
  ];
};

// Axis formatting.
x.timePeriod = d3.time.weeks;
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

timeLangChart.draw(2000);
x.titleShape.remove();

// ----------------------------------------------------------------------
// SOURCE BAR CHART
// ----------------------------------------------------------------------

// standard dimple svg definition for a responsive chart
var svg = dimple.newSvg("#sourceBarChart", "100%", 500);

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
sourceChart.setMargins(150, 50, 20, 20);

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

};
// custom tooltips
mySeries.getTooltipText = function (e) {
  return [
    e.xValue + ' %'
  ];
};
// // Override the standard tooltip behaviour
//   mySeries.addEventHandler("mouseover", function (e){
//     console.log(e)
//
//     // Draw the text information in the top left corner
//     svg.selectAll(".dimple-hover-text")
//       .data([e.yValue, String(d3.format(".f")(e.aggField)) + "%"])
//         .enter()
//         .append("text")
//         .attr("class", "dimple-hover-text")
//         .attr("x", sourceChart._xPixels() + sourceChart._widthPixels() - 25)
//         .attr("y", function (d, i) { return sourceChart._yPixels() + sourceChart._heightPixels() - 50 + i * 25; })
//         .style("text-anchor", "end")
//         .style("font-size", "20px")
//         .style("fill", sourceChart.getColor(e.yValue).fill)
//         .style("pointer-events", "none")
//         .text(function (d) { return d ; } );
//
//     // Put a coloured bar next to the text for no good reason
//     svg.append("rect")
//       .attr("class", "dimple-hover-text")
//       .attr("x", sourceChart._xPixels() + sourceChart._widthPixels() - 15)
//       .attr("y", sourceChart._yPixels() + sourceChart._heightPixels() - 70)
//       .attr("height", 60)
//       .attr("width", 10)
//       .style("fill", sourceChart.getColor(e.yValue).fill)
//       .style("opacity", 1)
//       .style("pointer-events", "none");
//
//   });
//
//   // Clear the text on exit
//   mySeries.addEventHandler("mouseleave", function (e) {
//     svg.selectAll(".dimple-hover-text").remove();
//   });

sourceChart.draw(2000);

// ----------------------------------------------------------------------
// FREQUENCY OF STRING MATCH OVER TIME LINE CHART
// ----------------------------------------------------------------------
var plotStringMatchChart =  function(stringMatchData){

  var svg = dimple.newSvg("#timeStringMatchChart", "100%", 500);
  var timeStringMatchChart = new dimple.chart(svg, stringMatchData);
  var x = timeStringMatchChart.addTimeAxis("x", "occurred_at_week", "%d %b %Y", "%d %b %Y");
  var y = timeStringMatchChart.addMeasureAxis("y", "percentage");
  var mySeries = timeStringMatchChart.addSeries("string", dimple.plot.line);
  mySeries.lineMarkers = true;

  // custom tooltips
  mySeries.getTooltipText = function (e) {
    return [
      e.aggField[0]
    ];
  };

  // Axis formatting.
  x.timePeriod = d3.time.weeks;
  x.timeInterval = 1;
  x.fontSize = 14;
  y.fontSize = 14;
  y.title = "Percentage of tweets";

  timeStringMatchChart.draw(2000);
  x.titleShape.remove();
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
