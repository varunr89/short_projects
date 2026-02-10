const COLORS = [
  [27, 120, 55],
  [102, 189, 99],
  [254, 224, 76],
  [253, 141, 60],
  [215, 48, 39],
];

function interpolateColor(color1, color2, t) {
  return color1.map((c, i) => Math.round(c + (color2[i] - c) * t));
}

export function createColorScale(percentiles) {
  const breaks = [
    percentiles["0"],
    percentiles["20"],
    percentiles["40"],
    percentiles["60"],
    percentiles["80"],
    percentiles["100"],
  ];

  return function getColor(price) {
    for (let i = 0; i < breaks.length - 1; i++) {
      if (price <= breaks[i + 1]) {
        const t = (price - breaks[i]) / (breaks[i + 1] - breaks[i] || 1);
        const color = i < COLORS.length - 1
          ? interpolateColor(COLORS[i], COLORS[i + 1], t)
          : COLORS[COLORS.length - 1];
        return `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
      }
    }
    return `rgb(${COLORS[COLORS.length - 1].join(", ")})`;
  };
}

export function formatPrice(price) {
  if (price >= 1000000) return `$${(price / 1000000).toFixed(1)}M`;
  if (price >= 1000) return `$${(price / 1000).toFixed(0)}K`;
  return `$${price}`;
}
