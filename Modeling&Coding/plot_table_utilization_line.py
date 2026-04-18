import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


REQUIRED_RAW_COLUMNS = {
    "restaurant", "arrival_time", "start_service_time", "leave_time"
}
REQUIRED_RESTAURANT_COLUMNS = {"name", "strategy", "open_time", "table_number"}


def _validate_inputs(raw_data: pd.DataFrame, restaurant: pd.DataFrame) -> None:
    missing_raw = REQUIRED_RAW_COLUMNS - set(raw_data.columns)
    missing_restaurant = REQUIRED_RESTAURANT_COLUMNS - set(restaurant.columns)
    if missing_raw:
        raise ValueError(f"raw_data is missing columns: {sorted(missing_raw)}")
    if missing_restaurant:
        raise ValueError(f"restaurant is missing columns: {sorted(missing_restaurant)}")


def _build_table_utilization_series(
    restaurant_sub: pd.DataFrame,
    customer_sub: pd.DataFrame,
) -> pd.Series:
    served = customer_sub.dropna(subset=["start_service_time", "leave_time"]).copy()
    if served.empty:
        return pd.Series(dtype=float, name="table_utilization_rate")

    total_tables = int(restaurant_sub["table_number"].sum())
    if total_tables <= 0:
        return pd.Series(dtype=float, name="table_utilization_rate")

    t_start = int(restaurant_sub["open_time"].iloc[0])
    t_end = int(served["leave_time"].max())
    minutes = list(range(t_start, t_end + 1))

    utilization = []
    for t in minutes:
        occupied_tables = ((served["start_service_time"] <= t) & (served["leave_time"] > t)).sum()
        utilization.append(occupied_tables / total_tables)

    return pd.Series(utilization, index=minutes, name="table_utilization_rate")


def plot_table_utilization_line(
    raw_data: pd.DataFrame,
    restaurant: pd.DataFrame,
    save_path: str | None = None,
):
    """
    Plot minute-by-minute table utilization rate as a line/step chart.

    Parameters
    ----------
    raw_data : DataFrame
        Customer-level output containing at least:
        restaurant, arrival_time, start_service_time, leave_time.
    restaurant : DataFrame
        Restaurant configuration containing at least:
        name, strategy, open_time, table_number.
    save_path : str | None
        Save figure when provided. Otherwise show the figure.
    """
    _validate_inputs(raw_data, restaurant)

    restaurant_names = list(pd.unique(restaurant["name"]))
    plottable = []

    for r_name in restaurant_names:
        restaurant_sub = restaurant[restaurant["name"] == r_name].copy()
        customer_sub = raw_data[raw_data["restaurant"] == r_name].copy()
        series = _build_table_utilization_series(restaurant_sub, customer_sub)
        if not series.empty:
            plottable.append((r_name, restaurant_sub, series))

    if not plottable:
        raise ValueError("No restaurant has enough served-customer data to plot table utilization.")

    fig, axes = plt.subplots(
        nrows=len(plottable),
        ncols=1,
        figsize=(12, 4.5 * len(plottable)),
        squeeze=False,
    )
    fig.suptitle("Table Utilization Rate Over Time", fontsize=15, fontweight="bold")

    colors = plt.cm.tab10.colors

    for i, (r_name, restaurant_sub, series) in enumerate(plottable):
        ax = axes[i][0]
        color = colors[i % len(colors)]
        strategy = restaurant_sub["strategy"].iloc[0]
        total_tables = int(restaurant_sub["table_number"].sum())
        avg_rate = float(series.mean())

        ax.step(series.index, series.values * 100, where="post", linewidth=2, color=color)
        ax.fill_between(series.index, series.values * 100, step="post", alpha=0.15, color=color)
        ax.axhline(avg_rate * 100, linestyle="--", linewidth=1.2, color=color, alpha=0.8,
                   label=f"Average = {avg_rate * 100:.1f}%")

        ax.set_title(
            f"{r_name} | Strategy: {strategy} | Total tables: {total_tables}",
            fontsize=11,
            pad=8,
        )
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Table utilization (%)")
        ax.set_xlim(series.index[0], series.index[-1])
        ax.set_ylim(0, 110)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
        ax.grid(axis="y", linestyle="--", alpha=0.35)
        ax.legend(loc="upper right", fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Chart saved -> {save_path}")
    else:
        plt.show()

    return fig, axes
