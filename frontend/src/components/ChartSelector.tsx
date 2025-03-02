import React, { useState } from "react";
import BarChart from "./BarChart";
import PieChartComponent from "./Chart";

export default function ChartSelector({holdings, holdings2}) {

  const [selectedChart, setSelectedChart] = useState("bar");
  
  const handleSelectChange = (event) => {
    setSelectedChart(event.target.value);
  };

  // 4. Conditionally render the chart
  let chartComponent = null;
  if (selectedChart === "bar") {
    if (!holdings2) {
      return <div>No data available.</div>
    }
    chartComponent = <BarChart holdings={holdings2} />;
  } else if (selectedChart === "pie") {
    chartComponent = <PieChartComponent holdings={holdings}/>;
  }

  return (
    <div style={{ width: "500px", margin: "0 auto" }}>
      <h2>Chart Selector</h2>
      <select value={selectedChart} onChange={handleSelectChange}>
        <option value="bar">Bar Chart</option>
        <option value="pie">Holdings Distribution</option>
      </select>

      {/* Render the selected chart */}
      {chartComponent}
    </div>
  );
}
