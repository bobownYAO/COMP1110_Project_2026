import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib

matplotlib.use("Agg")

import io_file
import output_file
import plot_occupation
import plot_table_utilization_line
import plot_table_utilization_bar
import plot_waiting_time_density
import plot_queue_length_over_time

def __main__():
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    print("Dinning time predicting model?\nA) Random, B) Fixed")
    while 1:
        ans = input().strip().upper()
        if ans == "A":
            random_state=1
            break
        elif ans == "B":
            random_state=0
            break
        else:
            print("Invalid input! Please type again.")

    print("How will you load the data?\nA) from console, B) from csv file")
    while 1:
        ans = input().strip().upper()
        if ans == "A":
            try:
                restaurant, customer = io_file.read_console(random_state)
            except ValueError as exc:
                print(f"Invalid console input: {exc}")
                continue
            break
        elif ans == "B":
            filepath_restaurant = input("Enter restaurant CSV path: ").strip()
            filepath_customer = input("Enter customer CSV path: ").strip()
            try:
                restaurant, customer = io_file.read_file(filepath_restaurant, filepath_customer, random_state)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Failed to read CSV files: {exc}")
                continue
            break
        else:
            print("Invalid input! Please type again.")

    print("Loading complete!\n")
    print(f"Preview:\n{restaurant.head()}")
    print(f"Preview:\n{customer.head()}")

    raw_data=io_file.package(restaurant, customer)
    summary = output_file.analysis(raw_data, restaurant, customer)
    summary_path = output_dir / "summary_metrics_by_restaurant.csv"
    summary.to_csv(summary_path, index=False)
    print(f"Summary metrics saved -> {summary_path}")

    plot_occupation.plot_occupation(raw_data, restaurant, save_path=str(output_dir / "occupation_rate.png"))
    plot_table_utilization_line.plot_table_utilization_line(
        raw_data, restaurant, save_path=str(output_dir / "table_utilization_line.png")
    )

    plot_table_utilization_bar.plot_table_utilization_bar(
        raw_data, restaurant, save_path=str(output_dir / "table_utilization_bar.png")
    )

    plot_waiting_time_density.plot_waiting_time_density(
        raw_data, restaurant, save_path=str(output_dir / "waiting_time_density.png")
    )

    plot_queue_length_over_time.plot_queue_length_over_time(
        raw_data, restaurant, save_path=str(output_dir / "queue_length_over_time.png")
    )




if __name__ == "__main__":
    __main__()
