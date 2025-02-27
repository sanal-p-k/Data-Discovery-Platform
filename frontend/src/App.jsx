import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";
import DataExplorer from "./pages/DataExplorer";
import Visualizations from "./pages/Visualizations";

const App = () => {
  return (
    <Router>
      <div>
        <Header />
        <div className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/data-explorer" element={<DataExplorer />} />
            <Route path="/visualizations" element={<Visualizations />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;