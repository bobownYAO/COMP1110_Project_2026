import pandas as pd
import numpy as np

# Seat capacity per table type (max people a table of that type can seat)
TABLE_SEAT_CAPACITY = {"A": 2, "B": 4, "C": 6}


def f_total_seats(restaurant_sub):
   
    total = 0
    for _, row in restaurant_sub.iterrows():
        size     = row["table_size"]
        n_tables = int(row["table_number"])
        cap      = TABLE_SEAT_CAPACITY.get(size, 2)
        total   += n_tables * cap
    return total


def f_occupation_rate(customer_sub, total_seats, open_time):
    """Return average seat occupation: dining people divided by total seats."""
    
    served = customer_sub.dropna(subset=["start_service_time", "leave_time"])
    if served.empty:
        return np.nan, pd.Series(dtype=float)

    t_start = int(open_time)
    t_end   = int(served["leave_time"].max())

    rates = []
    minutes = list(range(t_start, t_end + 1))

    for t in minutes:
        dining_now = served[
            (served["start_service_time"] <= t) &
            (served["leave_time"] > t)
        ]["number"].sum()
        rates.append(dining_now / total_seats)

    rate_series = pd.Series(rates, index=minutes, name="occupation_rate")
    return rate_series.mean(), rate_series


def f_queue_length(customer_sub, open_time):
    if customer_sub.empty:
        return pd.Series(dtype=float, name="queue_length")

    t_start = int(min(open_time, customer_sub["arrival_time"].min()))
    candidates = [customer_sub["arrival_time"].max()]

    start_times = customer_sub["start_service_time"].dropna()
    leave_times = customer_sub["leave_time"].dropna()
    if not start_times.empty:
        candidates.append(start_times.max())
    if not leave_times.empty:
        candidates.append(leave_times.max())

    t_end = int(max(candidates))
    minutes = list(range(t_start, t_end + 1))
    queue_lengths = []

    for t in minutes:
        arrived = customer_sub["arrival_time"] <= t
        not_started = customer_sub["start_service_time"].isna() | (customer_sub["start_service_time"] > t)
        queue_lengths.append(int((arrived & not_started).sum()))

    return pd.Series(queue_lengths, index=minutes, name="queue_length")


def analysis(raw_data, restaurant, customer):

    print("\n" + "=" * 60)
    print("  RESTAURANT PERFORMANCE REPORT")
    print("=" * 60)

    restaurant_names = restaurant["name"].unique()
    summary_rows = []

    for r_name in restaurant_names:

        res_sub     = restaurant[restaurant["name"] == r_name]
        cus_sub     = raw_data[raw_data["restaurant"] == r_name].copy()
        strategy    = res_sub["strategy"].iloc[0]
        open_time   = res_sub["open_time"].iloc[0]
        total_seats = f_total_seats(res_sub)
        total_tables = int(res_sub["table_number"].sum())

        table_summary = {
            row["table_size"]: int(row["table_number"])
            for _, row in res_sub.iterrows()
        }

        print(f"\n{'-'*60}")
        print(f"  Restaurant : {r_name}")
        print(f"  Strategy   : {strategy}")
        print(f"  Open time  : t = {int(open_time)}")
        print(f"  Tables     : {table_summary}  ->  Total seats: {total_seats}")
        print(f"{'-'*60}")

        served   = cus_sub.dropna(subset=["final_wait_time"])
        unserved = cus_sub[cus_sub["final_wait_time"].isna()]
        queue_series = f_queue_length(cus_sub, open_time)

        # Wait time stats
        print(f"\n  -- Wait Time --")
        if served.empty:
            print("  Warning: No customers were served.")
        else:
            print(f"  Max waiting time : {served['final_wait_time'].max():.1f} min")
            print(f"  Min waiting time : {served['final_wait_time'].min():.1f} min")
            print(f"  Avg waiting time : {served['final_wait_time'].mean():.2f} min")
            print(f"  Served groups    : {len(served)} / {len(cus_sub)}")
            print(f"  Max queue length : {queue_series.max():.0f} groups")
            print(f"  Avg queue length : {queue_series.mean():.2f} groups")

        if not unserved.empty:
            print(f"\n  Warning: Unserved customers: index = {unserved['index'].tolist()}")

        # Occupation rate
        avg_occ, occ_series = f_occupation_rate(cus_sub, total_seats, open_time)

        print(f"\n  -- Occupation Rate --")
        if np.isnan(avg_occ):
            print("  Warning: Cannot compute - no served customers.")
        else:
            print(f"  Avg occupation rate : {avg_occ * 100:.2f}%")
            print(f"  Operating window    : t = {occ_series.index[0]} -> t = {occ_series.index[-1]}")

            # Minute-by-minute table
            served_detail = cus_sub.dropna(subset=["start_service_time", "leave_time"])
            print(f"\n  {'Minute':>8}  {'Dining people':>14}  {'/ Total seats':>14}  {'Rate':>8}")
            print(f"  {'------':>8}  {'-------------':>14}  {'-------------':>14}  {'----':>8}")
            for t, rate in occ_series.items():
                dining_now = int(served_detail[
                    (served_detail["start_service_time"] <= t) &
                    (served_detail["leave_time"] > t)
                ]["number"].sum())
                print(f"  {t:>8}  {dining_now:>14}  {total_seats:>14}  {rate*100:>7.1f}%")

        summary_rows.append({
            "restaurant": r_name,
            "strategy": strategy,
            "customers": int(len(cus_sub)),
            "served": int(len(served)),
            "unserved": int(len(unserved)),
            "avg_wait_time": np.nan if served.empty else float(served["final_wait_time"].mean()),
            "max_wait_time": np.nan if served.empty else float(served["final_wait_time"].max()),
            "avg_occupation_rate_pct": np.nan if np.isnan(avg_occ) else float(avg_occ * 100),
            "avg_queue_length": np.nan if queue_series.empty else float(queue_series.mean()),
            "max_queue_length": np.nan if queue_series.empty else int(queue_series.max()),
            "total_tables": total_tables,
            "total_seats": int(total_seats),
        })

    print(f"\n{'='*60}\n")
    return pd.DataFrame(summary_rows)
