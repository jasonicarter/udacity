// (keep) Used to keep truncate stings titles/labels
function truncate(str, maxLength, suffix) {
	if(str.length > maxLength) {
		str = str.substring(0, maxLength + 1); 
		str = str.substring(0, Math.min(str.length, str.lastIndexOf(" ")));
		str = str + suffix;
	}
	return str;
}

// (update) Create spacing and width/height of content
var margin = {top: 20, right: 200, bottom: 0, left: 20}, // Need to flip 'right' for left as labels will be on left side
	width = 300, // Need to update 
	height = 650; // Need to update

// (remove) 
var start_year = 2004,
	end_year = 2013;

var c = d3.scale.category20c();

// (keep)
var x = d3.scale.linear()
	.range([0, width]);

var svg = d3.select("body").append("svg") // Need to fix up spacing here to give label more room on right side
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.style("margin-left", margin.left + "px")
	.append("g") // D3 group element
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json("data/journals_optogenetic.json", function(data) {
	x.domain([start_year, end_year]);
	var xScale = d3.scale.linear()
		.domain([start_year, end_year])
		.range([0, width]);

	for (var j = 0; j < data.length; j++) {
		var g = svg.append("g")
            .attr("class","journal");

		var circles = g.selectAll("circle")
			.data(data[j]['articles'])
			.enter()
			.append("circle");

		var text = g.selectAll("text")
			.data(data[j]['articles'])
			.enter()
			.append("text");

		var rScale = d3.scale.linear()
			.domain([0, d3.max(data[j]['articles'], function(d) { return d[1]; })])
			.range([2, 9]);

		circles
			.attr("cx", function(d, i) { return xScale(d[0])+150; }) // TODO: what is d[0] value print out
			.attr("cy", j*20+20)
			.attr("r", function(d) { return rScale(d[1]); })
			.style("fill", function(d) { return c(j); });

		text
			.attr("y", j*20+25)
			.attr("x",function(d, i) { return xScale(d[0])+150; }) // Controls text in circle x dist from labels
			.attr("class","value")
			.text(function(d){ return d[1]; })
			.style("fill", function(d) { return c(j); })
			.style("display","none");

		g.append("text")
			.attr("y", j*20+25)
			.attr("x", 0)
			.attr("class","label")
			.text(truncate(data[j]['name'],30,"...")) // This is maxLength in characters need to get a static length in px
			.style("fill", function(d) { return c(j); })
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