
function plotShotChart(error, data, shotChartDivId) {
  if (error) throw error;

  var shotChartDiv = d3.select(`#${shotChartDivId}`);

  var svgHeight = shotChartDiv.node().getBoundingClientRect().height;
  var svgWidth = shotChartDiv.node().getBoundingClientRect().width;

  var svg = d3.select(`#${shotChartDivId}`).append("svg")
      .attr("width", svgWidth)
      .attr("height", svgHeight);

  var chartMargins = {top: svgHeight*.1, right: svgWidth*.1, bottom: svgHeight*.1, left: svgWidth*.1};
  var chartWidth = +svg.attr("width") - chartMargins.left - chartMargins.right;
  var chartHeight = +svg.attr("height") - chartMargins.top - chartMargins.bottom;


  var g = svg.append("g")
      .attr("transform", `translate(${chartMargins.left},${chartMargins.top})`);


  var x = d3.scaleLinear()
      .range([0, chartWidth]);

  var y = d3.scaleLinear()
      .range([chartHeight, 0]);

  var r = d3.scaleLinear()
      .range([7, 18]);

  var color = d3.scaleOrdinal()
        .range(["#8c510a", "#dfc27d", "#35978f"]);

  var r = d3.scaleLinear()
      .range([7, 18])
      .domain(d3.extent (data, function (d)  {return d.totalShots;}));


  g.append("g")
      .attr("class", "x axis")
      .attr("transform", `translate(0,${chartHeight})`)
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "y axis")
      .call(d3.axisLeft(y));

  g.selectAll(".dot")
    .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", function(d) { return r(d.totalShots); })
      .attr("cx", function(d) { return x(d.shotLocX); })
      .attr("cy", function(d) { return y(d.shotLocY); })
      .style("fill", function(d) { return color(d.efgPct); });
}






d3.json("../static/vendor/shotChartData.json", function(error, data) {
  var shotChartDivId = "team_1_shot_chart";
  plotShotChart(error, data, shotChartDivId);
});

d3.json("../static/vendor/shotChartData.json", function(error, data) {
  var shotChartDivId = "team_2_shot_chart";
  plotShotChart(error, data, shotChartDivId);
});

/*
d3.csv("../static/vendor/shotChartData.csv", function(error, data) {
  var shotChartDivId = "team_2_shot_chart";
  plotShotChart(error, data, shotChartDivId);
});
*/
/*
function resize() {

  var shotChartDivId = "team_1_shot_chart";
  var dim = Math.min(parseInt(d3.select("#team_1_shot_chart").style("width")), parseInt(d3.select("#team_1_shot_chart").style("height")));

  var shotChartDiv = d3.select(`#${shotChartDivId}`);
  var svg = d3.select("#team_1_shot_chart").append("svg")
      .attr("width", svgWidth)
      .attr("height", svgHeight);
  var svgHeight = shotChartDiv.node().getBoundingClientRect().height;
  var svgWidth = shotChartDiv.node().getBoundingClientRect().width;
  var chartMargins = {top: 40, right: 40, bottom: 40, left: 40};

  var chartWidth = +svg.attr("width") - chartMargins.left - chartMargins.right;
  var chartHeight = +svg.attr("height") - chartMargins.top - chartMargins.bottom;

  // Update the range of the scale with new width/height
  x.range([0, chartWidth]);
  y.range([chartHeight, 0]);

  // Update the axis and text with the new scale
  g.select('.x.axis')
    .attr("transform", `translate(0,${svgHeight})`)
    .call(xAxis);

  g.select('.x.axis').select('.label')
      .attr("x", svgWidth);

  g.select('.y.axis')
    .call(yAxis);
/*
  // Update the tick marks
  xAxis.ticks(dim / 75);
  yAxis.ticks(dim / 75);

  // Update the circles
  r.range([dim / 90, dim / 35])

  g.selectAll('.dot')
    .attr("r", function(d) {return r(d.TotalValue)})
    .attr("cx", function(d) { return x(d.ProductConcentration); })
    .attr("cy", function(d) { return y(d.CustomerConcentration); })
}

d3.select(window).on('resize', resize);

resize();
*/
