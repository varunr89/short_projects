import { useMemo, useState } from "react";
import { Polygon, Tooltip, Popup } from "react-leaflet";
import { cellToBoundary } from "h3-js";
import { formatPrice } from "../utils/colorScale";

function computeMedian(values) {
  if (values.length === 0) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function computePercentile(sorted, p) {
  if (sorted.length === 0) return 0;
  const idx = (p / 100) * (sorted.length - 1);
  const lo = Math.floor(idx);
  const hi = Math.ceil(idx);
  if (lo === hi) return sorted[lo];
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo);
}

function HexPopup({ hexId, sales }) {
  const prices = sales.map((s) => s.price).sort((a, b) => a - b);
  const p25 = computePercentile(prices, 25);
  const p75 = computePercentile(prices, 75);
  const median = computePercentile(prices, 50);

  // Bedroom histogram
  const bedCounts = {};
  sales.forEach((s) => {
    if (s.beds != null) {
      const key = s.beds >= 5 ? "5+" : String(s.beds);
      bedCounts[key] = (bedCounts[key] || 0) + 1;
    }
  });

  // Sqft stats
  const sqfts = sales.filter((s) => s.sqft != null).map((s) => s.sqft).sort((a, b) => a - b);
  // Year built range
  const years = sales.filter((s) => s.yrBuilt != null).map((s) => s.yrBuilt).sort((a, b) => a - b);

  // Drive times (from first sale -- all in same hex should be similar)
  const driveGym = sales.find((s) => s.driveGym != null)?.driveGym;
  const driveOffice = sales.find((s) => s.driveOffice != null)?.driveOffice;
  const nearestGymName = sales.find((s) => s.nearestGymName)?.nearestGymName;

  // Sort by date descending for recent sales
  const recentSales = [...sales].sort((a, b) => b.date.localeCompare(a.date));

  return (
    <div style={{ minWidth: 260, maxHeight: 400, overflowY: "auto", fontSize: 13 }}>
      <div style={{ fontWeight: 600, marginBottom: 6 }}>
        {sales.length} sale{sales.length !== 1 ? "s" : ""} in this area
      </div>

      <div style={{ marginBottom: 6 }}>
        <div>
          <strong>Price:</strong> {formatPrice(median)} median
        </div>
        <div style={{ color: "#666", fontSize: 12 }}>
          {formatPrice(p25)} (25th) &ndash; {formatPrice(p75)} (75th)
        </div>
        <div style={{ color: "#666", fontSize: 12 }}>
          Range: {formatPrice(prices[0])} &ndash; {formatPrice(prices[prices.length - 1])}
        </div>
      </div>

      {Object.keys(bedCounts).length > 0 && (
        <div style={{ marginBottom: 6 }}>
          <strong>Beds:</strong>{" "}
          {Object.entries(bedCounts)
            .sort(([a], [b]) => a.localeCompare(b, undefined, { numeric: true }))
            .map(([bed, count]) => `${bed}bd(${count})`)
            .join(", ")}
        </div>
      )}

      {sqfts.length > 0 && (
        <div style={{ marginBottom: 6, fontSize: 12, color: "#666" }}>
          <strong style={{ color: "#333" }}>Sqft:</strong>{" "}
          {computePercentile(sqfts, 25).toLocaleString()} &ndash;{" "}
          {computePercentile(sqfts, 75).toLocaleString()}
          {years.length > 0 && (
            <>
              {" | "}
              <strong style={{ color: "#333" }}>Built:</strong> {years[0]} &ndash;{" "}
              {years[years.length - 1]}
            </>
          )}
        </div>
      )}

      {(driveGym != null || driveOffice != null) && (
        <div style={{ marginBottom: 6 }}>
          {driveGym != null && (
            <div>
              <span role="img" aria-label="climbing">&#x1F9D7;</span>{" "}
              <strong>{driveGym} min</strong>
              {nearestGymName && <> to {nearestGymName}</>}
            </div>
          )}
          {driveOffice != null && (
            <div>
              <span role="img" aria-label="office">&#x1F3E2;</span>{" "}
              <strong>{driveOffice} min</strong> to Building 43
            </div>
          )}
        </div>
      )}

      <hr style={{ margin: "8px 0", borderColor: "#eee" }} />
      <div style={{ fontSize: 11, color: "#999", marginBottom: 4 }}>Recent sales:</div>
      {recentSales.map((s, i) => (
        <div
          key={i}
          style={{
            fontSize: 12,
            padding: "3px 0",
            borderBottom: i < recentSales.length - 1 ? "1px solid #f0f0f0" : "none",
          }}
        >
          <strong>{formatPrice(s.price)}</strong>
          {s.beds != null && <> &middot; {s.beds}bd</>}
          {s.sqft != null && <> &middot; {s.sqft.toLocaleString()}sf</>}
          {s.yrBuilt != null && <> &middot; {s.yrBuilt}</>}
          <span style={{ color: "#999" }}> &middot; {s.date}</span>
        </div>
      ))}
    </div>
  );
}

export default function HexLayer({ sales, getColor }) {
  const hexGroups = useMemo(() => {
    const groups = {};
    for (const sale of sales) {
      if (!sale.h3) continue;
      if (!groups[sale.h3]) groups[sale.h3] = [];
      groups[sale.h3].push(sale);
    }
    return groups;
  }, [sales]);

  const hexData = useMemo(() => {
    return Object.entries(hexGroups).map(([hexId, hexSales]) => {
      const medianPrice = computeMedian(hexSales.map((s) => s.price));
      const boundary = cellToBoundary(hexId);
      return { hexId, boundary, medianPrice, count: hexSales.length };
    });
  }, [hexGroups]);

  return (
    <>
      {hexData.map(({ hexId, boundary, medianPrice, count }) => (
        <Polygon
          key={hexId}
          positions={boundary}
          pathOptions={{
            fillColor: getColor(medianPrice),
            fillOpacity: Math.min(0.85, 0.4 + count * 0.05),
            color: "#666",
            weight: 0.5,
          }}
        >
          <Tooltip>
            <div>
              <strong>{formatPrice(medianPrice)}</strong> median &middot; {count} sale
              {count !== 1 ? "s" : ""}
            </div>
          </Tooltip>
          <Popup maxWidth={320}>
            <HexPopup hexId={hexId} sales={hexGroups[hexId]} />
          </Popup>
        </Polygon>
      ))}
    </>
  );
}
