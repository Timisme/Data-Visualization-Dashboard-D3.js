
async function visualizeMapChart(data, element){
    // The svg
    const width = 800;
    const height = 500;
    const svg = d3.select(element)
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto;");

    // Map and projection
    const path = d3.geoPath();
    const projection = d3.geoMercator()
    .scale(100)
    .center([0,20])
    .translate([width / 2, height / 2]);

    // Data and color scale
    let mapData = new Map();
    const colorScale = d3.scaleThreshold()
    .domain([0, 5, 10, 20, 50, 100, 150])
    .range(d3.schemeBlues[7]);

    // extra data for tooltip
    let intensityMapper = {}
    let likelihoodMapper = {}
    let relevanceMapper = {}

    d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")
    .then(function(topo) {

        // remove Antarctica from the map
        topo.features = topo.features.filter(function(feature) {
            return feature.properties.name !== "Antarctica";
        });

        // set data on the map by country code (3 digits)
        data.forEach(item => {
            mapData.set(item.code, +item.count)
            intensityMapper[item.code] = item.avg_intensity
            likelihoodMapper[item.code] = item.avg_likelihood
            relevanceMapper[item.code] = item.avg_relevance
        })

        let tooltip = d3.select("body")
            .append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        let mouseOver = function(event, d) {
            console.log("d: ", d)
            tooltip.transition()
                .duration(200)
                .style("opacity", 1);

            tooltip.html(
                `<strong>${d.properties.name}</strong>` + "<br/>" + "Data Count: " + (mapData.get(d.id) || 0)
                + "<br/>" + "Average Intensity: " + intensityMapper[d.id].toFixed(1)
                + "<br/>" + "Average Likelihood: " + likelihoodMapper[d.id].toFixed(1)
                + "<br/>" + "Average Relevance: " + relevanceMapper[d.id].toFixed(1)
            )
                .style("left", (event.pageX + 20) + "px")
                .style("top", (event.pageY - 28) + "px");

            d3.selectAll(".Country")
                .transition()
                .duration(200)
                .style("opacity", .5)

            d3.select(this)
                .transition()
                .duration(200)
                .style("opacity", 1)
                .style("stroke", "black")
        }

        let mouseLeave = function(d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
            d3.selectAll(".Country")
                .transition()
                .duration(200)
                .style("opacity", .8)
            d3.select(this)
                .transition()
                .duration(200)
                .style("stroke", "transparent")
        }

        // Draw the map
        svg.append("g")
            .selectAll("path")
            .data(topo.features)
            .enter()
            .append("path")
            // draw each country
            .attr("d", d3.geoPath()
                .projection(projection)
            )
            // set the color of each country
            .attr("fill", function (d) {
                d.total = mapData.get(d.id) || 0;
                return colorScale(d.total);
            })
            .style("stroke", "transparent")
            .attr("class", function(d){ return "Country" } )
            .style("opacity", .8)
            .on("mouseover", mouseOver)
            .on("mouseleave", mouseLeave)
        })
}
