import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import DatasetTable from "../components/DatasetTable";
import { getDatasets } from "../services/api"; // Import the API service

const DataExplorer = () => {
  const [datasets, setDatasets] = useState([]); // State to store datasets
  const [filteredDatasets, setFilteredDatasets] = useState([]); // State to store filtered datasets
  const [loading, setLoading] = useState(true); // State to handle loading state
  const [error, setError] = useState(null); // State to handle errors

  // Fetch datasets from the backend on component mount
  useEffect(() => {
    const fetchDatasets = async () => {
      try {
        const data = await getDatasets(); // Fetch datasets using the API service
        setDatasets(data);
        setFilteredDatasets(data); // Initialize filtered datasets with all datasets
        setLoading(false);
      } catch (error) {
        console.error("Error fetching datasets:", error);
        setError("Failed to fetch datasets. Please try again later.");
        setLoading(false);
      }
    };

    fetchDatasets();
  }, []);

  // Handle search functionality
  const handleSearch = (query) => {
    if (!query) {
      // If the query is empty, show all datasets
      setFilteredDatasets(datasets);
    } else {
      // Filter datasets based on the search query
      const filtered = datasets.filter((dataset) =>
        dataset.name.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredDatasets(filtered);
    }
  };

  // Display loading state
  if (loading) {
    return (
      <div>
        <Header />
        <div className="container mx-auto p-4">
          <h1 className="text-2xl font-bold mb-4">Data Explorer</h1>
          <p>Loading datasets...</p>
        </div>
      </div>
    );
  }

  // Display error state
  if (error) {
    return (
      <div>
        <Header />
        <div className="container mx-auto p-4">
          <h1 className="text-2xl font-bold mb-4">Data Explorer</h1>
          <p className="text-red-500">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Header />
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Data Explorer</h1>
        <SearchBar onSearch={handleSearch} />
        {filteredDatasets.length > 0 ? (
          <DatasetTable datasets={filteredDatasets} />
        ) : (
          <p>No datasets found.</p>
        )}
      </div>
    </div>
  );
};

export default DataExplorer;