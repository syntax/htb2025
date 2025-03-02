import React, { useState } from "react";
import BarChart from "./BarChart";
import PieChartComponent from "./Chart";
import KnnGraph from "./KnnChart";

export default function ChartSelector({holdings, holdings2, knndata}) {

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
    if (!holdings) {
      return <div>No data available.</div>
    }
    chartComponent = <PieChartComponent holdings={holdings}/>;
  } else if (selectedChart === "knn") {
    if (!knndata) {
      return <div>No data available.</div>
    }
    chartComponent = <KnnGraph coordinates={knndata} />;
  }

  return (
    <div style={{ width: "500px", margin: "0 auto" }}>
      <h2>Chart Selector</h2>
      <select value={selectedChart} onChange={handleSelectChange}>
        <option value="bar">Value Chart</option>
        <option value="pie">Holdings Distribution</option>
        <option value="knn">KNN Graph</option>
      </select>

      {/* Render the selected chart */}
      {chartComponent}
    </div>
  );
}
