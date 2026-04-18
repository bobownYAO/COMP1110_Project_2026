import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


REQUIRED_RAW_COLUMNS = {"restaurant", "arrival_time", "start_service_time", "leave_time"}
REQUIRED_RESTAURANT_COLUMNS = {"name", "strategy", "open_time"}


def _validate_inputs(raw_data: pd.DataFrame, restaurant: pd.DataFrame) -> None:
    missing_raw = REQUIRED_RAW_COLUMNS - set(raw_data.columns)
    missing_restaurant = REQUIRED_RESTAURANT_COLUMNS - set(restaurant.columns)
    if missing_raw:
        raise ValueError(f"raw_data is missing columns: {sorted(missing_raw)}")
    if missing_restaurant:
        raise ValueError(f"restaurant is missing columns: {sorted(missing_restaurant)}")


def _build_queue_length_series(
    restaurant_sub: pd.DataFrame,
    customer_sub: pd.DataFrame,
) -> pd.Series:
    if customer_sub.empty:
        return pd.Series(dtype=float, name="queue_length")

    t_start = int(min(restaurant_sub["open_time"].iloc[0], customer_sub["arrival_time"].min()))

    leave_max = customer_sub["leave_time"].dropna()
    start_max = customer_sub["start_service_time"].dropna()
    arrival_max = customer_sub["arrival_time"].max()
    candidates = [arrival_max]
    if not start_max.empty:
        candidates.append(start_max.max())
    if not leave_max.empty:
        candidates.append(leave_max.max())
    t_end = int(max(candidates))

    minutes = list(range(t_start, t_end + 1))
    queue_lengths = []

    for t in minutes:
        arrived = customer_sub["arrival_time"] <= t
        not_started_yet = customer_sub["start_service_time"].isna() | (customer_sub["start_service_time"] > t)
        queue_lengths.append(int((arrived & not_started_yet).sum()))

    return pd.Series(queue_lengths, index=minutes, name="queue_length")


def plot_queue_length_over_time(
    raw_data: pd.DataFrame,
    restaurant: pd.DataFrame,
    save_path: str | None = None,
):
    """
    Plot queue length over time as a step chart.
    y-axis = number of waiting customer groups.
    """
    _validate_inputs(raw_data, restaurant)

    restaurant_names = list(pd.unique(restaurant["name"]))
    plottable = []

    for r_name in restaurant_names:
        restaurant_sub = restaurant[restaurant["name"] == r_name].copy()
        customer_sub = raw_data[raw_data["restaurant"] == r_name].copy()
        series = _build_queue_length_series(restaurant_sub, customer_sub)
        if not series.empty:
            plottable.append((r_name, restaurant_sub, series))

    if not plottable:
        raise ValueError("No restaurant has enough data to plot queue length over time.")

    fig, axes = plt.subplots(
        nrows=len(plottable),
        ncols=1,
        figsize=(12, 4.5 * len(plottable)),
        squeeze=False,
    )
    fig.suptitle("Queue Length Over Time", fontsize=15, fontweight="bold")

    colors = plt.cm.tab10.colors

    for i, (r_name, restaurant_sub, series) in enumerate(plottable):
        ax = axes[i][0]
        color = colors[i % len(colors)]
        strategy = restaurant_sub["strategy"].iloc[0]

        ax.step(series.index, series.values, where="post", linewidth=2, color=color, label="Queue length")
        ax.fill_between(series.index, series.values, step="post", alpha=0.15, color=color)
        ax.axhline(series.mean(), linestyle="--", linewidth=1.2, color=color,
                   alpha=0.8, label=f"Average = {series.mean():.2f}")

        ax.set_title(f"{r_name} | Strategy: {strategy}", fontsize=11, pad=8)
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Waiting groups")
        ax.set_xlim(series.index[0], series.index[-1])
        ax.set_ylim(0, max(1, series.max() + 1))
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
