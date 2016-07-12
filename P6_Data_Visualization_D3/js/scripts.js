// modified from http://neuralengr.com/asifr/journals/
var margin = {top: 20, right: 400, bottom: 0, left: 20}, // TODO: don't really need margin.right
	width = 400,
	height = 650; // TODO: need to update for ~50 neighbourhoods

var maxBarWidth = 200,
    barHeight = 20;

// http://bl.ocks.org/aaizemberg/78bd3dade9593896a59d
var c10 = d3.scale.category10();

// TODO: pull this from dataset
var x = d3.scale.ordinal()
    .domain(["arsons","assaults", "break_enters", "fire_fire_alarms", "fire_medical_calls",
            "fire_vehicle_incidents", "hazardous_incidents", "murders", "robberies",
            "sexual_assaults", "thefts", "vehicle_thefts"])
    .rangePoints([0, width]);

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
//            .clamp(true);
        
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
        
//        d3.select("input").on("change", change);
//
//        var sortTimeout = setTimeout(function() {
//            d3.select("input").property("checked", true).each(change);
//        }, 2000);
//
//        function change() {
//            clearTimeout(sortTimeout);
//
//            // Copy-on-write since tweens are evaluated after a delay.
//            var x0 = x.domain(data.sort(this.checked
//                ? function(a, b) { return b["total_pop"] - a["total_pop"]; }
//                : function(a, b) { return d3.ascending(a["name"], b["name"]); })
//                .map(function(d) { return d["name"]; }))
//                .copy();
//
//            svg.selectAll("neighbourhood")
//                .sort(function(a, b) { return x0(a["total_pop"]) - x0(b["total_pop"]); });
//
//            var transition = svg.transition().duration(750),
//                delay = function(d, i) { return i * 50; };
//
//            transition.selectAll("neighbourhood")
//                .delay(delay)
//                .attr("x", function(d) { return x0(d["name"]); });

//            transition.select(".x.axis")
//                .call(xAxis)
//              .selectAll("g")
//                .delay(delay);
//        }
      
	};
        
        
var sortOrder = false;
var sortBars = function () {
    sortOrder = !sortOrder;
  
    console.log("I'm here")
  
    sortItems = function (a, b) {
        if (sortOrder) {
            return console.log(a) //a.total_pop - b.total_pop;
        }
        return console.log("this is b") //b.total_pop - a.total_pop;
    };

    svg.selectAll(".label")
        .sort(sortItems)
        .transition()
        .delay(function (d, i) {
          console.log("i'm here too")
        return i * 50;
    })
        .duration(1000)
        .attr("x", function (d, i) {
        return i; //xScale(i);
    });

//    svg.selectAll('text')
//        .sort(sortItems)
//        .transition()
//        .delay(function (d, i) {
//        return i * 50;
//    })
//        .duration(1000)
//        .text(function (d) {
//        return d.value;
//    })
//        .attr("text-anchor", "middle")
//        .attr("x", function (d, i) {
//          return i + i / 2;
////        return xScale(i) + xScale.rangeBand() / 2;
//    })
//        .attr("y", function (d) {
//        return h - yScale(d.total_pop) + 14;
//    });
};
// Add the onclick callback to the button
//d3.select("#sort").on("click", sortBars);    
d3.select("input").on("change", sortBars);
        

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