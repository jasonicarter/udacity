/*
// central idea modified from http://neuralengr.com/asifr/journals/
*/

var margin = {top: 80, right: 0, bottom: 0, left: 20},
	width = 800, // width of neighbourhood + crime types + comm_housing bars
	height = 650; // TODO: need to update

var maxBarWidth = 200,
    barHeight = 20
    xAxisWidth = 400;

// http://bl.ocks.org/aaizemberg/78bd3dade9593896a59d
var c10 = d3.scale.category10();

// TODO: pull this from dataset
var x = d3.scale.ordinal()
    .domain(["Arsons","Assaults", "Break & Enters", "Fire Alarms", "Medical Calls",
            "Vehicle Incidents", "Hazardous Incidents", "Murders", "Robberies",
            "Sexual Assaults", "Thefts", "Vehicle Thefts"])
    .rangePoints([0, xAxisWidth]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("top");

var xBarScale = d3.scale.linear()
    .domain([0, 1]) //d3.max(data, function(d) { return d.comm_housing_pop_ratio; })]);
    .range([0, 10]);

// http://bl.ocks.org/mstanaland/6106487
var formatDecimal = d3.format(".2f")

// TODO: update with with bar width
var svg = d3.select("body").append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.style("margin-left", margin.left + "px")
	.append("g") // D3 group element
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(" + 165 + "," + 0 + ")")
    .call(xAxis)
  .selectAll("text")
    .attr("y", -10)
    .attr("x", 5)
    .attr("dy", ".35em")
    .attr("transform", "rotate(-45)")
    .style("text-anchor", "start");

// Load data and create svg elements
d3.json("data/data_formatted.json", function(data) {
    
    // Apply svg elements for each individual record / neighbourhood
	for (var j = 0; j < data.length; j++) {
		var g = svg.append("g")
            .attr("class","neighbourhood")
            .attr("transform", "translate(" + 0 + "," + j*5 + ")");

		var circles = g.selectAll("circle")
                .data(data[j]['crime_types'])
			.enter()
                .append("circle");

		var text = g.selectAll("text")
                .data(data[j]['crime_types'])
			.enter()
                .append("text");
      
        var rScale = d3.scale.sqrt() // d3.scale.linear()
            .domain([1, 800 ]) // .domain([0, d3.max(data[j]['crime_types'], function(d) { return d3.values(d)[0]; }) ])
            .range([1, 10])
            // .clamp(true);
        
        circles
            .attr("cx", function(d, i) { return i*35+175; })
            .attr("cy", j*20+20)
            .attr("r", function(d) { return rScale(d3.values(d)[0]); })
            .style("fill", function(d,i) { return c10(i); });
      
		text
			.attr("y", j*20+25)
			.attr("x",function(d, i) { return i*35+175; })
			.attr("class", "value")
			.text(function(d){ return d3.values(d)[0]; }) // each d = {key:value} of crime_types
			.style("fill", function(d,i) { return c10(i); })
            .style("text-anchor", "middle")
			.style("display", "none");

		g.append("text")
			.attr("y", j*20+25)
			.attr("x", 140) // Setting text-anchor to end means x must be x-(text.length) where text.length is max px of label
			.attr("class", "label")
			.text(data[j]['name'])
            .style("text-anchor", "end")
			.on("mouseover", mouseover)
			.on("mouseout", mouseout);
        
        g.append("rect")
            .attr("width", xBarScale(data[j]["comm_housing_pop_ratio"])*100)
            .attr("height", barHeight)
            .attr("class", "housing")
            .attr("y", j*20+25/2) // center rect on each neighbourhood
            .attr("transform", "translate(" + 600 + "," + 0 + ")") // TODO: get this working with variables
            .style("fill", c10(0));
            
        g.append("text")
            .attr("x", xBarScale(data[j]["comm_housing_pop_ratio"])*100)
            .attr("y", j*20+25/2)
            .attr("dy", "1.35em") //vertical align middle
            .attr("transform", "translate(" + 610 + "," + 0 + ")") // TODO: use exiting or put in variables at top
            .text(formatDecimal(data[j]["comm_housing_pop_ratio"]*100) + "%");
      
	};
    
	function mouseover(p) {
		var g = d3.select(this).node().parentNode;
		d3.select(g).selectAll("circle").style("display","none");
		d3.select(g).selectAll("text.value").style("display","block");
	}

	function mouseout(p) {
		var g = d3.select(this).node().parentNode;
		d3.select(g).selectAll("circle").style("display","block");
		d3.select(g).selectAll("text.value").style("display","none");
	}
});