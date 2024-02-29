async function visualizeDonutChart(data, element){
    const width = 600;
    const height = Math.min(width, 500);
    const radius = Math.min(width, height) / 2;

    const arc = d3.arc()
        .innerRadius(radius * 0.67)
        .outerRadius(radius - 1);

    const pie = d3.pie()
        .padAngle(1 / radius)
        .sort(null)
        .value(d => d.count);

    const color = d3.scaleOrdinal()
        .domain(data.map(d => d.country))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), data.length).reverse());

    const svg = d3.select(element)
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("style", "max-width: 100%; height: auto;");

    svg.append("g")
        .selectAll()
        .data(pie(data))
        .join("path")
        .attr("fill", d => color(d.data.country))
        .attr("d", arc)
        .append("title")
        .text(d => `${d.data.country}: ${d.data.count.toLocaleString()}`);

    svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 12)
        .attr("text-anchor", "middle")
        .selectAll()
        .data(pie(data))
        .join("text")
        .attr("transform", d => `translate(${arc.centroid(d)})`)
        .call(text => text.append("tspan")
            .attr("y", "-0.4em")
            .attr("font-weight", "bold")
            .text(d => d.data.country))
        .call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
            .attr("x", 0)
            .attr("y", "0.7em")
            .attr("fill-opacity", 0.7)
            .text(d => d.data.count.toLocaleString("en-US")));
}


// async function fetchData() {
//     const response = await fetch('/api/data/chart1/');
//     const data = await response.json();
//     // Now you have your data and can pass it to a D3.js function to visualize
//     await visualizeData(data);
// }

// fetchData();