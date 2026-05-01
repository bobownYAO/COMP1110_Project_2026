import pandas as pd
import numpy as np

import strategy_vip
import strategy_single_snake
import strategy_size_base

RESTAURANT_COLUMNS = ["name", "strategy", "open_time", "table_size", "table_number"]
CUSTOMER_COLUMNS = ["index", "restaurant", "vip", "number", "arrival_time"]
NUMERIC_RESTAURANT_COLUMNS = ["open_time", "table_number"]
NUMERIC_CUSTOMER_COLUMNS = ["index", "vip", "number", "arrival_time"]
VALID_STRATEGIES = {"vip", "single_snake", "size_base"}
VALID_TABLE_SIZES = {"A", "B", "C"}


def _check_required_columns(df, required_columns, label):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"{label} data is missing required column(s): {', '.join(missing)}")


def _check_not_empty(df, label):
    if df.empty:
        raise ValueError(f"{label} data must contain at least one row.")


def _convert_numeric_columns(df, numeric_columns, label):
    for col in numeric_columns:
        try:
            df[col] = pd.to_numeric(df[col], errors="raise")
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{label} column '{col}' must contain numeric values.") from exc


def _check_no_missing_values(df, columns, label):
    missing_columns = [col for col in columns if df[col].isna().any()]
    if missing_columns:
        raise ValueError(f"{label} data has missing value(s) in: {', '.join(missing_columns)}")


def _check_non_negative(df, columns, label):
    for col in columns:
        if (df[col] < 0).any():
            raise ValueError(f"{label} column '{col}' cannot contain negative values.")


def _validate_restaurant_data(restaurant):
    _check_not_empty(restaurant, "Restaurant")
    _check_required_columns(restaurant, RESTAURANT_COLUMNS, "Restaurant")
    _check_no_missing_values(restaurant, RESTAURANT_COLUMNS, "Restaurant")
    _convert_numeric_columns(restaurant, NUMERIC_RESTAURANT_COLUMNS, "Restaurant")
    _check_non_negative(restaurant, NUMERIC_RESTAURANT_COLUMNS, "Restaurant")

    invalid_strategies = sorted(set(restaurant["strategy"]) - VALID_STRATEGIES)
    if invalid_strategies:
        raise ValueError(
            "Restaurant column 'strategy' contains invalid value(s): "
            + ", ".join(map(str, invalid_strategies))
        )

    invalid_table_sizes = sorted(set(restaurant["table_size"]) - VALID_TABLE_SIZES)
    if invalid_table_sizes:
        raise ValueError(
            "Restaurant column 'table_size' contains invalid value(s): "
            + ", ".join(map(str, invalid_table_sizes))
        )

    for restaurant_name, rows in restaurant.groupby("name"):
        missing_table_sizes = sorted(VALID_TABLE_SIZES - set(rows["table_size"]))
        if missing_table_sizes:
            raise ValueError(
                f"Restaurant '{restaurant_name}' is missing table type(s): "
                + ", ".join(missing_table_sizes)
            )


def _validate_customer_data(customer, restaurant):
    _check_not_empty(customer, "Customer")
    _check_required_columns(customer, CUSTOMER_COLUMNS, "Customer")
    _check_no_missing_values(customer, CUSTOMER_COLUMNS, "Customer")
    _convert_numeric_columns(customer, NUMERIC_CUSTOMER_COLUMNS, "Customer")
    _check_non_negative(customer, NUMERIC_CUSTOMER_COLUMNS, "Customer")

    invalid_vip_values = sorted(set(customer["vip"]) - {0, 1})
    if invalid_vip_values:
        raise ValueError(
            "Customer column 'vip' must contain only 0 or 1. Invalid value(s): "
            + ", ".join(map(str, invalid_vip_values))
        )

    if (customer["number"] <= 0).any():
        raise ValueError("Customer column 'number' must be greater than 0.")

    missing_restaurants = sorted(set(customer["restaurant"]) - set(restaurant["name"]))
    if missing_restaurants:
        raise ValueError(
            "Customer data references unknown restaurant(s): "
            + ", ".join(map(str, missing_restaurants))
        )


def validate_input_data(restaurant, customer):
    _validate_restaurant_data(restaurant)
    _validate_customer_data(customer, restaurant)
    return restaurant, customer


#load data
def read_file(filepath_restaurant,filepath_customer,random_state):
    try:
        restaurant = pd.read_csv(filepath_restaurant)
        customer = pd.read_csv(filepath_customer)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {exc.filename}") from exc
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise ValueError("Input CSV format is empty or invalid.") from exc

    validate_input_data(restaurant, customer)
    return data_process(restaurant,customer, random_state)


def read_console(random_state):
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

    restaurant = _read_rows("Enter restaurant rows:", RESTAURANT_COLUMNS)
    customer = _read_rows("Enter customer rows:", CUSTOMER_COLUMNS)

    validate_input_data(restaurant, customer)
    return data_process(restaurant, customer, random_state)

#data processing
def data_process(restaurant ,customer, random_state):

    random_offsets = np.random.randint(-10, 11, size=len(customer))
    customer["dining_time"] = customer["number"] * 10 + 20 + random_state * random_offsets
    # Backward-compatible alias used by the existing strategy modules.
    customer["dinning_time"] = customer["dining_time"]
    
    earliest_arrival = customer.groupby("restaurant")["arrival_time"].min()
    restaurant["open_time"] = restaurant["name"].map(earliest_arrival)

    return restaurant,customer

#pack and send
def package(restaurant, customer):
    restaurant_list = restaurant[["name", "strategy"]].drop_duplicates()
    result_columns = ["final_wait_time", "start_service_time", "leave_time", "assigned_table_type"]
    for col in result_columns:
        if col not in customer.columns:
            customer[col] = None if col == "assigned_table_type" else np.nan
    
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
    print(customer[["restaurant", "index", "arrival_time", "final_wait_time", "start_service_time", "leave_time", "assigned_table_type"]].head())
    return customer
