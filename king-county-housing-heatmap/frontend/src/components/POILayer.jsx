import { CircleMarker, Tooltip } from "react-leaflet";
import { ALL_POIS } from "../data/pois";

const STYLES = {
  gym: { fillColor: "#16a34a", color: "#15803d", emoji: "\u{1F9D7}" },
  office: { fillColor: "#7c3aed", color: "#6d28d9", emoji: "\u{1F3E2}" },
};

export default function POILayer() {
  return (
    <>
      {ALL_POIS.map((poi) => {
        const s = STYLES[poi.type];
        return (
          <CircleMarker
            key={poi.name}
            center={[poi.lat, poi.lng]}
            radius={8}
            pathOptions={{
              fillColor: s.fillColor,
              fillOpacity: 0.9,
              color: s.color,
              weight: 2,
            }}
          >
            <Tooltip>
              <strong>
                {s.emoji} {poi.name}
              </strong>
            </Tooltip>
          </CircleMarker>
        );
      })}
    </>
  );
}
