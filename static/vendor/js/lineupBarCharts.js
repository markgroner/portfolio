

function plotNbaGroupedBar(error, data, graphDivId) {

  if (error) throw error;

  var chartTitle = "Scoring";
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
  var teamAbbreviations = data.team_abbreviations;
  var statKeys = data.stat_keys;
  var graphData = data.graphData;
  console.log(teamAbbreviations);
  console.log(statKeys);
  console.log(graphData);

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
      .attr("transform", function(d) { return "translate(" + x0(d.teamAbbreviation) + ",0)"; })
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
      .attr("transform", "translate(0," + chartHeight + ")")
      .call(d3.axisBottom(x0));


  g.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y).ticks(5, "p"))
    .append("text")
      .attr("x", 8)
      .attr("y", y(y.ticks().pop()) + 0.5)
      .attr("dy", "0.32em")
      .attr("fill", "#000")
      .attr("font-weight", "bold")
      .attr("font-size", "14")
      .attr("text-anchor", "start")
      .text(chartTitle);

/*
  var legend = g.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("text-anchor", "end")
    .selectAll("g")
    .data(statKeys.slice())
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });



  legend.append("rect")
      .attr("x", chartWidth - 19)
      .attr("width", 19)
      .attr("height", 19)
      .attr("fill", colors);


  legend.append("text")
      .attr("x", chartWidth - 24)
      .attr("y", 9.5)
      .attr("dy", "0.32em")
      .text(function(d) { return d; });
*/
 var width = 500;
 var height = 75;
 var svgw = 20;
 var svgh = 20;
 var dataL = 0;
 var offset = 80;
 var legendColorBoxSize = 15;
 var legendPaddingY = chartMargins.bottom - chartMargins.top;
 var legendPaddingX = svgWidth*.25;

  var legend = svg.append("g")
      .attr("width", width)
      .attr("height", height - 50)
      .selectAll("g")
      .data(statKeys)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
         if (i === 0) {
            dataL = d.length + offset
            return "translate(0,0)"
        } else {
         var newdataL = dataL
         dataL +=  d.length + offset
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
  .text(function (d, i) {
      return d
  })
  .attr("class", "textselected")
  .style("text-anchor", "start")
          .attr("font-family", "sans-serif")
          .attr("font-size", 10);


};





/* SCORING GRAPH */
d3.json("../static/nba-grouped-bar-data.json", function(error, data) {
  plotNbaGroupedBar(error, data, "#scoring_graph");
});
