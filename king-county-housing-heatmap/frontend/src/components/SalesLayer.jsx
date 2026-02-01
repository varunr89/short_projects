import { CircleMarker, Tooltip } from "react-leaflet";
import { formatPrice } from "../utils/colorScale";

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
        >
          <Tooltip>
            <div>
              <strong>{formatPrice(sale.price)}</strong>
              <br />
              {sale.date}
            </div>
          </Tooltip>
        </CircleMarker>
      ))}
    </>
  );
}
