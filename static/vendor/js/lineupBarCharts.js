// Dataset we will be using to set the height of our rectangles
var booksReadThisYear = [17, 23, 20, 34];
var svgHeight = 400;
var svgWeight = 400;
// Append an SVG wrapper to the page and set a variable equal to a reference to it
var svg = d3.select("#ratings_graph")
  .append("svg")
    .attr("height", svgHeight)
    .attr("width", svgWeight);

var svgGroup = svg.append("g")
  .attr("transform", "translate(50, 100)");
// Vertical Bar Chart
// Selects all rectangles currently on the page - which is none - and binds our dataset to them. If there are no rectangles, it will append one for each piece of data.
svgGroup.selectAll("rect")
  .data(booksReadThisYear)
  .enter()
  .append("rect")
  .classed("bar", true)
  .attr("width", 50)
  // Setting the height of our rectangles now uses an anonymous function that selects a single piece of data from our dataset and multiplies it by 10
  .attr("height", function(data) {
    return data * 10;
  })
  // Setting the height of our rectangles now uses an anonymous function that selects a single piece of data from our dataset and multiplies it by 10
  .attr("x", function(data, index) {
    return index * 60;
  })
  .attr("y", function(d) {
    return svgHeight - d * 10;
  });


  /* SHOOTING GRAPH8 */

    // Define SVG area dimensions
    var svgWidth = 960;
    var svgHeight = 500;

    // Define the chart's margins as an object
    var chartMargin = {
      top: 30,
      right: 30,
      bottom: 30,
      left: 30
    };

    // Define dimensions of the chart area
    var chartWidth = svgWidth - chartMargin.left - chartMargin.right;
    var chartHeight = svgHeight - chartMargin.top - chartMargin.bottom;

    // Select body, append SVG area to it, and set the dimensions
    var svg = d3.select("#shooting_graph")
      .append("svg")
      .attr("height", svgHeight)
      .attr("width", svgWidth)

    // Append a group to the SVG area and shift ('translate') it to the right and to the bottom
    var chartGroup = svg.append("g")
      .attr("transform", "translate(" + chartMargin.right + ", " + chartMargin.top + ")");

    // Configure a band scale, with a range between 0 and the chartWidth and a padding of 0.1 (10%)
    var xBandScale = d3.scaleBand().range([0, chartWidth]).padding(0.1);

    // Create a linear scale, with a range between the chartHeight and 0.
    var yLinearScale = d3.scaleLinear().range([chartHeight, 0]);

    // var barColorArray = ['#0046AD', '#D6D6C9', '#D0103A']

    // Load data from hours-of-tv-watched.csv
    d3.csv("../static/nba-sample.csv", function (error, nbaBarChartData) {
      if (error) throw error;

      console.log(nbaBarChartData);

      // Set the domain of the band scale to the names of students in hours-of-tv-watched.csv
      xBandScale.domain(nbaBarChartData.map(function (data) {
        return data.lineupMetric;
      }));

      // Set the domain of the linear scale to 0 and the largest number of hours watched in nbaBarChartData
      yLinearScale.domain([0, d3.max(nbaBarChartData, function (data) {
        return data.value;
      })]);

      // Create two new functions passing our scales in as arguments
      // These will be used to create the chart's axes
      var bottomAxis = d3.axisBottom(xBandScale);
      var leftAxis = d3.axisLeft(yLinearScale).ticks(10);


      // Create one SVG rectangle per piece of nbaBarChartData
      // Use the linear and band scales to position each rectangle within the chart
      chartGroup.selectAll(".bar")
        .data(nbaBarChartData)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", function (data) {
          return xBandScale(data.lineupMetric);
        })
        .attr("y", function (data) {
          return yLinearScale(data.value);
        })
        .attr("width", xBandScale.bandwidth())
        .attr("height", function (data) {
          return chartHeight - yLinearScale(data.value);
        })
        .style("fill", function (data) {
          return d3.rgb(data.color)
        });

      // Append two SVG group elements to the chartGroup area,
      // and create the bottom and left axes inside of them
      chartGroup.append("g")
        .call(leftAxis);

      chartGroup.append("g")
        .attr("transform", "translate(0, " + chartHeight + ")")
        .call(bottomAxis);
    });


/* SCORING GRAPH */

var svgHeight = 500;
var svgWeight = 960;

var svg = d3.select("#scoring_graph_2")
    .append("svg")
      .attr("height", svgHeight)
      .attr("width", svgWeight),
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var x0 = d3.scaleBand()
    .rangeRound([0, width])
    .paddingInner(0.1);

var x1 = d3.scaleBand()
    .padding(0.05);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var z = d3.scaleOrdinal()
    .range(['#0046AD', '#D6D6C9', '#D0103A']);

d3.csv("../static/nba-grouped-bar-data.csv", function(d, i, columns) {
  for (var i = 1, n = columns.length; i < n; ++i) d[columns[i]] = +d[columns[i]];
  return d;
}, function(error, data) {
  if (error) throw error;

  var keys = data.columns.slice(1);

  x0.domain(data.map(function(d) { return d.State; }));
  x1.domain(keys).rangeRound([0, x0.bandwidth()]);
  y.domain([0, d3.max(data, function(d) { return d3.max(keys, function(key) { return d[key]; }); })]).nice();

  g.append("g")
    .selectAll("g")
    .data(data)
    .enter().append("g")
      .attr("transform", function(d) { return "translate(" + x0(d.State) + ",0)"; })
    .selectAll("rect")
    .data(function(d) { return keys.map(function(key) { return {key: key, value: d[key]}; }); })
    .enter().append("rect")
      .attr("x", function(d) { return x1(d.key); })
      .attr("y", function(d) { return y(d.value); })
      .attr("width", x1.bandwidth())
      .attr("height", function(d) { return height - y(d.value); })
      .attr("fill", function(d) { return z(d.key); });

  g.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x0));

  g.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y).ticks(null, "s"))
    .append("text")
      .attr("x", 2)
      .attr("y", y(y.ticks().pop()) + 0.5)
      .attr("dy", "0.32em")
      .attr("fill", "#000")
      .attr("font-weight", "bold")
      .attr("text-anchor", "start")
      .text("Population");

  var legend = g.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("text-anchor", "end")
    .selectAll("g")
    .data(keys.slice().reverse())
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width - 19)
      .attr("width", 19)
      .attr("height", 19)
      .attr("fill", z);

  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9.5)
      .attr("dy", "0.32em")
      .text(function(d) { return d; });
  console.log('made it here')
});



/*
d3.select(window).on("resize", handleResize);

// When the browser loads, loadChart() is called
loadChart();

function handleResize() {
  var svgArea = d3.select("#scoring_graph");

  // If there is already an svg container on the page, remove it and reload the chart
  if (!svgArea.empty()) {
    svgArea.remove();
    loadChart();
  }
}

function loadChart() {
    var svgWidth = window.innerWidth;
    var svgHeight = window.innerHeight;

    var margin = {
        top: 30,
        right: 30,
        bottom: 30,
        left: 30
    };
    var chartWidth = svgWidth - margin.left - margin.right;
    var chartHeight = svgHeight - margin.top - margin.bottom;


    var svg = d3.select("body").append('svg')
        .attr("height", svgHeight)
        .attr("width", svgWidth);

    var chartGroup = svg.append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    d3.csv("../static/hours-of-tv-watched.csv", function (error, tvData) {
        if (error) return console.warn(error);

        tvData.forEach(function (data) {
            data.hours = +data.hours;
        })

        var labels = tvData.map(d => d.name);
        // scale x to chart
        var xScale = d3.scaleBand()
            .domain(labels)
            .range([0, chartWidth]);

        var hours = tvData.map(d => d.hours);
        // scale y
        var yScale = d3.scaleLinear()
            .domain([0, d3.max(hours)])
            .range([chartHeight, 0]);

        var yAxis = d3.axisLeft(yScale);
        var xAxis = d3.axisBottom(xScale);

        chartGroup.append("g")
            .attr("transform", `translate(0, ${chartHeight})`)
            .call(xAxis);

        chartGroup.append("g")
            .call(yAxis);

        var barWidth = chartWidth / tvData.length;
        chartGroup.selectAll(".bar")
            .data(tvData)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", (d, i) => xScale(labels[i]))
            .attr("y", d => yScale(d.hours))
            .attr("width", xScale.bandwidth())
            .attr("height", d => chartHeight - yScale(d.hours))
    });

}
*/
