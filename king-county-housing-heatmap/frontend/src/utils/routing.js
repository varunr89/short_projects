import { CLIMBING_GYMS, MICROSOFT_B43 } from "../data/pois";

const OSRM_BASE = "https://router.project-osrm.org/table/v1/driving";

/**
 * Fetch driving durations from a point to all POIs using OSRM table API.
 * Returns { nearestGym: { name, minutes }, office: { name, minutes } }
 */
export async function fetchDrivingTimes(lat, lng) {
  const destinations = [
    ...CLIMBING_GYMS.map((g) => [g.lng, g.lat]),
    [MICROSOFT_B43.lng, MICROSOFT_B43.lat],
  ];

  // OSRM format: lng,lat;lng,lat;... source first, then destinations
  const coords = [[lng, lat], ...destinations]
    .map((c) => c.join(","))
    .join(";");

  const destIndices = destinations.map((_, i) => i + 1).join(";");
  const url = `${OSRM_BASE}/${coords}?sources=0&destinations=${destIndices}&annotations=duration`;

  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`OSRM error: ${resp.status}`);
  const data = await resp.json();

  if (data.code !== "Ok") throw new Error(`OSRM: ${data.code}`);

  const durations = data.durations[0]; // single source row

  // Find nearest climbing gym
  const gymDurations = CLIMBING_GYMS.map((g, i) => ({
    name: g.name,
    seconds: durations[i],
  }));
  const nearestGym = gymDurations
    .filter((g) => g.seconds != null)
    .sort((a, b) => a.seconds - b.seconds)[0];

  // Microsoft Building 43 is the last destination
  const officeSeconds = durations[durations.length - 1];

  return {
    nearestGym: nearestGym
      ? { name: nearestGym.name, minutes: Math.round(nearestGym.seconds / 60) }
      : null,
    office: officeSeconds != null
      ? { name: MICROSOFT_B43.name, minutes: Math.round(officeSeconds / 60) }
      : null,
  };
}
