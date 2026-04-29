import pandas as pd
import numpy as np

from queue_structure import State

def assigned_table(number):
    if number <= 2:
        return "A"
    elif number <= 4:
        return "B"
    else:
        return "C"

def algorithm(restaurant, customer):

    print(f"Preview:\n{restaurant.head()}")
    print(f"Preview:\n{customer.head()}")

    customer = customer.sort_values("arrival_time").copy()
    customer["final_wait_time"] = np.nan
    customer["start_service_time"] = np.nan
    customer["leave_time"] = np.nan
    customer["assigned_table_type"] = None

    table = dict(zip(restaurant["table_size"], restaurant["table_number"]))

    queue_state = State()

    now_time = int(restaurant.iloc[0]["open_time"])
    pointer_customer = 0

    while (not queue_state.is_empty()) or (pointer_customer < len(customer)):

        for table_index in ("A", "B", "C"):
            while queue_state.peek_occupied(table_index) and queue_state.peek_occupied(table_index)[0] <= now_time:
                queue_state.pop_occupied(table_index)

        while pointer_customer < len(customer) and int(customer.iloc[pointer_customer]["arrival_time"]) <= now_time:
            customer_data = customer.iloc[pointer_customer]
            customer_id = customer.index[pointer_customer]
            queue_state.enqueue_waiting(
                model=assigned_table(customer_data["number"]),
                is_vip=bool(customer_data["vip"]),
                arrive_time=int(customer_data["arrival_time"]),
                customer_id=customer_id,
                customer_size=int(customer_data["number"]),
                wait_time=0,
                dinning_time=int(customer_data["dinning_time"])
                )
            pointer_customer += 1

        for table_index in ("A", "B", "C"):
            while table[table_index] > queue_state.occupied_size(table_index) and queue_state.waiting_size(table_index, True):
                x = queue_state.dequeue_waiting(table_index, True)
                arrive_time, customer_size, customer_id, _, dinning_time = x
                customer.loc[customer_id, "final_wait_time"] = now_time - arrive_time
                customer.loc[customer_id, "start_service_time"] = now_time
                customer.loc[customer_id, "leave_time"] = now_time + dinning_time
                customer.loc[customer_id, "assigned_table_type"] = table_index
                queue_state.push_occupied(table_index, now_time + dinning_time, now_time, customer_size, customer_id)

            while table[table_index] > queue_state.occupied_size(table_index) and queue_state.waiting_size(table_index, False):
                x = queue_state.dequeue_waiting(table_index, False)
                arrive_time, customer_size, customer_id, _, dinning_time = x
                customer.loc[customer_id, "final_wait_time"] = now_time - arrive_time
                customer.loc[customer_id, "start_service_time"] = now_time
                customer.loc[customer_id, "leave_time"] = now_time + dinning_time
                customer.loc[customer_id, "assigned_table_type"] = table_index
                queue_state.push_occupied(table_index, now_time + dinning_time, now_time, customer_size, customer_id)

        now_time += 1

    return customer








