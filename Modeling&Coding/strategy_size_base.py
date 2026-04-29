import numpy as np

from queue_structure import State


# 按人数映射到桌型，与 strategy_vip 完全一致
# 返回 "A" / "B" / "C"，方便直接复用 State 默认 models

def assigned_table(number):
    if number <= 2:
        return "A"
    elif number <= 4:
        return "B"
    else:
        return "C"


def algorithm(restaurant, customer):
    """Size-base 策略：按桌型分队列，但不区分 VIP。

    - 顾客根据人数被分配到 A/B/C 桌型对应的等待队列；
    - 每个桌型只有一条 FIFO 队列（我们统一用 non_vip 队列存放）；
    - 不考虑 vip 字段，所有顾客一视同仁，先到先服务。
    """

    # 拷贝一份，避免在原 DataFrame 上无意修改
    customer = customer.sort_values("arrival_time").copy()

    # 初始化结果列
    customer["final_wait_time"] = np.nan
    customer["start_service_time"] = np.nan
    customer["leave_time"] = np.nan
    customer["assigned_table_type"] = None

    # 把餐厅的桌子信息整理成 dict，比如 {"A": 3, "B": 2, "C": 1}
    table = dict(zip(restaurant["table_size"], restaurant["table_number"]))

    # 使用默认 State：models=("A", "B", "C")
    queue_state = State()

    # 从开门时间开始模拟
    now_time = int(restaurant.iloc[0]["open_time"])
    pointer_customer = 0

    # 只要系统里还有人（在队列里或者未来会到达），就继续模拟
    while (not queue_state.is_empty()) or (pointer_customer < len(customer)):
        # 1) 先释放已经吃完的桌子
        for table_index in ("A", "B", "C"):
            while queue_state.peek_occupied(table_index) and queue_state.peek_occupied(table_index)[0] <= now_time:
                queue_state.pop_occupied(table_index)

        # 2) 把到达时间 <= now_time 的顾客全部入队
        while pointer_customer < len(customer) and int(customer.iloc[pointer_customer]["arrival_time"]) <= now_time:
            customer_data = customer.iloc[pointer_customer]
            customer_id = customer.index[pointer_customer]

            queue_state.enqueue_waiting(
                model=assigned_table(customer_data["number"]),
                # 不区分 VIP，一律放到 non_vip 队列
                is_vip=False,
                arrive_time=int(customer_data["arrival_time"]),
                customer_size=int(customer_data["number"]),
                customer_id=customer_id,
                wait_time=0,
                dinning_time=int(customer_data["dinning_time"]),
            )
            pointer_customer += 1

        # 3) 按桌型安排入座：只看 non_vip 队列
        for table_index in ("A", "B", "C"):
            # 当前已经占用的桌子数量
            while table[table_index] > queue_state.occupied_size(table_index) and queue_state.waiting_size(table_index, False):
                x = queue_state.dequeue_waiting(table_index, False)
                arrive_time, customer_size, customer_id, _, dinning_time = x

                customer.loc[customer_id, "final_wait_time"] = now_time - arrive_time
                customer.loc[customer_id, "start_service_time"] = now_time
                customer.loc[customer_id, "leave_time"] = now_time + dinning_time
                customer.loc[customer_id, "assigned_table_type"] = table_index

                queue_state.push_occupied(
                    table_index,
                    now_time + dinning_time,
                    now_time,
                    customer_size,
                    customer_id,
                )

        # 时间前进一单位
        now_time += 1

    return customer
