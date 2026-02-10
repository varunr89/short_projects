import { useEffect, useState } from "react";
import Map from "./components/Map";
import Legend from "./components/Legend";
import { createColorScale } from "./utils/colorScale";

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/sales_data.json")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
        Loading sales data...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", color: "red" }}>
        Error loading data: {error}
      </div>
    );
  }

  const getColor = createColorScale(data.stats.percentiles);

  return (
    <div style={{ position: "relative" }}>
      <div
        style={{
          position: "absolute",
          top: 10,
          left: 60,
          zIndex: 1000,
          background: "white",
          padding: "8px 16px",
          borderRadius: 8,
          boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
          fontSize: 14,
        }}
      >
        <strong>King County Housing Sales</strong>
        <span style={{ marginLeft: 12, color: "#666" }}>
          {data.stats.count.toLocaleString()} sales | Generated {data.generated}
        </span>
      </div>
      <Map sales={data.sales} getColor={getColor} />
      <Legend percentiles={data.stats.percentiles} />
    </div>
  );
}
