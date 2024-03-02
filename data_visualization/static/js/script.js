const CHARTS_CONFIG = [
    {chartName: "1", endPoint: "/api/data/chart1/", func: visualizeDonutChart, elementName: "#chart1"},
    {chartName: "2", endPoint: "/api/data/chart2/", func: visualizeBarChart, elementName: "#chart2"},
    {chartName: "3", endPoint: "/api/data/chart3/", func: visualizePieChart, elementName: "#chart3"},
    {chartName: "4", endPoint: "/api/data/chart4/", func: visualizeGroupedBarChart, elementName: "#chart4"},
    {chartName: "5", endPoint: "/api/data/chart5/", func: visualizeMapChart, elementName: "#chart5"},
    {chartName: "6", endPoint: "/api/data/chart6/", func: visualizeLineChart, elementName: "#chart6"},
    {chartName: "7", endPoint: "/api/data/chart7/", func: visualizeLineChart, elementName: "#chart7"},
    {chartName: "8", endPoint: "/api/data/chart8/", func: visualizeBarChart, elementName: "#chart8"},
    {chartName: "9", endPoint: "/api/data/chart9/", func: visualizeBarChart, elementName: "#chart9"},
    {chartName: "10", endPoint: "/api/data/chart10/", func: visualizeBarChart, elementName: "#chart10"},
    {chartName: "11", endPoint: "/api/data/chart11/", func: visualizeBarChart, elementName: "#chart11"},
    {chartName: "12", endPoint: "/api/data/chart12/", func: visualizeBarChart, elementName: "#chart12"}
]

async function showEmptyOnChart(elementName){
    const svgWidth = 400;
    const svgHeight = 300;

    const svg = d3.select(elementName)
        .attr("width", svgWidth)
        .attr("height", svgHeight)

    svg.append("text")
        .attr("x", svgWidth / 2)
        .attr("y", svgHeight / 2)
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "middle")
        .attr("font-size", 30)
        .text("No Data Available");
    return
}

async function fetchDataAndRenderChart(url, func, elementName) {
    const response = await fetch(url);
    const data = await response.json();
    // Now you have your data and can pass it to a D3.js function to visualize
    if ($.isEmptyObject(data)){
        await showEmptyOnChart(elementName);
    } else {
        await func(data, elementName);
    }
}

async function renderAllCharts(urlParams){
    for (let chart_config of CHARTS_CONFIG){
        if (urlParams){
            await fetchDataAndRenderChart(`${chart_config.endPoint}?${urlParams}`, chart_config.func, chart_config.elementName)
        } else {
            await fetchDataAndRenderChart(chart_config.endPoint, chart_config.func, chart_config.elementName)
        }
    }
}

renderAllCharts();


// add filter callback
async function cleanUpD3(){
    d3.selectAll("svg")
    .attr("width", null)
    .attr("height", null)
    .attr("viewBox", null)
    .attr("style", null)
    .selectAll("*").remove();
    return
}

function getSelectedValues(){
    selectedValues = {}
    const filters = document.querySelectorAll("select");
    filters.forEach(filter => {
        if (filter.value !== "All"){
            selectedValues[filter.name] = filter.value
        }
    })
    return selectedValues
}

function serializeFilters(selectedValues){
    return Object.keys(selectedValues)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(selectedValues[key])}`)
        .join('&');
}

const filters = document.querySelectorAll(".filter");

filters.forEach(filter => {
    filter.addEventListener("change", async function(event){
        const selectedOption = event.target.value;

        //TODO: update other filter values

        // get all filter values, send api then render the chart
        const selectedValues = getSelectedValues();
        await cleanUpD3();
        await renderAllCharts(serializeFilters(selectedValues));
    })
})
