// modified from http://neuralengr.com/asifr/journals/

var margin = {top: 20, right: 200, bottom: 0, left: 20}, // TODO: don't really need margin.right
	width = 400,
	height = 650; // TODO: need to update for ~50 neighbourhoods

var c = d3.scale.category20c();

var svg = d3.select("body").append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.style("margin-left", margin.left + "px")
	.append("g") // D3 group element
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json("data/sample_data.json", function(data) {
  
//    TODO: look into using a scale and xAxis

	for (var j = 0; j < data.length; j++) {
		var g = svg.append("g")
            .attr("class","neighbourhood")
            .attr("transform", "translate(" + 0 + "," + j*10 + ")");

		var circles = g.selectAll("circle")
			.data(data[j]['crime_types'])
			.enter()
			.append("circle");
        
        console.log(circles)

		var text = g.selectAll("text")
			.data(data[j]['crime_types'])
			.enter()
			.append("text");

//		var rScale = d3.scale.linear()
//			.domain([0, d3.max(data[j]['crime_types'], function(d) { return d[1]; })])
//			.range([2, 9]);
      
        var rScale = d3.scale.linear()
            .domain([0, 1500])
            .range([0, 30]);
        
        circles
            .attr("cx", function(d, i) { return i*30+175; })
            .attr("cy", j*20+20)
            .attr("r", function(d) { return rScale(d3.values(d)[0]); })
            .style("fill", function(d) { return c(j); });
      
		text
			.attr("y", j*20+25)
			.attr("x",function(d, i) { return i*30+175; })
			.attr("class", "value")
			.text(function(d){ return d3.values(d)[0]; }) // each d = {key:value} of crime_types
			.style("fill", function(d) { return c(j); })
            .style("text-anchor", "middle")
			.style("display", "none");

		g.append("text")
			.attr("y", j*20+25)
			.attr("x", 140) // Setting text-anchor to end means x must be x-(text.length) where text.length is max px of label
			.attr("class", "label")
			.text(data[j]['name'])
			.style("fill", function(d) { return c(j); })
            .style("text-anchor", "end")
			.on("mouseover", mouseover)
			.on("mouseout", mouseout);
      
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