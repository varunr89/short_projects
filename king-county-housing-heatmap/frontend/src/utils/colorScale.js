const COLORS = [
  [27, 120, 55],   // deep green — well below median
  [102, 189, 99],  // light green
  [254, 224, 76],  // yellow — at median
  [253, 141, 60],  // orange
  [215, 48, 39],   // red — well above median
];

// log2 range: -1.5 (0.35x median) to +1.5 (2.83x median)
const LOG_MIN = -1.5;
const LOG_MAX = 1.5;
const LOG_RANGE = LOG_MAX - LOG_MIN;

function interpolateColor(color1, color2, t) {
  return color1.map((c, i) => Math.round(c + (color2[i] - c) * t));
}

export function createColorScale(median) {
  return function getColor(price) {
    const logVal = Math.max(LOG_MIN, Math.min(LOG_MAX, Math.log2(price / median)));
    const norm = (logVal - LOG_MIN) / LOG_RANGE; // 0 to 1

    const segment = norm * (COLORS.length - 1);
    const i = Math.min(Math.floor(segment), COLORS.length - 2);
    const t = segment - i;

    const color = interpolateColor(COLORS[i], COLORS[i + 1], t);
    return `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
  };
}

export function getGradientCSS() {
  const stops = COLORS.map((c, i) => {
    const pct = (i / (COLORS.length - 1)) * 100;
    return `rgb(${c[0]}, ${c[1]}, ${c[2]}) ${pct}%`;
  });
  return `linear-gradient(to right, ${stops.join(", ")})`;
}

export { LOG_MIN, LOG_RANGE };

export function formatPrice(price) {
  if (price >= 1000000) return `$${(price / 1000000).toFixed(1)}M`;
  if (price >= 1000) return `$${(price / 1000).toFixed(0)}K`;
  return `$${price}`;
}
