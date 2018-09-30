
function plotShotChart(error, data, shotChartDivId) {
  if (error) throw error;

  var shotChartDiv = d3.select(`#${shotChartDivId}`);

  var svgHeight = shotChartDiv.node().getBoundingClientRect().height;
  var svgWidth = shotChartDiv.node().getBoundingClientRect().width;

  var svg = d3.select(`#${shotChartDivId}`).append("svg")
      .attr("width", svgWidth)
      .attr("height", svgHeight);

  var chartMargins = {top: svgHeight*.1, bottom: svgHeight*.1, left: 0, right:0};
  var chartHeight = +svg.attr("height") - chartMargins.top - chartMargins.bottom;
  var chartWidth = chartHeight * (30/21) //court size ratio
  chartMargins['left'] = (svgWidth - chartWidth)/2;
  chartMargins['right'] = (svgWidth - chartWidth)/2;

  var g = svg.append("g")
    .attr("transform", `translate(${chartMargins.left},${chartMargins.top})`);

  var x = d3.scaleLinear()
    .range([0, chartWidth])
    .domain([-25,25]);

  var y = d3.scaleLinear()
    .range([chartHeight, 0])
    .domain([-4,31]);

  var size = d3.scaleLinear()
    .range([25, 200])
    .domain(d3.extent (data, function (d)  {return d.totalShots;}));

  function linspace(start, end, n) {
    var out = [];
    var delta = (end - start) / (n - 1);
    var i = 0;
    while(i < (n - 1)) {
        out.push(start + (i * delta));
        i++;
    }
    out.push(end);
    return out;
  }
  var efgShotGradient = ["#22316C", "#0046AD", "#D6D6C9", "#D0103A", "#8B0000"];
  var color = d3.scaleLinear()
    .domain(linspace(0, 1, efgShotGradient.length))
    .range(efgShotGradient);

  // this section plots the actual data points
  g.selectAll(".point")
    .data(data)
    .enter().append("path")
      .attr("class", "point")
      .attr("d", d3.symbol().type(d3.symbolSquare).size(function(d) { return size(d.totalShots)} ))
      .attr("transform", function(d) { return `translate(${x(d.shotLocX)},${y(d.shotLocY)})`})
      .style("fill", function(d) { return color(d.efgPct); });
  // color points
  g.selectAll('circle')
      .attr('fill', function(d) {
          return color(d.z);
      });
  // DRAWING THE COURT
  // baseline
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(-25))
    .attr("y1", y(-4))
    .attr("x2", x(25))
    .attr("y2", y(-4));
  // left lane outter
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(-8))
    .attr("y1", y(-4)) //3.95 = 47.4 on other chart may be for line width in 4
    .attr("x2", x(-8))
    .attr("y2", y(13.75));
  // left lane inner
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(-6))
    .attr("y1", y(-4)) //3.95 = 47.4 on other chart may be for line width in 4
    .attr("x2", x(-6))
    .attr("y2", y(13.75));
  // right lane outter
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(8))
    .attr("y1", y(-4)) //3.95 = 47.4 on other chart may be for line width in 4
    .attr("x2", x(8))
    .attr("y2", y(13.75));
  // right lane inner
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(6))
    .attr("y1", y(-4)) //3.95 = 47.4 on other chart may be for line width in 4
    .attr("x2", x(6))
    .attr("y2", y(13.75));
  // free throw line
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(-8))
    .attr("y1", y(13.75))
    .attr("x2", x(8))
    .attr("y2", y(13.75));
  // straight line left side 3 point
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(-22))
    .attr("y1", y(-4))
    .attr("x2", x(-22))
    .attr("y2", y(9));
  // straight line left side 3 point
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(22))
    .attr("y1", y(-4))
    .attr("x2", x(22))
    .attr("y2", y(9));
  // backboard
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(-3))
    .attr("y1", y(-1.25))
    .attr("x2", x(3))
    .attr("y2", y(-1.25));
  // left rim connector
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(-.3))
    .attr("y1", y(-.55))
    .attr("x2", x(-.3))
    .attr("y2", y(-1.25));
  // right rim connector
  g.append("line")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("x1", x(.3))
    .attr("y1", y(-.55))
    .attr("x2", x(.3))
    .attr("y2", y(-1.25));
  // rim
  g.append("circle")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("fill", "none")
    .attr("cx", x(0))
    .attr("cy", y(0))
    .attr("r", x(.775)-x(0));
  // free throw circle variables
  var freeThrowCircleRadius = (x(-6)-x(6))/2;
  var freeThrowCircleRadians = 2 * Math.PI;
  var freeThrowCirclePoints = 50; // points to draw lines between for circle the higher the better the circle
  var freeThrowCirclePercentOfCircle = 0.5; // .5 because we are drawing half circle at a time
  var freeThrowCircleAngleScaler = d3.scaleLinear()
    .domain([0, freeThrowCirclePoints-1])
    .range([0, freeThrowCircleRadians]);
  var freeThrowCircleLine = d3.radialLine()
    .radius(freeThrowCircleRadius)
    .angle((d, i) => {
      if(i < (freeThrowCirclePoints*freeThrowCirclePercentOfCircle +1)) {
        return freeThrowCircleAngleScaler(i);
      }
    });
  // top free throw circle
  g.append("path")
    .datum(d3.range(freeThrowCirclePoints/2+1))
    .attr("class", "line")
  	.attr("transform", `translate(${x(0)},${y(13.75)}) rotate(90)`)
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("fill", "none")
    .attr("d", freeThrowCircleLine);
  // top free throw circle
  g.append("path")
    .datum(d3.range(freeThrowCirclePoints/2+1))
    .attr("class", "line")
  	.attr("transform", `translate(${x(0)},${y(13.75)}) rotate(-90)`)
    .style("stroke", "black")
    .attr("fill", "none")
    .attr("stroke-dasharray", "18 21")
    .attr('stroke-width', 3)
    .attr("d", freeThrowCircleLine);
  // three point line
  var threePointArcGenerator = d3.line()
     .curve(d3.curveCardinal);
  var threePointArcPoints = 50;
  var threePointArcCoords =[];
  for (xRaw = -22; xRaw <= 22; xRaw += 44/threePointArcPoints) {
    var yRaw = Math.sqrt(Math.pow(23.75,2)-Math.pow(xRaw,2));
    var arcCoords = [x(xRaw), y(yRaw)];
    threePointArcCoords.push(arcCoords);
  }
  g.append("path")
    .style("stroke", "black")
    .attr('stroke-width', 3)
    .attr("fill", "none")
    .attr("d", threePointArcGenerator(threePointArcCoords));
}


d3.json("../nba/lineup-shots?lineupId=1", function(error, data) {
  var shotChartDivId = "team_1_shot_chart";
  plotShotChart(error, data, shotChartDivId);
});

d3.json("../nba/lineup-shots?lineupId=1", function(error, data) {
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
