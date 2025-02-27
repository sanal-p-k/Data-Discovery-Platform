import React from "react";

const DatasetTable = ({ datasets }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Name</th>
            <th className="p-2 border">Description</th>
            <th className="p-2 border">Created At</th>
          </tr>
        </thead>
        <tbody>
          {datasets.map((dataset) => (
            <tr key={dataset.id} className="hover:bg-gray-50">
              <td className="p-2 border">{dataset.id}</td>
              <td className="p-2 border">{dataset.name}</td>
              <td className="p-2 border">{dataset.description}</td>
              <td className="p-2 border">{dataset.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DatasetTable;