import { MapContainer, TileLayer } from "react-leaflet";
import SalesLayer from "./SalesLayer";
import "leaflet/dist/leaflet.css";

const KC_CENTER = [47.5, -122.2];
const DEFAULT_ZOOM = 10;

export default function Map({ sales, getColor }) {
  return (
    <MapContainer
      center={KC_CENTER}
      zoom={DEFAULT_ZOOM}
      style={{ width: "100%", height: "100vh" }}
      preferCanvas={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />
      {sales && <SalesLayer sales={sales} getColor={getColor} />}
    </MapContainer>
  );
}
