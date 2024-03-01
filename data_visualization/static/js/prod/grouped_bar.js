async function visualizeGroupedBarChart(data, element){
    // Specify the chart’s dimensions.
    const width = 600;
    const height = 500;
    const marginTop = 10;
    const marginRight = 10;
    const marginBottom = 20;
    const marginLeft = 40;

    // const data = [
    //     {country: "CA", category: "<10", count: 5038433},
    //     {country: "TX", category: "<10", count: 3983091},
    //     {country: "CA", category: "10-19", count: 5170341}
    // ]

    // Prepare the scales for positional and color encodings.
    // Fx encodes the country.
    const fx = d3.scaleBand()
        .domain(new Set(data.map(d => d.country)))
        .rangeRound([marginLeft, width - marginRight])
        .paddingInner(0.1);

    // Both x and color encode the category class.
    const categorys = new Set(data.map(d => d.category));
    console.log("category.size: ", categorys.size)
    console.log("d3.schemeSpectral[categorys.size]: ", d3.schemeSpectral[categorys.size])

    const x = d3.scaleBand()
        .domain(categorys)
        .rangeRound([0, fx.bandwidth()])
        .padding(0.05);

    const color = d3.scaleOrdinal(d3.schemeSpectral)
        .domain(categorys)
        .range(["#ca0020","#f4a582","#d5d5d5","#92c5de","#0571b0", "#0571b0"])
        .unknown("#ccc");

    // Y encodes the height of the bar.
    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)]).nice()
        .rangeRound([height - marginBottom, marginTop]);

    // A function to format the value in the tooltip.
    const formatValue = x => isNaN(x) ? "N/A" : x.toLocaleString("en")

    // Create the SVG container.
    const svg = d3.select(element)
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: auto;");

    // Append a group for each country, and a rect for each category.
    svg.append("g")
      .selectAll()
      .data(d3.group(data, d => d.country))
      .join("g")
        .attr("transform", ([country]) => `translate(${fx(country)},0)`)
      .selectAll()
      .data(([, d]) => d)
      .join("rect")
        .attr("x", d => x(d.category))
        .attr("y", d => y(d.value))
        .attr("width", x.bandwidth())
        .attr("height", d => y(0) - y(d.value))
        .attr("fill", d => color(d.category));

    // Append the horizontal axis.
    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(fx).tickSizeOuter(0))
        .call(g => g.selectAll(".domain").remove());

    // Append the vertical axis.
    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).ticks(null, "s"))
        .call(g => g.selectAll(".domain").remove());

    //Legend

    // Return the chart with the color scale as a property (for the legend).
    return Object.assign(svg.node(), {scales: {color}});
  }