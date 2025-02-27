import Home from "./pages/Home";
import DataExplorer from "./pages/DataExplorer";
import Visualizations from "./pages/Visualizations";

const routes = [
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/data-explorer",
    element: <DataExplorer />,
  },
  {
    path: "/visualizations",
    element: <Visualizations />,
  },
];

export default routes;