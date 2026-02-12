import { MapContainer, TileLayer } from "react-leaflet";
import POILayer from "./POILayer";
import SalesLayer from "./SalesLayer";
import HexLayer from "./HexLayer";
import "leaflet/dist/leaflet.css";

const MAP_CENTER = [47.65, -122.2];
const DEFAULT_ZOOM = 9;

// Prevent panning/zooming beyond King + Snohomish County area
const MAX_BOUNDS = [
  [46.9, -123.0], // SW corner (with padding)
  [48.5, -121.1], // NE corner (with padding)
];

export default function Map({ sales, getColor, viewMode }) {
  return (
    <MapContainer
      center={MAP_CENTER}
      zoom={DEFAULT_ZOOM}
      minZoom={9}
      maxZoom={18}
      maxBounds={MAX_BOUNDS}
      maxBoundsViscosity={1.0}
      style={{ width: "100%", height: "100vh" }}
      preferCanvas={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />
      {sales && viewMode === "hex" && <HexLayer sales={sales} getColor={getColor} />}
      {sales && viewMode === "points" && <SalesLayer sales={sales} getColor={getColor} />}
      <POILayer />
    </MapContainer>
  );
}
