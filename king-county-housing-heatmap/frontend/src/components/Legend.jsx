import { formatPrice, getGradientCSS, LOG_MIN, LOG_RANGE } from "../utils/colorScale";

const TICKS = [
  { ratio: 0.5, label: "0.5x" },
  { ratio: 1, label: "1x" },
  { ratio: 2, label: "2x" },
];

export default function Legend({ median }) {
  if (!median) return null;

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
        width: 220,
      }}
    >
      <div style={{ fontWeight: "bold", marginBottom: 8 }}>
        Price vs Median ({formatPrice(median)})
      </div>
      <div
        style={{
          height: 14,
          borderRadius: 2,
          background: getGradientCSS(),
        }}
      />
      <div style={{ position: "relative", height: 32, marginTop: 4 }}>
        {TICKS.map(({ ratio, label }) => {
          const pct = ((Math.log2(ratio) - LOG_MIN) / LOG_RANGE) * 100;
          return (
            <div
              key={ratio}
              style={{
                position: "absolute",
                left: `${pct}%`,
                transform: "translateX(-50%)",
                textAlign: "center",
                lineHeight: 1.2,
              }}
            >
              <div style={{ fontSize: 11, color: "#333" }}>{label}</div>
              <div style={{ fontSize: 10, color: "#888" }}>
                {formatPrice(Math.round(median * ratio))}
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ fontSize: 10, color: "#999", marginTop: 2 }}>
        Below median &larr; &rarr; Above median
      </div>
    </div>
  );
}
