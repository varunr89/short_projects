#!/usr/bin/env python3
"""
GitHub Outage Trend Analysis

Generates charts exploring:
1. Incidents per year (bar chart)
2. Incidents per quarter (line chart, to see acceleration)
3. Impact severity distribution over time
4. Major/critical incidents over time
5. Incidents by component category over time
6. Average incident duration by year
7. Monthly incident frequency heatmap
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
from pathlib import Path

DATA = Path(__file__).parent.parent / "data" / "github_incidents_clean.csv"
CHARTS = Path(__file__).parent.parent / "charts"
CHARTS.mkdir(exist_ok=True)

# Style -- sized for blog column (~672px wide, rendered at 2x for retina)
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("deep")
FIGSIZE = (8, 4.5)
DPI = 170
plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
})

# Load data
df = pd.read_csv(DATA)
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce")
df["year"] = df["start_date"].dt.year
df["quarter"] = df["start_date"].dt.to_period("Q")
df["year_month"] = df["start_date"].dt.to_period("M")

# Filter to complete years for fair comparison (2014-2025)
df_full = df[(df["year"] >= 2014) & (df["year"] <= 2025)].copy()

print(f"Total incidents: {len(df)}")
print(f"Date range: {df['start_date'].min()} to {df['start_date'].max()}")
print(f"Full years (2014-2025): {len(df_full)}")
print()

# ── Chart 1: Incidents per year ──────────────────────────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE)
yearly = df_full.groupby("year").size()
colors = ["#2563eb" if y < 2022 else "#dc2626" for y in yearly.index]
bars = ax.bar(yearly.index, yearly.values, color=colors, edgecolor="white", linewidth=0.5)

# Add count labels on bars
for bar, val in zip(bars, yearly.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            str(val), ha="center", va="bottom", fontsize=11, fontweight="bold")

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of Incidents", fontsize=12)
ax.set_title("GitHub Status Incidents Per Year (2014-2025)", fontsize=14, fontweight="bold")
ax.set_xticks(yearly.index)

# Product launch annotations
milestones = [
    (2019, "Actions GA\n(Nov 2019)", "#e36209"),
    (2021, "Codespaces GA\n(Aug 2021)", "#28a745"),
    (2022, "Copilot GA\n(Jun 2022)", "#6f42c1"),
    (2025, "Core Azure\nmigration\n(Oct 2025)", "#0366d6"),
]
for yr, label, color in milestones:
    ax.annotate(label, xy=(yr, yearly.get(yr, 0)),
                xytext=(yr, yearly.get(yr, 0) + 20),
                fontsize=7, ha="center", fontweight="bold", color=color,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2))

ax.set_ylim(0, max(yearly.values) + 55)
plt.tight_layout()
plt.savefig(CHARTS / "01_incidents_per_year.png", dpi=DPI)
plt.close()
print("Saved 01_incidents_per_year.png")


# ── Chart 2: Quarterly trend ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE)
quarterly = df_full.groupby("quarter").size()
x_labels = [str(q) for q in quarterly.index]
ax.plot(range(len(quarterly)), quarterly.values, marker="o", markersize=4,
        linewidth=1.5, color="#2563eb", alpha=0.8)

# Add rolling average
if len(quarterly) >= 4:
    rolling = quarterly.rolling(4).mean()
    ax.plot(range(len(rolling)), rolling.values, linewidth=2.5, color="#dc2626",
            label="4-quarter rolling avg", alpha=0.9)

ax.set_xticks(range(0, len(x_labels), 4))
ax.set_xticklabels([x_labels[i] for i in range(0, len(x_labels), 4)], rotation=45, ha="right")
ax.set_ylabel("Incidents per Quarter", fontsize=12)
ax.set_title("GitHub Incidents by Quarter (2014-2025)", fontsize=14, fontweight="bold")
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(CHARTS / "02_quarterly_trend.png", dpi=DPI)
plt.close()
print("Saved 02_quarterly_trend.png")


# ── Chart 3: Impact severity over time (stacked bar) ────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE)
severity_order = ["critical", "major", "minor", "none", "maintenance"]
severity_colors = {"critical": "#991b1b", "major": "#dc2626", "minor": "#f59e0b",
                   "none": "#6b7280", "maintenance": "#3b82f6"}
pivot = df_full.pivot_table(index="year", columns="impact", aggfunc="size", fill_value=0)
# Reorder columns
pivot = pivot.reindex(columns=[c for c in severity_order if c in pivot.columns])
pivot.plot(kind="bar", stacked=True, ax=ax,
           color=[severity_colors[c] for c in pivot.columns], edgecolor="white", linewidth=0.5)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of Incidents", fontsize=12)
ax.set_title("Incident Severity Distribution by Year", fontsize=14, fontweight="bold")
ax.legend(title="Impact", fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig(CHARTS / "03_severity_by_year.png", dpi=DPI)
plt.close()
print("Saved 03_severity_by_year.png")


# ── Chart 4: Major + Critical incidents over time ────────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE)
serious = df_full[df_full["impact"].isin(["major", "critical"])].copy()
serious_yearly = serious.groupby("year").size()
# Also show total as reference
total_yearly = df_full.groupby("year").size()
ax.bar(total_yearly.index, total_yearly.values, color="#d1d5db", label="All incidents", edgecolor="white")
ax.bar(serious_yearly.index, serious_yearly.values, color="#dc2626", label="Major/Critical", edgecolor="white")
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of Incidents", fontsize=12)
ax.set_title("Major & Critical Incidents vs Total (2014-2025)", fontsize=14, fontweight="bold")
ax.set_xticks(total_yearly.index)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(CHARTS / "04_major_critical_vs_total.png", dpi=DPI)
plt.close()
print("Saved 04_major_critical_vs_total.png")


# ── Chart 5: Top components over time ────────────────────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE)
top_components = df_full["component"].value_counts().head(8).index.tolist()
comp_yearly = df_full[df_full["component"].isin(top_components)].pivot_table(
    index="year", columns="component", aggfunc="size", fill_value=0
)
comp_yearly = comp_yearly[top_components]  # preserve order
comp_yearly.plot(kind="bar", ax=ax, edgecolor="white", linewidth=0.5)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of Incidents", fontsize=12)
ax.set_title("Incidents by Component Category (Top 8)", fontsize=14, fontweight="bold")
ax.legend(title="Component", fontsize=9, ncol=2)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig(CHARTS / "05_components_over_time.png", dpi=DPI)
plt.close()
print("Saved 05_components_over_time.png")


# ── Chart 6: Average incident duration by year ───────────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE)
duration_df = df_full[df_full["duration_minutes"] > 0].copy()
dur_stats = duration_df.groupby("year")["duration_minutes"].agg(["median", "mean", "count"])

ax.bar(dur_stats.index, dur_stats["median"], color="#2563eb", alpha=0.8, label="Median duration")
ax.plot(dur_stats.index, dur_stats["mean"], color="#dc2626", marker="o", linewidth=2,
        label="Mean duration")
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Duration (minutes)", fontsize=12)
ax.set_title("Incident Duration by Year (median bar, mean line)", fontsize=14, fontweight="bold")
ax.set_xticks(dur_stats.index)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(CHARTS / "06_duration_by_year.png", dpi=DPI)
plt.close()
print("Saved 06_duration_by_year.png")


# ── Chart 7: Monthly heatmap ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 6))
df_full["month_num"] = df_full["start_date"].dt.month
heatmap_data = df_full.pivot_table(index="month_num", columns="year", aggfunc="size", fill_value=0)
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
heatmap_data.index = [month_labels[i-1] for i in heatmap_data.index]
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlOrRd", ax=ax,
            linewidths=0.5, linecolor="white")
ax.set_title("Monthly Incident Heatmap (2014-2025)", fontsize=14, fontweight="bold")
ax.set_ylabel("Month", fontsize=12)
ax.set_xlabel("Year", fontsize=12)
plt.tight_layout()
plt.savefig(CHARTS / "07_monthly_heatmap.png", dpi=DPI)
plt.close()
print("Saved 07_monthly_heatmap.png")


# ── Chart 8: New components (Copilot, Actions, Codespaces) emergence ─────

fig, ax = plt.subplots(figsize=FIGSIZE)
ai_components = ["Copilot", "Actions", "Codespaces"]
ai_df = df_full[df_full["component"].isin(ai_components)]
ai_yearly = ai_df.pivot_table(index="year", columns="component", aggfunc="size", fill_value=0)
for comp in ai_components:
    if comp not in ai_yearly.columns:
        ai_yearly[comp] = 0
ai_yearly = ai_yearly[ai_components]
ai_yearly.plot(kind="bar", ax=ax, edgecolor="white", linewidth=0.5)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of Incidents", fontsize=12)
ax.set_title("AI-Era Services: Copilot, Actions & Codespaces Incidents", fontsize=14, fontweight="bold")
ax.legend(fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
plt.tight_layout()
plt.savefig(CHARTS / "08_ai_services_trend.png", dpi=DPI)
plt.close()
print("Saved 08_ai_services_trend.png")


# ── Chart 9: Annotated quarterly timeline with all key events ────────────

fig, ax = plt.subplots(figsize=(10, 5))
quarterly = df_full.groupby("quarter").size()
x_vals = range(len(quarterly))
x_labels = [str(q) for q in quarterly.index]

# Plot quarterly counts
ax.fill_between(x_vals, quarterly.values, alpha=0.3, color="#2563eb")
ax.plot(x_vals, quarterly.values, marker="o", markersize=3, linewidth=1.2, color="#2563eb")

# Rolling average
if len(quarterly) >= 4:
    rolling = quarterly.rolling(4).mean()
    ax.plot(x_vals, rolling.values, linewidth=2.5, color="#dc2626", label="4-quarter rolling avg")

# Key events to annotate (quarter_label, text, color)
events = [
    ("2018Q4", "Microsoft\nacquires\nGitHub", "#6f42c1"),
    ("2019Q4", "Actions\nGA", "#e36209"),
    ("2021Q3", "Codespaces\nGA", "#28a745"),
    ("2022Q2", "Copilot\nGA", "#6f42c1"),
    ("2024Q1", "Actions+Copilot\nfully on Azure", "#0366d6"),
    ("2025Q1", "Pages+Packages\non Azure", "#0366d6"),
    ("2025Q4", "Core migration\nbegins (Oct)", "#dc2626"),
]

for evt_q, evt_label, evt_color in events:
    if evt_q in x_labels:
        idx = x_labels.index(evt_q)
        yval = quarterly.iloc[idx]
        ax.annotate(evt_label, xy=(idx, yval),
                    xytext=(idx, yval + 16),
                    fontsize=7, ha="center", fontweight="bold", color=evt_color,
                    arrowprops=dict(arrowstyle="-|>", color=evt_color, lw=1.2),
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                              edgecolor=evt_color, alpha=0.9))

ax.set_xticks(range(0, len(x_labels), 4))
ax.set_xticklabels([x_labels[i] for i in range(0, len(x_labels), 4)], rotation=45, ha="right")
ax.set_ylabel("Incidents per Quarter", fontsize=12)
ax.set_title("GitHub Incidents Timeline with Key Product & Infrastructure Events",
             fontsize=14, fontweight="bold")
ax.set_ylim(0, max(quarterly.values) + 35)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(CHARTS / "09_annotated_timeline.png", dpi=DPI)
plt.close()
print("Saved 09_annotated_timeline.png")


# ── Summary stats ────────────────────────────────────────────────────────

print("\n=== Summary Statistics ===")
print(f"\nIncidents per year:")
for year in sorted(df_full["year"].unique()):
    subset = df_full[df_full["year"] == year]
    major = len(subset[subset["impact"].isin(["major", "critical"])])
    med_dur = subset["duration_minutes"].median()
    print(f"  {year}: {len(subset):4d} total, {major:3d} major/critical, "
          f"median duration: {med_dur:.0f} min")

print(f"\nTop components (all time):")
for comp, count in df_full["component"].value_counts().head(10).items():
    print(f"  {comp}: {count}")
