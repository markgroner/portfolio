

function plotNbaGroupedBar(error, data, graphDivId, yAxisMeasure) {

  if (error) throw error;


  var barGraphDiv = d3.select(graphDivId);
  var svgHeight = barGraphDiv.node().getBoundingClientRect().height;
  var svgWidth = barGraphDiv.node().getBoundingClientRect().width;

  var svg = barGraphDiv.append("svg")
        .attr("height", svgHeight)
        .attr("width", svgWidth)

  var chartMargins = {top: svgHeight*.1, right: svgWidth*.1, bottom: svgHeight*.2, left: svgWidth*.1};
  var chartWidth = +svg.attr("width") - chartMargins.left - chartMargins.right;
  var chartHeight = +svg.attr("height") - chartMargins.top - chartMargins.bottom;


  var g = svg.append("g").attr("transform", "translate(" + chartMargins.left + "," + chartMargins.top + ")");
  var teamAbbreviations = data.teamAbbreviations;
  var statKeys = data.statKeys;
  var graphData = data.graphData;
  var graphTitle = data.graphTitle;

  // scale x to chart
  var x0 = d3.scaleBand()
      .rangeRound([0, chartWidth])
      .paddingInner(0.1)
      .domain(teamAbbreviations);

  var x1 = d3.scaleBand()
      .padding(0.05)
      .domain(statKeys).rangeRound([0, x0.bandwidth()]);

  var y = d3.scaleLinear()
      .rangeRound([chartHeight, 0])
      .domain([0, d3.max(graphData, function(d) { return d3.max(statKeys, function(key) { return d[key]; }); })]).nice();

  var colors = d3.scaleOrdinal()
      .range(["#0046AD", "#D6D6C9", "#D0103A"]);



  g.append("g")
    .selectAll("g")
    .data(graphData)
    .enter().append("g")
      .attr("transform", function(d) { return `translate(${x0(d.teamAbbreviation)},0)`; })
    .selectAll("rect")
    .data(function(d) { return statKeys.map(function(key) { return {key: key, value: d[key]}; }); })
    .enter().append("rect")
      .attr("x", function(d) { return x1(d.key); })
      .attr("y", function(d) { return y(d.value); })
      .attr("width", x1.bandwidth())
      .attr("height", function(d) { return chartHeight - y(d.value); })
      .attr("fill", function(d) { return colors(d.key); });

  g.append("g")
      .attr("class", "axis")
      .attr("transform", `translate(0,${chartHeight})`)
      .call(d3.axisBottom(x0))
      .attr("font-weight", "bold");


  g.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y).ticks(5, yAxisMeasure))
    .append("text")
    .style("text-anchor", "middle")
      .attr("x", chartWidth*.5)
      .attr("y", 0)
      //.attr("dy", "0.32em")
      .attr("fill", "#000")
      .attr("font-weight", "bold")
      .attr("font-size", "14")
      .attr("text-anchor", "start")
      .text(graphTitle);


 var legendColorBoxSize = 15;
 var legendPaddingY = chartMargins.bottom - chartMargins.top;
 var legendPaddingX = svgWidth*.25;
 var legendKeysOffset = svgWidth*.2;

  var legend = svg.append("g")
      .attr("width", svgWidth)
      .attr("height", legendPaddingY - 50)
      .selectAll("g")
      .data(statKeys)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
         if (i === 0) {
            dataL = d.length + legendKeysOffset
            return "translate(0,0)"
        } else {
         var newdataL = dataL
         dataL +=  d.length + legendKeysOffset
         return `translate(${newdataL},0)`
        }
  })

  legend.append("rect")
      .attr("x", legendPaddingX)
      .attr("y", svgHeight - legendPaddingY)
      .attr("width", legendColorBoxSize)
      .attr("height", legendColorBoxSize)
      .style("fill", function (d, i) {
      return colors(i)
  })

  legend.append("text")
      .attr("x", legendPaddingX + 20)
      .attr("y", svgHeight - legendPaddingY + 10)
  .attr("dy", ".1em")
  .text(function (d, i) { return d })
  .attr("class", "textselected")
  .style("text-anchor", "start")
          .attr("font-family", "sans-serif")
          .attr("font-size", 10);


};



/* RATINGS GRAPH */
d3.json("../nba/grouped-bar-data?graphTitle=Ratings", function(error, data) {
  plotNbaGroupedBar(error, data, "#ratings_graph", "d");
});

/* SHOOTING GRAPH */
d3.json("../nba/grouped-bar-data?graphTitle=Shooting", function(error, data) {
  plotNbaGroupedBar(error, data, "#shooting_graph", "p");
});

/* SCORING GRAPH */
d3.json("../nba/grouped-bar-data?graphTitle=Scoring", function(error, data) {
  plotNbaGroupedBar(error, data, "#scoring_graph", "p");
});

/* REBOUNDING GRAPH */
d3.json("../nba/grouped-bar-data?graphTitle=Rebounding", function(error, data) {
  console.log('here')
  plotNbaGroupedBar(error, data, "#rebounding_graph", "p");
});




/* SHOOTING GRAPH */
d3.json("../static/nba-grouped-bar-data.json", function(error, data) {
  plotNbaGroupedBar(error, data, "#sample_data_graph", "p");
});
