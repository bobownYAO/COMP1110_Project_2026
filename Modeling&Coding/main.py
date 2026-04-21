import pandas as pd
import numpy as np

import io_file
import output_file
import visualise
import plot_table_utilization_line
import plot_table_utilization_bar
import plot_waiting_time_density
import plot_queue_length_over_time

def __main__():
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

    print("How will you load the data?\nA) from console, B) from csv file, C) by default")
    while 1:
        ans = input().strip().upper()
        if ans == "A":
            try:
                restaurant, customer = io_file.read_console(random_state)
            except ValueError as exc:
                print(f"Invalid console input: {exc}")
                continue
            break
        elif ans == "B" or ans == "C":
            filepath_restaurant = r"Project\github\COMP1110_Project_2026\Modeling&Coding\testdata_restaurant.csv"
            filepath_customer = r"Project/github/COMP1110_Project_2026/Modeling&Coding/testdata_customer.csv"
            if ans == "B":
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
    output_file.analysis(raw_data, restaurant, customer)

    visualise.plot_occupation(raw_data, restaurant)
    plot_table_utilization_line.plot_table_utilization_line(
        raw_data, restaurant, save_path="table_utilization_line.png"
    )

    plot_table_utilization_bar.plot_table_utilization_bar(
        raw_data, restaurant, save_path="table_utilization_bar.png"
    )

    plot_waiting_time_density.plot_waiting_time_density(
        raw_data, restaurant, save_path="waiting_time_density.png"
    )

    plot_queue_length_over_time.plot_queue_length_over_time(
        raw_data, restaurant, save_path="queue_length_over_time.png"
    )




__main__()
