import pandas as pd
import numpy as np

# Seat capacity per table type (max people a table of that type can seat)
TABLE_SEAT_CAPACITY = {"A": 2, "B": 4, "C": 6}


def total_seats1(restaurant_sub):
   
    total = 0
    for _, row in restaurant_sub.iterrows():
        size     = row["table_size"]
        n_tables = int(row["table_number"])
        cap      = TABLE_SEAT_CAPACITY.get(size, 2)
        total   += n_tables * cap
    return total


def occupation_rate(customer_sub, total_seats, open_time):
    
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


def analysis(raw_data, restaurant, customer):

    print("\n" + "=" * 60)
    print("  RESTAURANT PERFORMANCE REPORT")
    print("=" * 60)

    restaurant_names = restaurant["name"].unique()

    for r_name in restaurant_names:

        res_sub     = restaurant[restaurant["name"] == r_name]
        cus_sub     = raw_data[raw_data["restaurant"] == r_name].copy()
        strategy    = res_sub["strategy"].iloc[0]
        open_time   = res_sub["open_time"].iloc[0]
        total_seats = total_seats1(res_sub)

        table_summary = {
            row["table_size"]: int(row["table_number"])
            for _, row in res_sub.iterrows()
        }

        print(f"\n{'─'*60}")
        print(f"  Restaurant : {r_name}")
        print(f"  Strategy   : {strategy}")
        print(f"  Open time  : t = {int(open_time)}")
        print(f"  Tables     : {table_summary}  →  Total seats: {total_seats}")
        print(f"{'─'*60}")

        served   = cus_sub.dropna(subset=["final_wait_time"])
        unserved = cus_sub[cus_sub["final_wait_time"].isna()]

        # ── Wait time stats ───────────────────────────────────────────────
        print(f"\n  ── Wait Time ──")
        if served.empty:
            print("  ⚠  No customers were served.")
        else:
            print(f"  Max waiting time : {served['final_wait_time'].max():.1f} min")
            print(f"  Min waiting time : {served['final_wait_time'].min():.1f} min")
            print(f"  Avg waiting time : {served['final_wait_time'].mean():.2f} min")

        if not unserved.empty:
            print(f"\n  ⚠  Unserved customers: index = {unserved['index'].tolist()}")

        # ── Occupation rate ───────────────────────────────────────────────
        avg_occ, occ_series = occupation_rate(cus_sub, total_seats, open_time)

        print(f"\n  ── Occupation Rate ──")
        if np.isnan(avg_occ):
            print("  ⚠  Cannot compute — no served customers.")
        else:
            print(f"  Avg occupation rate : {avg_occ * 100:.2f}%")
            print(f"  Operating window    : t = {occ_series.index[0]} → t = {occ_series.index[-1]}")

            # Minute-by-minute table
            served_detail = cus_sub.dropna(subset=["start_service_time", "leave_time"])
            print(f"\n  {'Minute':>8}  {'Dining people':>14}  {'/ Total seats':>14}  {'Rate':>8}")
            print(f"  {'──────':>8}  {'─────────────':>14}  {'─────────────':>14}  {'────':>8}")
            for t, rate in occ_series.items():
                dining_now = int(served_detail[
                    (served_detail["start_service_time"] <= t) &
                    (served_detail["leave_time"] > t)
                ]["number"].sum())
                print(f"  {t:>8}  {dining_now:>14}  {total_seats:>14}  {rate*100:>7.1f}%")

    print(f"\n{'='*60}\n")
