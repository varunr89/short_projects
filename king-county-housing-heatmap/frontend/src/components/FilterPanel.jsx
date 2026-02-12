import { useEffect, useRef, useState } from "react";

const dropdownStyle = {
  position: "absolute",
  top: "100%",
  left: 0,
  marginTop: 4,
  background: "white",
  borderRadius: 8,
  boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
  fontSize: 13,
  width: 260,
  padding: "8px 12px 12px",
};

const labelStyle = {
  fontWeight: 600,
  marginBottom: 4,
  marginTop: 10,
  fontSize: 12,
  color: "#555",
};

const bedBtnStyle = (active) => ({
  padding: "4px 10px",
  border: "1px solid #ccc",
  borderRadius: 4,
  background: active ? "#2563eb" : "white",
  color: active ? "white" : "#333",
  cursor: "pointer",
  fontSize: 12,
  fontWeight: active ? 600 : 400,
});

const rangeRowStyle = {
  display: "flex",
  alignItems: "center",
  gap: 6,
  marginBottom: 2,
};

const inputStyle = {
  width: 90,
  padding: "4px 6px",
  border: "1px solid #ccc",
  borderRadius: 4,
  fontSize: 12,
  textAlign: "right",
};

function RangeInputs({ label, min, max, value, onChange, format, parse }) {
  const fmt = format || ((v) => String(v));
  const prs = parse || ((v) => Number(v.replace(/[^0-9.-]/g, "")));
  const [localMin, setLocalMin] = useState(fmt(value[0]));
  const [localMax, setLocalMax] = useState(fmt(value[1]));

  // Sync local state when value prop changes externally (e.g. reset)
  useEffect(() => {
    setLocalMin(fmt(value[0]));
    setLocalMax(fmt(value[1]));
  }, [value[0], value[1]]);

  const commitMin = () => {
    const num = prs(localMin);
    if (!isNaN(num)) {
      const clamped = Math.max(min, Math.min(num, value[1]));
      onChange([clamped, value[1]]);
      setLocalMin(fmt(clamped));
    } else {
      setLocalMin(fmt(value[0]));
    }
  };

  const commitMax = () => {
    const num = prs(localMax);
    if (!isNaN(num)) {
      const clamped = Math.min(max, Math.max(num, value[0]));
      onChange([value[0], clamped]);
      setLocalMax(fmt(clamped));
    } else {
      setLocalMax(fmt(value[1]));
    }
  };

  const handleKey = (commit) => (e) => {
    if (e.key === "Enter") commit();
  };

  return (
    <div>
      <div style={labelStyle}>{label}</div>
      <div style={rangeRowStyle}>
        <input
          type="text"
          inputMode="numeric"
          style={inputStyle}
          value={localMin}
          onChange={(e) => setLocalMin(e.target.value)}
          onBlur={commitMin}
          onKeyDown={handleKey(commitMin)}
        />
        <span style={{ color: "#999", fontSize: 12 }}>to</span>
        <input
          type="text"
          inputMode="numeric"
          style={inputStyle}
          value={localMax}
          onChange={(e) => setLocalMax(e.target.value)}
          onBlur={commitMax}
          onKeyDown={handleKey(commitMax)}
        />
      </div>
    </div>
  );
}

function MaxDriveInput({ label, emoji, max, value, onChange }) {
  const [local, setLocal] = useState(String(value));

  useEffect(() => {
    setLocal(String(value));
  }, [value]);

  const commit = () => {
    const num = Number(local);
    if (!isNaN(num) && num > 0) {
      onChange(Math.min(num, max));
      setLocal(String(Math.min(num, max)));
    } else {
      setLocal(String(value));
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter") commit();
  };

  return (
    <div>
      <div style={labelStyle}>{emoji} {label}</div>
      <div style={rangeRowStyle}>
        <span style={{ color: "#999", fontSize: 12 }}>max</span>
        <input
          type="text"
          inputMode="numeric"
          style={{ ...inputStyle, width: 60 }}
          value={local}
          onChange={(e) => setLocal(e.target.value)}
          onBlur={commit}
          onKeyDown={handleKey}
        />
        <span style={{ color: "#999", fontSize: 12 }}>min</span>
      </div>
    </div>
  );
}

export default function FilterPanel({ filters, onChange, ranges }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    if (!open) return;
    const handleClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [open]);

  if (!ranges) return null;

  const hasDriveTimes = ranges.driveGym != null;

  const isDefault =
    filters.beds.length === 0 &&
    filters.price[0] === ranges.price.min &&
    filters.price[1] === ranges.price.max &&
    filters.sqft[0] === ranges.sqft.min &&
    filters.sqft[1] === ranges.sqft.max &&
    filters.yrBuilt[0] === ranges.yrBuilt.min &&
    filters.yrBuilt[1] === ranges.yrBuilt.max &&
    (!hasDriveTimes || filters.maxDriveGym === ranges.driveGym.max) &&
    (!hasDriveTimes || filters.maxDriveOffice === ranges.driveOffice.max);

  const handleReset = () => {
    onChange({
      beds: [],
      price: [ranges.price.min, ranges.price.max],
      sqft: [ranges.sqft.min, ranges.sqft.max],
      yrBuilt: [ranges.yrBuilt.min, ranges.yrBuilt.max],
      maxDriveGym: hasDriveTimes ? ranges.driveGym.max : null,
      maxDriveOffice: hasDriveTimes ? ranges.driveOffice.max : null,
    });
  };

  const toggleBed = (val) => {
    const next = filters.beds.includes(val)
      ? filters.beds.filter((v) => v !== val)
      : [...filters.beds, val];
    onChange({ ...filters, beds: next });
  };

  const bedValues = [1, 2, 3, 4, 5];
  const bedLabels = ["1", "2", "3", "4", "5+"];

  return (
    <span
      ref={ref}
      style={{ position: "relative", marginLeft: 12 }}
    >
      <span
        onClick={() => setOpen(!open)}
        style={{
          cursor: "pointer",
          color: isDefault ? "#666" : "#2563eb",
          fontWeight: isDefault ? 400 : 600,
          borderBottom: "1px dashed currentColor",
        }}
      >
        {isDefault ? "Filters \u25BC" : "Filtered \u25BC"}
      </span>
      {open && (
        <div style={dropdownStyle}>
          <div style={{ ...labelStyle, marginTop: 0 }}>Bedrooms</div>
          <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
            <button
              style={bedBtnStyle(filters.beds.length === 0)}
              onClick={() => onChange({ ...filters, beds: [] })}
            >
              All
            </button>
            {bedValues.map((val, i) => (
              <button
                key={val}
                style={bedBtnStyle(filters.beds.includes(val))}
                onClick={() => toggleBed(val)}
              >
                {bedLabels[i]}
              </button>
            ))}
          </div>

          <RangeInputs
            label="Price"
            min={ranges.price.min}
            max={ranges.price.max}
            value={filters.price}
            onChange={(price) => onChange({ ...filters, price })}
            format={(v) => "$" + v.toLocaleString()}
            parse={(v) => Number(v.replace(/[^0-9]/g, ""))}
          />

          <RangeInputs
            label="Square Footage"
            min={ranges.sqft.min}
            max={ranges.sqft.max}
            value={filters.sqft}
            onChange={(sqft) => onChange({ ...filters, sqft })}
            format={(v) => v.toLocaleString()}
            parse={(v) => Number(v.replace(/[^0-9]/g, ""))}
          />

          <RangeInputs
            label="Year Built"
            min={ranges.yrBuilt.min}
            max={ranges.yrBuilt.max}
            value={filters.yrBuilt}
            onChange={(yrBuilt) => onChange({ ...filters, yrBuilt })}
          />

          {hasDriveTimes && (
            <>
              <MaxDriveInput
                label="Drive to closest gym"
                emoji="&#x1F9D7;"
                max={ranges.driveGym.max}
                value={filters.maxDriveGym}
                onChange={(v) => onChange({ ...filters, maxDriveGym: v })}
              />
              <MaxDriveInput
                label="Drive to Building 43"
                emoji="&#x1F3E2;"
                max={ranges.driveOffice.max}
                value={filters.maxDriveOffice}
                onChange={(v) => onChange({ ...filters, maxDriveOffice: v })}
              />
            </>
          )}

          {!isDefault && (
            <button
              onClick={handleReset}
              style={{
                marginTop: 12,
                width: "100%",
                padding: "6px 0",
                border: "1px solid #ccc",
                borderRadius: 4,
                background: "#f5f5f5",
                cursor: "pointer",
                fontSize: 12,
              }}
            >
              Reset All
            </button>
          )}
        </div>
      )}
    </span>
  );
}
