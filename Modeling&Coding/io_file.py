import pandas as pd
import numpy as np

import strategy_vip
import strategy_single_snake
import strategy_size_base

#load data
def read_file(filepath_restaurant,filepath_customer,random_state):
    try:
        restaurant = pd.read_csv(filepath_restaurant)
        customer = pd.read_csv(filepath_customer)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {exc.filename}") from exc
    except pd.errors.ParserError as exc:
        raise ValueError("Input CSV format is invalid.") from exc

    return data_process(restaurant,customer, random_state)


def read_console(random_state):
    restaurant_columns = ["name", "strategy", "open_time", "table_size", "table_number"]
    customer_columns = ["index", "restaurant", "vip", "number", "arrival_time"]

    def _read_rows(prompt, columns):
        rows = []
        print(prompt)
        print("Use comma-separated values and type DONE on a new line to finish.")
        print("Expected format: " + ", ".join(columns))

        while True:
            line = input().strip()
            if line.upper() == "DONE":
                break
            if line == "":
                print("Empty line is not valid. Please input a row or DONE.")
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) != len(columns):
                print(f"Invalid column count. Expected {len(columns)} values.")
                continue
            rows.append(parts)

        return pd.DataFrame(rows, columns=columns)

    restaurant = _read_rows("Enter restaurant rows:", restaurant_columns)
    customer = _read_rows("Enter customer rows:", customer_columns)

    numeric_restaurant_cols = ["open_time", "table_number"]
    numeric_customer_cols = ["index", "vip", "number", "arrival_time"]

    for col in numeric_restaurant_cols:
        restaurant[col] = pd.to_numeric(restaurant[col], errors="raise")
    for col in numeric_customer_cols:
        customer[col] = pd.to_numeric(customer[col], errors="raise")

    return restaurant,data_process(customer, random_state)

#data processing
def data_process(restaurant ,customer, random_state):

    random_offsets = np.random.randint(-10, 11, size=len(customer))
    customer["dinning_time"]=customer["number"]*10+20+random_state*random_offsets
    
    earliest_arrival = customer.groupby("restaurant")["arrival_time"].min()
    restaurant["open_time"] = restaurant["name"].map(earliest_arrival)

    return restaurant,customer

#pack and send
def package(restaurant, customer):
    restaurant_list = restaurant[["name", "strategy"]].drop_duplicates()
    result_columns = ["final_wait_time", "start_service_time", "leave_time"]
    for col in result_columns:
        if col not in customer.columns:
            customer[col] = np.nan
    
    for row in restaurant_list.itertuples(index=False):
        restaurant_name = row.name
        restaurant_strategy = row.strategy
        res_sub = restaurant[restaurant["name"] == restaurant_name]
        cus_sub = customer[customer["restaurant"] == restaurant_name]

        match restaurant_strategy:
            case "vip":
                updated_sub = strategy_vip.algorithm(res_sub, cus_sub)
                customer.loc[updated_sub.index, result_columns] = updated_sub[result_columns]
            case "single_snake":
                updated_sub = strategy_single_snake.algorithm(res_sub, cus_sub)
                customer.loc[updated_sub.index, result_columns] = updated_sub[result_columns]
            case "size_base":
                updated_sub = strategy_size_base.algorithm(res_sub, cus_sub)
                customer.loc[updated_sub.index, result_columns] = updated_sub[result_columns]
            # case "normal":
            #     pass

    print("Final customer wait-time preview:")
    print(customer[["restaurant", "index", "arrival_time", "final_wait_time", "start_service_time", "leave_time"]].head())
    return customer