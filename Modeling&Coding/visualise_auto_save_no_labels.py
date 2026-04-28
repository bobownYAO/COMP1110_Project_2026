import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, '/home/claude')
import io_file
import output_file


def plot_occupation(raw_data, restaurant, save_path="outputs/occupation_rate.png"):
    """
    For each restaurant in `restaurant`, compute the minute-by-minute
    occupation rate and draw it as a line graph.

    All restaurants are plotted on the SAME figure as separate subplots,
    one row per restaurant, so they are easy to compare.

    Parameters
    ----------
    raw_data    : customer DataFrame returned by io_file.package()
    restaurant  : restaurant DataFrame returned by io_file.read_file()
    save_path   : path used to save the figure automatically.
                  Default: outputs/occupation_rate.png
    """

    restaurant_names = restaurant["name"].unique()

    plottable = []
    for r_name in restaurant_names:
        res_sub = restaurant[restaurant["name"] == r_name]
        cus_sub = raw_data[raw_data["restaurant"] == r_name].copy()
        open_time = res_sub["open_time"].iloc[0]
        total_seats = output_file.f_total_seats(res_sub)
        avg_occ, occ_series = output_file.f_occupation_rate(cus_sub, total_seats, open_time)

        if not np.isnan(avg_occ):
            plottable.append((r_name, res_sub, cus_sub, total_seats,
                              open_time, avg_occ, occ_series))

    if not plottable:
        print("No plottable restaurants found (all customers unserved).")
        return

    n = len(plottable)
    fig, axes = plt.subplots(
        nrows=n, ncols=1,
        figsize=(12, 4.5 * n),
        squeeze=False
    )
    fig.suptitle("Restaurant Occupation Rate — Minute by Minute",
                 fontsize=15, fontweight="bold", y=1.01)

    colours = plt.cm.tab10.colors

    for i, (r_name, res_sub, cus_sub, total_seats,
            open_time, avg_occ, occ_series) in enumerate(plottable):

        ax = axes[i][0]
        colour = colours[i % len(colours)]

        strategy = res_sub["strategy"].iloc[0]
        table_summary = {
            row["table_size"]: int(row["table_number"])
            for _, row in res_sub.iterrows()
        }

        ax.step(occ_series.index, occ_series.values * 100,
                where="post",
                color=colour, linewidth=2,
                label="Occupation rate")

        ax.fill_between(occ_series.index, occ_series.values * 100,
                        step="post", alpha=0.15, color=colour)

        ax.axhline(avg_occ * 100, color=colour, linewidth=1.2,
                   linestyle="--", alpha=0.8,
                   label=f"Avg {avg_occ * 100:.1f}%")

        # Data-point labels and event-time vertical lines have been removed.
        # This keeps the chart clean, similar to the example image.

        ax.set_title(
            f"{r_name}  |  Strategy: {strategy}  |  "
            f"Tables: {table_summary}  →  {total_seats} seats",
            fontsize=11, pad=8
        )
        ax.set_xlabel("Time (minutes)", fontsize=10)
        ax.set_ylabel("Occupation Rate (%)", fontsize=10)
        ax.set_xlim(occ_series.index[0], occ_series.index[-1])
        ax.set_ylim(0, 110)
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
        ax.legend(fontsize=9, loc="upper right")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()

    # Automatically create the output folder and save the figure.
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved -> {save_path.resolve()}")


if __name__ == "__main__":
    filepath_restaurant = "/home/claude/testdata_restaurant.csv"
    filepath_customer = "/home/claude/testdata_customer.csv"

    restaurant, customer = io_file.read_file(
        filepath_restaurant, filepath_customer, random_state=0
    )
    raw_data = io_file.package(restaurant, customer)

    plot_occupation(raw_data, restaurant,
                    save_path="outputs/occupation_rate.png")
