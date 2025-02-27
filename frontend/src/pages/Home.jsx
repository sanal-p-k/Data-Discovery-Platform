import React from "react";
import Header from "../components/Header";

const Home = () => {
  return (
    <div>
      <Header />
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Welcome to the Data Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-4 shadow rounded">
            <h2 className="text-lg font-bold">Total Datasets</h2>
            <p className="text-3xl">123</p>
          </div>
          <div className="bg-white p-4 shadow rounded">
            <h2 className="text-lg font-bold">Total Users</h2>
            <p className="text-3xl">45</p>
          </div>
          <div className="bg-white p-4 shadow rounded">
            <h2 className="text-lg font-bold">Active Projects</h2>
            <p className="text-3xl">7</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;