import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


TABLE_TYPES = ("A", "B", "C")
REQUIRED_RAW_COLUMNS = {
    "restaurant", "number", "start_service_time", "leave_time"
}
REQUIRED_RESTAURANT_COLUMNS = {"name", "strategy", "open_time", "table_size", "table_number"}


def _validate_inputs(raw_data: pd.DataFrame, restaurant: pd.DataFrame) -> None:
    missing_raw = REQUIRED_RAW_COLUMNS - set(raw_data.columns)
    missing_restaurant = REQUIRED_RESTAURANT_COLUMNS - set(restaurant.columns)
    if missing_raw:
        raise ValueError(f"raw_data is missing columns: {sorted(missing_raw)}")
    if missing_restaurant:
        raise ValueError(f"restaurant is missing columns: {sorted(missing_restaurant)}")


def _assigned_table_type(group_size: int) -> str:
    if group_size <= 2:
        return "A"
    if group_size <= 4:
        return "B"
    return "C"


def _average_utilization_by_table_type(
    restaurant_sub: pd.DataFrame,
    customer_sub: pd.DataFrame,
) -> dict[str, float]:
    served = customer_sub.dropna(subset=["start_service_time", "leave_time"]).copy()
    if served.empty:
        return {}

    if "assigned_table_type" in served.columns and served["assigned_table_type"].notna().any():
        served["table_type_used"] = served["assigned_table_type"]
        missing_table_type = served["table_type_used"].isna()
        served.loc[missing_table_type, "table_type_used"] = (
            served.loc[missing_table_type, "number"].astype(int).map(_assigned_table_type)
        )
    else:
        served["table_type_used"] = served["number"].astype(int).map(_assigned_table_type)
    table_counts = {
        row["table_size"]: int(row["table_number"])
        for _, row in restaurant_sub.iterrows()
    }

    t_start = int(restaurant_sub["open_time"].iloc[0])
    t_end = int(served["leave_time"].max())
    minutes = list(range(t_start, t_end + 1))

    result = {}
    for table_type in TABLE_TYPES:
        total_tables = int(table_counts.get(table_type, 0))
        if total_tables <= 0:
            result[table_type] = np.nan
            continue

        rates = []
        type_rows = served[served["table_type_used"] == table_type]
        for t in minutes:
            occupied = ((type_rows["start_service_time"] <= t) & (type_rows["leave_time"] > t)).sum()
            rates.append(occupied / total_tables)
        result[table_type] = float(np.mean(rates)) if rates else 0.0

    return result


def plot_table_utilization_bar(
    raw_data: pd.DataFrame,
    restaurant: pd.DataFrame,
    save_path: str | None = None,
):
    """
    Plot average table utilization by table type (A/B/C) as a bar chart.
    This complements the time-series utilization chart.
    """
    _validate_inputs(raw_data, restaurant)

    restaurant_names = list(pd.unique(restaurant["name"]))
    plottable = []

    for r_name in restaurant_names:
        restaurant_sub = restaurant[restaurant["name"] == r_name].copy()
        customer_sub = raw_data[raw_data["restaurant"] == r_name].copy()
        avg_by_type = _average_utilization_by_table_type(restaurant_sub, customer_sub)
        if avg_by_type:
            plottable.append((r_name, restaurant_sub, avg_by_type))

    if not plottable:
        raise ValueError("No restaurant has enough served-customer data to plot bar utilization.")

    fig, axes = plt.subplots(
        nrows=len(plottable),
        ncols=1,
        figsize=(10, 4.5 * len(plottable)),
        squeeze=False,
    )
    fig.suptitle("Average Table Utilization by Table Type", fontsize=15, fontweight="bold")

    colors = plt.cm.tab10.colors

    for i, (r_name, restaurant_sub, avg_by_type) in enumerate(plottable):
        ax = axes[i][0]
        strategy = restaurant_sub["strategy"].iloc[0]

        x_positions = np.arange(len(TABLE_TYPES))
        values = [avg_by_type.get(table_type, np.nan) for table_type in TABLE_TYPES]
        bar_colors = [colors[j % len(colors)] for j in range(len(TABLE_TYPES))]
        bars = ax.bar(x_positions, np.nan_to_num(values, nan=0.0) * 100, color=bar_colors, width=0.6)

        for bar, value in zip(bars, values):
            label = "N/A" if np.isnan(value) else f"{value * 100:.1f}%"
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 2,
                label,
                ha="center",
                va="bottom",
                fontsize=9,
            )
            if np.isnan(value):
                bar.set_alpha(0.35)

        ax.set_title(f"{r_name} | Strategy: {strategy}", fontsize=11, pad=8)
        ax.set_xlabel("Table type")
        ax.set_ylabel("Average utilization (%)")
        ax.set_xticks(x_positions)
        ax.set_xticklabels(TABLE_TYPES)
        ax.set_ylim(0, 110)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
        ax.grid(axis="y", linestyle="--", alpha=0.35)
        ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Chart saved -> {save_path}")
    else:
        plt.show()

    return fig, axes
