import { MapContainer, TileLayer } from "react-leaflet";
import POILayer from "./POILayer";
import SalesLayer from "./SalesLayer";
import HexLayer from "./HexLayer";
import "leaflet/dist/leaflet.css";

const MAP_CENTER = [47.65, -122.2];
const DEFAULT_ZOOM = 9;

export default function Map({ sales, getColor, viewMode }) {
  return (
    <MapContainer
      center={MAP_CENTER}
      zoom={DEFAULT_ZOOM}
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
