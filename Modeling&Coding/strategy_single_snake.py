import pandas as pd
import numpy as np

from queue_structure import State
from collections import deque

def algorithm(restaurant, customer):

    print(f"Preview:\n{restaurant.head()}")
    print(f"Preview:\n{customer.head()}")

    customer = customer.sort_values("arrival_time").copy()
    customer["final_wait_time"] = np.nan
    customer["start_service_time"] = np.nan
    customer["leave_time"] = np.nan

    table = dict(zip(restaurant["table_size"], restaurant["table_number"]))
    table_types = ["A", "B", "C"]

    queue_state = State()
    # create single queue
    global_waiting_queue = deque()

    now_time = int(restaurant.iloc[0]["open_time"])
    pointer_customer = 0

    while (not queue_state.is_empty()) or (pointer_customer < len(customer) or  global_waiting_queue):
        for t_type in table_types:
            while queue_state.peek_occupied(t_type) and queue_state.peek_occupied(t_type)[0] <= now_time:
                queue_state.pop_occupied(t_type)

        while pointer_customer < len(customer) and int(customer.iloc[pointer_customer]["arrival_time"]) <= now_time:
            cust = customer.iloc[pointer_customer]
            cust_id = customer.index[pointer_customer]
            global_waiting_queue.append((
                int(cust["arrival_time"]),
                int(cust["number"]),
                cust_id,
                int(cust["dinning_time"])))
            pointer_customer += 1

        #assign customer
        while True:
            assigned = False
            for i in range(len(global_waiting_queue)):
                arrive_time, cust_size, cust_id, din_time = global_waiting_queue[i]

                #minimum table size
                if cust_size <= 2:
                    min_idx = 0
                elif cust_size <= 4:
                    min_idx = 1
                else:
                    min_idx = 2

                #search for suitable table
                for t_idx in range(min_idx, len(table_types)):
                    t_type = table_types[t_idx]
                    if table[t_type] > queue_state.occupied_size(t_type):
                        customer.loc[cust_id, "final_wait_time"] = now_time - arrive_time
                        customer.loc[cust_id, "start_service_time"] = now_time
                        customer.loc[cust_id, "leave_time"] = now_time + din_time
                        queue_state.push_occupied(t_type, now_time + din_time, now_time, cust_size, cust_id)
                        del global_waiting_queue[i]
                        assigned = True
                        break
                if assigned:
                    break
            if not assigned:
                break
        now_time += 1

    return customer