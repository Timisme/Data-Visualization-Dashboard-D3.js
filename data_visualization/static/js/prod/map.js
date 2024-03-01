
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
    .domain([0, 10, 50, 100])
    .range(d3.schemeBlues[4]);

    // Load external data and boot
    // Promise.all([
    // d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"),
    // d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world_population.csv", function(d) {
    //     mapData.set(d.code, +d.pop)
    // })]).then(function(loadData){
    //     topo = loadData[0];

    d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")
    .then(function(topo) {

        // remove Antarctica from the map
        topo.features = topo.features.filter(function(feature) {
            return feature.properties.name !== "Antarctica";
        });

        // set data on the map by country code (3 digits)
        data.forEach(item => {
            mapData.set(item.code, +item.count)
        })

        console.log(mapData)
        console.log(data)

        let tooltip = d3.select("body")
            .append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        let mouseOver = function(event, d) {
            tooltip.transition()
                .duration(10)
                .style("opacity", .9);
            tooltip.html(d.properties.name + "<br/>" + "Count: " + (mapData.get(d.id) || 0))
                .style("left", (event.pageX) + "px")
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
                .duration(10)
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
            .on("mouseover", mouseOver )
            .on("mouseleave", mouseLeave )
        })
}
