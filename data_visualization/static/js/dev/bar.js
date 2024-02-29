async function visualizeData(data){

    const DUMMY_DATA = [
        { id: 'd1', value: 10, region: 'USA' },
        { id: 'd2', value: 11, region: 'India' },
        { id: 'd3', value: 12, region: 'China' },
        { id: 'd4', value: 6, region: 'Germany' },
    ];

    const CHART_WIDTH = 600;
    const CHART_HEIGHT = 400;

    const x = d3.scaleBand().rangeRound([0, CHART_WIDTH]).padding(0.1); // equally sized items across x axis, 10% space is reserved for padding
    const y = d3.scaleLinear().range([CHART_HEIGHT, 0]);

    // put real data into the scaled axises
    x.domain(DUMMY_DATA.map(data => data.region));
    y.domain([0, d3.max(DUMMY_DATA, data => data.value) + 3]);

    // x, y are the mapper from real value to axis

    const chartContainer = d3.select('svg')
        .attr("width", CHART_WIDTH)
        .attr("height", CHART_HEIGHT);

    const chart = chartContainer.append("g");

    // add axises
    chart.append('g').call(d3.axisBottom())
    //
    chart.selectAll(".bar")
        .data(DUMMY_DATA) // join data
        .enter() // enter missing data
        .append("rect") // svg element
        .classed('bar', true) // add bar class to the rect eleemtn
        .attr("width", x.bandwidth()) // no hardcoded, use d3 scale instead
        .attr("height", data => CHART_HEIGHT - y(data.value)) // start from top left corner
        .attr("x", data => x(data.region))
        .attr("y", data => y(data.value));

    // add label to the bar
    chart.selectAll(".label")
        .data(DUMMY_DATA)
        .enter()
        .append("text")
        .text(data => data.value)
        .attr('x', data => x(data.region) + x.bandwidth() / 2)
        .attr('y', data => y(data.value) - 20)
        .attr("text-anchor", "middle")
        .classed("label", true);
};

async function fetchData() {
    const response = await fetch('/api/data/chart1/');
    const data = await response.json();
    // Now you have your data and can pass it to a D3.js function to visualize
    await visualizeData(data);
}

fetchData();


