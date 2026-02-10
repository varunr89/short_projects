import { formatPrice } from "../utils/colorScale";

const COLORS = [
  "rgb(27, 120, 55)",
  "rgb(102, 189, 99)",
  "rgb(254, 224, 76)",
  "rgb(253, 141, 60)",
  "rgb(215, 48, 39)",
];

export default function Legend({ percentiles }) {
  if (!percentiles) return null;

  const breaks = ["0", "20", "40", "60", "80", "100"];

  return (
    <div
      style={{
        position: "absolute",
        bottom: 30,
        right: 10,
        background: "white",
        padding: "12px 16px",
        borderRadius: 8,
        boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
        zIndex: 1000,
        fontSize: 13,
      }}
    >
      <div style={{ fontWeight: "bold", marginBottom: 8 }}>Sale Price</div>
      {COLORS.map((color, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", marginBottom: 4 }}>
          <div
            style={{
              width: 20,
              height: 14,
              backgroundColor: color,
              marginRight: 8,
              borderRadius: 2,
            }}
          />
          <span>
            {formatPrice(percentiles[breaks[i]])} - {formatPrice(percentiles[breaks[i + 1]])}
          </span>
        </div>
      ))}
    </div>
  );
}
