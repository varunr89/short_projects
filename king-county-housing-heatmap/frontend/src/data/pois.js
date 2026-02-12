export const CLIMBING_GYMS = [
  { name: "Edgeworks Bellevue", lat: 47.6195, lng: -122.1302 },
  { name: "Edgeworks Seattle", lat: 47.6680, lng: -122.3953 },
  { name: "Vertical World Seattle", lat: 47.6610, lng: -122.3865 },
  { name: "Vertical World North", lat: 47.8688, lng: -122.2981 },
  { name: "Uplift Shoreline", lat: 47.7548, lng: -122.3143 },
  { name: "Momentum SODO", lat: 47.5781, lng: -122.3348 },
  { name: "SBP Poplar", lat: 47.5936, lng: -122.3109 },
  { name: "SBP Fremont", lat: 47.6502, lng: -122.3418 },
];

export const MICROSOFT_B43 = {
  name: "Microsoft Building 43",
  lat: 47.6395,
  lng: -122.1344,
};

export const ALL_POIS = [
  ...CLIMBING_GYMS.map((g) => ({ ...g, type: "gym" })),
  { ...MICROSOFT_B43, type: "office" },
];
