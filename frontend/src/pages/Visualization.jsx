import React, { useState } from "react";
import Header from "../components/Header";
import Visualization from "../components/Visualization";

const Visualizations = () => {
  const [chartData, setChartData] = useState({
    labels: ["January", "February", "March", "April", "May"],
    values: [65, 59, 80, 81, 56],
  });

  return (
    <div>
      <Header />
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Visualizations</h1>
        <div className="bg-white p-4 shadow rounded">
          <h2 className="text-lg font-bold mb-4">Sales Data</h2>
          <Visualization data={chartData} />
        </div>
      </div>
    </div>
  );
};

export default Visualizations;