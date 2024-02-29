async function visualizeData(data){
    // Set up dimensions
    const width = 400;
    const height = 400;
    const radius = Math.min(width, height) / 2;

    // Set up color scale
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // Create SVG element
    const svg = d3.select("#chart-container")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", `translate(${width / 2}, ${height / 2})`);

    // Create pie generator
    const pie = d3.pie()
    .value(d => d.count);

    // Create arc generator
    const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(radius);

    // Iterate over data and create arcs
    const arcs = svg.selectAll("arc")
    .data(pie(data))
    .enter()
    .append("g")
    .attr("class", "arc");

    // Append path elements to SVG
    arcs.append("path")
    .attr("d", arc)
    .attr("fill", d => color(d.data.country))
    .attr("stroke", "white")
    .attr("stroke-width", 2);

    // Append text labels to SVG
    const textOffset = 50;
    arcs.append("text")
    .attr("transform", d => {
    const pos = arc.centroid(d);
    const angle = Math.atan2(pos[1], pos[0]);
    const x = radius * Math.cos(angle);
    const y = radius * Math.sin(angle);
    return `translate(${x}, ${y})`;
    })
    .attr("text-anchor", "middle")
    .text(d => d.data.country)
    .attr("dy", "0.35em")
    .attr("dx", d => {
    const pos = arc.centroid(d);
    const angle = Math.atan2(pos[1], pos[0]);
    return Math.sign(pos[0]) * textOffset;
    });

    // Draw arrows
    arcs.append("line")
    .attr("x1", d => {
    const pos = arc.centroid(d);
    const angle = Math.atan2(pos[1], pos[0]);
    return radius * Math.cos(angle);
    })
    .attr("y1", d => {
    const pos = arc.centroid(d);
    const angle = Math.atan2(pos[1], pos[0]);
    return radius * Math.sin(angle);
    })
    .attr("x2", d => {
    const pos = arc.centroid(d);
    const angle = Math.atan2(pos[1], pos[0]);
    return (radius + textOffset) * Math.cos(angle);
    })
    .attr("y2", d => {
    const pos = arc.centroid(d);
    const angle = Math.atan2(pos[1], pos[0]);
    return (radius + textOffset) * Math.sin(angle);
    })
    .attr("stroke", "black");
    return
};

async function fetchData() {
    const response = await fetch('/api/data/chart1/');
    const data = await response.json();
    // Now you have your data and can pass it to a D3.js function to visualize
    await visualizeData(data);
}

fetchData();


