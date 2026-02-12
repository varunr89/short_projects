import { useCallback, useRef, useState } from "react";
import { CircleMarker, Popup, Tooltip } from "react-leaflet";
import { formatPrice } from "../utils/colorScale";
import { fetchDrivingTimes } from "../utils/routing";

function SalePopup({ sale }) {
  const [driving, setDriving] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const fetched = useRef(false);

  // Fetch driving times when popup opens (once)
  if (!fetched.current) {
    fetched.current = true;
    fetchDrivingTimes(sale.lat, sale.lng)
      .then((result) => {
        setDriving(result);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }

  return (
    <div style={{ minWidth: 180 }}>
      <strong>{formatPrice(sale.price)}</strong>
      <br />
      {sale.date}
      {sale.county && <> &middot; {sale.county} County</>}
      {sale.beds != null && (
        <>
          <br />
          {sale.beds} bed{sale.baths != null && <> / {sale.baths} bath</>}
        </>
      )}
      {sale.sqft != null && (
        <>
          <br />
          {sale.sqft.toLocaleString()} sqft
        </>
      )}
      {sale.yrBuilt != null && (
        <>
          <br />
          Built {sale.yrBuilt}
        </>
      )}

      <hr style={{ margin: "6px 0", borderColor: "#eee" }} />

      {loading && (
        <span style={{ color: "#999", fontSize: 12 }}>
          Calculating drive times...
        </span>
      )}
      {error && (
        <span style={{ color: "#c00", fontSize: 12 }}>
          Drive time unavailable
        </span>
      )}
      {driving && (
        <div style={{ fontSize: 12 }}>
          {driving.nearestGym && (
            <div>
              <span role="img" aria-label="climbing">&#x1F9D7;</span>{" "}
              <strong>{driving.nearestGym.minutes} min</strong> to{" "}
              {driving.nearestGym.name}
            </div>
          )}
          {driving.office && (
            <div>
              <span role="img" aria-label="office">&#x1F3E2;</span>{" "}
              <strong>{driving.office.minutes} min</strong> to Building 43
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function SalesLayer({ sales, getColor }) {
  return (
    <>
      {sales.map((sale, i) => (
        <CircleMarker
          key={i}
          center={[sale.lat, sale.lng]}
          radius={5}
          pathOptions={{
            fillColor: getColor(sale.price),
            fillOpacity: 0.7,
            color: "#333",
            weight: 0.5,
          }}
          eventHandlers={{
            click: () => {},
          }}
        >
          <Tooltip>
            <div>
              <strong>{formatPrice(sale.price)}</strong>
              {sale.county && <> &middot; {sale.county} Co.</>}
              {sale.beds != null && (
                <>
                  {" "}&middot; {sale.beds}bd
                </>
              )}
            </div>
          </Tooltip>
          <Popup>
            <SalePopup sale={sale} />
          </Popup>
        </CircleMarker>
      ))}
    </>
  );
}
