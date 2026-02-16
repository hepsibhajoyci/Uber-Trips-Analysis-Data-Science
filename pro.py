import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Config ────────────────────────────────────────────────────────────────────
FILE          = "uber65.csv"
ACCENT        = "#3B82F6"
WEEKDAY_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# ── Load & clean ──────────────────────────────────────────────────────────────
df = pd.read_csv(FILE)
df["DateTime"] = pd.to_datetime(
    df["DATE"].str.strip() + " " + df["TIME"].str.strip(),
    errors="coerce"
)
df.dropna(subset=["DateTime"], inplace=True)

df["Hour"]    = df["DateTime"].dt.hour
df["Month"]   = df["DateTime"].dt.month
df["Weekday"] = df["DateTime"].dt.day_name()

# Pre-compute aggregates ONCE (not repeatedly inside each plot)
hour_counts  = df["Hour"].value_counts().sort_index()
month_counts = df["Month"].value_counts().sort_index()
pivot = (
    df.groupby(["Weekday", "Hour"])
      .size()
      .unstack(fill_value=0)
      .reindex(WEEKDAY_ORDER)
)

total_trips = len(df)
peak_hour   = hour_counts.idxmax()
busiest_day = df["Weekday"].value_counts().idxmax()

# ── Dashboard ─────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", font_scale=0.9)
fig, axes = plt.subplots(3, 3, figsize=(20, 14))
fig.suptitle("Uber Trips Dashboard", fontsize=22, fontweight="bold", y=1.01)

# 1 – Bar Chart: Trips by Hour
ax = axes[0, 0]
sns.barplot(x=hour_counts.index, y=hour_counts.values, ax=ax,
            palette="Blues_d", hue=hour_counts.index, legend=False)
ax.set(title="Trips by Hour (Bar)", xlabel="Hour of Day", ylabel="Trip Count")
ax.tick_params(axis="x", rotation=45)

# 2 – Line Chart: Trips by Hour
ax = axes[0, 1]
ax.plot(hour_counts.index, hour_counts.values,
        color=ACCENT, linewidth=2.5, marker="o", markersize=4)
ax.fill_between(hour_counts.index, hour_counts.values, alpha=0.15, color=ACCENT)
ax.set(title="Trips by Hour (Line)", xlabel="Hour of Day", ylabel="Trip Count")

# 3 – Area Chart: Trips by Hour
ax = axes[0, 2]
GREEN = "#10B981"
ax.fill_between(hour_counts.index, hour_counts.values, alpha=0.55, color=GREEN)
ax.plot(hour_counts.index, hour_counts.values, color=GREEN, linewidth=1.5)
ax.set(title="Trips by Hour (Area)", xlabel="Hour of Day", ylabel="Trip Count")

# 4 – Pie Chart: Trips by Month
ax = axes[1, 0]
ax.pie(
    month_counts.values,
    labels=[f"Month {m}" for m in month_counts.index],
    autopct="%1.1f%%", startangle=140,
    colors=sns.color_palette("pastel", len(month_counts)),
)
ax.set_title("Trips by Month (Pie)")

# 5 – Donut Chart: Trips by Month
ax = axes[1, 1]
ax.pie(
    month_counts.values,
    labels=[f"Month {m}" for m in month_counts.index],
    wedgeprops=dict(width=0.45, edgecolor="white"),
    autopct="%1.1f%%", startangle=140,
    colors=sns.color_palette("Set2", len(month_counts)),
)
ax.set_title("Trips by Month (Donut)")

# 6 – Scatter Plot: Hour vs Month (low alpha reveals density)
ax = axes[1, 2]
ax.scatter(df["Hour"], df["Month"], alpha=0.04, s=8, color="#8B5CF6")
ax.set(title="Hour vs Month (Scatter)", xlabel="Hour of Day", ylabel="Month")
ax.set_yticks(sorted(df["Month"].unique()))

# 7 – Heatmap: Weekday × Hour
ax = axes[2, 0]
sns.heatmap(pivot, cmap="coolwarm", ax=ax, linewidths=0.3,
            cbar_kws={"shrink": 0.8})
ax.set(title="Heatmap: Weekday × Hour", xlabel="Hour of Day", ylabel="")

# 8 – Histogram: Hour Distribution
ax = axes[2, 1]
ax.hist(df["Hour"], bins=24, range=(0, 24),
        color="#F59E0B", edgecolor="white", linewidth=0.5)
ax.set(title="Hour Distribution (Histogram)", xlabel="Hour of Day", ylabel="Count")
ax.set_xticks(range(0, 24, 2))

# 9 – KPI Card
ax = axes[2, 2]
ax.axis("off")
kpis = [
    (0.78, "Total Trips",              13, "#6B7280", "normal"),
    (0.52, f"{total_trips:,}",         34, "#1D4ED8", "bold"),
    (0.30, f"Peak Hour: {peak_hour}:00", 11, "#374151", "normal"),
    (0.14, f"Busiest Day: {busiest_day}", 11, "#374151", "normal"),
]
for y, text, size, color, weight in kpis:
    ax.text(0.5, y, text, transform=ax.transAxes,
            ha="center", fontsize=size, color=color, fontweight=weight)

plt.tight_layout()
plt.savefig("uber_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("Dashboard saved to uber_dashboard.png")