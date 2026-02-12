import { useEffect, useMemo, useState } from "react";
import Map from "./components/Map";
import Legend from "./components/Legend";
import FilterPanel from "./components/FilterPanel";
import { createColorScale } from "./utils/colorScale";

function getDefaultFilters(ranges) {
  if (!ranges) return null;
  return {
    beds: [],
    price: [ranges.price.min, ranges.price.max],
    sqft: [ranges.sqft.min, ranges.sqft.max],
    yrBuilt: [ranges.yrBuilt.min, ranges.yrBuilt.max],
    maxDriveGym: ranges.driveGym ? ranges.driveGym.max : null,
    maxDriveOffice: ranges.driveOffice ? ranges.driveOffice.max : null,
  };
}

function applyFilters(sales, filters) {
  if (!filters) return sales;

  const buildingFilterActive =
    filters.beds.length > 0 ||
    filters.sqft[0] !== filters._ranges.sqft.min ||
    filters.sqft[1] !== filters._ranges.sqft.max ||
    filters.yrBuilt[0] !== filters._ranges.yrBuilt.min ||
    filters.yrBuilt[1] !== filters._ranges.yrBuilt.max;

  const driveGymActive = filters.maxDriveGym != null &&
    filters._ranges.driveGym &&
    filters.maxDriveGym < filters._ranges.driveGym.max;
  const driveOfficeActive = filters.maxDriveOffice != null &&
    filters._ranges.driveOffice &&
    filters.maxDriveOffice < filters._ranges.driveOffice.max;

  return sales.filter((s) => {
    if (s.price < filters.price[0] || s.price > filters.price[1]) return false;

    if (buildingFilterActive) {
      if (s.beds == null || s.sqft == null) return false;

      if (filters.beds.length > 0) {
        const match = filters.beds.includes(5) ? s.beds >= 5 || filters.beds.includes(s.beds) : filters.beds.includes(s.beds);
        if (!match) return false;
      }

      if (s.sqft < filters.sqft[0] || s.sqft > filters.sqft[1]) return false;
      if (s.yrBuilt != null && (s.yrBuilt < filters.yrBuilt[0] || s.yrBuilt > filters.yrBuilt[1])) return false;
    }

    if (driveGymActive) {
      if (s.driveGym == null || s.driveGym > filters.maxDriveGym) return false;
    }
    if (driveOfficeActive) {
      if (s.driveOffice == null || s.driveOffice > filters.maxDriveOffice) return false;
    }

    return true;
  });
}

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState(null);
  const [viewMode, setViewMode] = useState("hex");

  useEffect(() => {
    fetch("./sales_data.json")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        setData(json);
        const ranges = json.stats.filterRanges;
        if (ranges) {
          setFilters({ ...getDefaultFilters(ranges), _ranges: ranges });
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const filteredSales = useMemo(() => {
    if (!data) return [];
    return applyFilters(data.sales, filters);
  }, [data, filters]);

  const median = useMemo(() => {
    if (filteredSales.length === 0) return 0;
    const prices = filteredSales.map((s) => s.price).sort((a, b) => a - b);
    return prices[Math.floor(prices.length / 2)];
  }, [filteredSales]);

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

  const getColor = createColorScale(median);
  const ranges = data.stats.filterRanges;
  const isFiltered = filteredSales.length !== data.sales.length;

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
        <strong>King &amp; Snohomish County Housing Sales</strong>
        <span style={{ marginLeft: 12, color: "#666" }}>
          {isFiltered
            ? `${filteredSales.length.toLocaleString()} of ${data.stats.count.toLocaleString()} sales (filtered)`
            : `${data.stats.count.toLocaleString()} sales`}
          {" | Generated "}
          {data.generated}
        </span>
        <span
          style={{
            marginLeft: 12,
            display: "inline-flex",
            borderRadius: 4,
            overflow: "hidden",
            border: "1px solid #ccc",
            fontSize: 12,
          }}
        >
          {["hex", "points"].map((mode) => (
            <button
              key={mode}
              onClick={() => setViewMode(mode)}
              style={{
                padding: "3px 10px",
                border: "none",
                background: viewMode === mode ? "#2563eb" : "white",
                color: viewMode === mode ? "white" : "#333",
                cursor: "pointer",
                fontWeight: viewMode === mode ? 600 : 400,
              }}
            >
              {mode === "hex" ? "Hex" : "Points"}
            </button>
          ))}
        </span>
        {ranges && (
          <FilterPanel
            filters={filters}
            onChange={(f) => setFilters({ ...f, _ranges: ranges })}
            ranges={ranges}
          />
        )}
      </div>
      <Map sales={filteredSales} getColor={getColor} viewMode={viewMode} />
      <Legend median={median} />
    </div>
  );
}
