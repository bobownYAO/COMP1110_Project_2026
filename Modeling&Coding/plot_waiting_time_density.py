import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


REQUIRED_RAW_COLUMNS = {"restaurant", "final_wait_time"}
REQUIRED_RESTAURANT_COLUMNS = {"name", "strategy"}


def _validate_inputs(raw_data: pd.DataFrame, restaurant: pd.DataFrame) -> None:
    missing_raw = REQUIRED_RAW_COLUMNS - set(raw_data.columns)
    missing_restaurant = REQUIRED_RESTAURANT_COLUMNS - set(restaurant.columns)
    if missing_raw:
        raise ValueError(f"raw_data is missing columns: {sorted(missing_raw)}")
    if missing_restaurant:
        raise ValueError(f"restaurant is missing columns: {sorted(missing_restaurant)}")


def _gaussian_kde(values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    n = len(values)
    if n == 0:
        return np.array([])
    if n == 1:
        return np.zeros_like(grid)

    std = np.std(values, ddof=1)
    iqr = np.subtract(*np.percentile(values, [75, 25]))
    sigma = min(std, iqr / 1.34) if iqr > 0 else std
    if sigma <= 0:
        sigma = max(np.std(values), 1.0)

    bandwidth = 0.9 * sigma * (n ** (-1 / 5))
    bandwidth = max(float(bandwidth), 1e-3)

    density = np.zeros_like(grid, dtype=float)
    constant = 1 / (n * bandwidth * math.sqrt(2 * math.pi))
    for x in values:
        density += np.exp(-0.5 * ((grid - x) / bandwidth) ** 2)
    density *= constant
    return density


def plot_waiting_time_density(
    raw_data: pd.DataFrame,
    restaurant: pd.DataFrame,
    save_path: str | None = None,
):
    """
    Plot waiting-time density curves for each restaurant.
    Area under each curve is approximately 1.
    """
    _validate_inputs(raw_data, restaurant)

    restaurant_names = list(pd.unique(restaurant["name"]))
    plottable = []

    for r_name in restaurant_names:
        restaurant_sub = restaurant[restaurant["name"] == r_name].copy()
        wait_times = (
            raw_data.loc[raw_data["restaurant"] == r_name, "final_wait_time"]
            .dropna()
            .astype(float)
            .to_numpy()
        )
        if len(wait_times) > 0:
            plottable.append((r_name, restaurant_sub, wait_times))

    if not plottable:
        raise ValueError("No restaurant has enough waiting-time data to plot density curves.")

    fig, axes = plt.subplots(
        nrows=len(plottable),
        ncols=1,
        figsize=(12, 4.5 * len(plottable)),
        squeeze=False,
    )
    fig.suptitle("Waiting Time Density", fontsize=15, fontweight="bold")

    colors = plt.cm.tab10.colors

    for i, (r_name, restaurant_sub, wait_times) in enumerate(plottable):
        ax = axes[i][0]
        color = colors[i % len(colors)]
        strategy = restaurant_sub["strategy"].iloc[0]

        x_min = max(0.0, float(wait_times.min()) - 2.0)
        x_max = float(wait_times.max()) + 2.0
        grid = np.linspace(x_min, x_max, 400)

        if len(wait_times) == 1 or np.allclose(wait_times, wait_times[0]):
            ax.axvline(wait_times[0], linewidth=2, color=color,
                       label=f"Single wait time = {wait_times[0]:.1f}")
        else:
            density = _gaussian_kde(wait_times, grid)
            ax.plot(grid, density, linewidth=2, color=color)
            ax.fill_between(grid, density, alpha=0.18, color=color)

            mean_wait = float(np.mean(wait_times))
            ax.axvline(mean_wait, linestyle="--", linewidth=1.2, color=color,
                       alpha=0.8, label=f"Mean = {mean_wait:.2f} min")

        ax.set_title(
            f"{r_name} | Strategy: {strategy} | Sample size: {len(wait_times)}",
            fontsize=11,
            pad=8,
        )
        ax.set_xlabel("Waiting time (minutes)")
        ax.set_ylabel("Density")
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
