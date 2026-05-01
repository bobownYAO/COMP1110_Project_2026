from pathlib import Path
import sys

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "Modeling&Coding"

sys.path.insert(0, str(MODEL_DIR))

from main import run_simulation  # noqa: E402


SUMMARY_COLUMNS = {
    "restaurant",
    "strategy",
    "customers",
    "served",
    "unserved",
    "avg_wait_time",
    "max_wait_time",
    "avg_occupation_rate_pct",
    "avg_queue_length",
    "max_queue_length",
    "total_tables",
    "total_seats",
}


def restaurant(strategy):
    return pd.DataFrame(
        [
            {"name": "R1", "strategy": strategy, "open_time": 0, "table_size": "A", "table_number": 1},
            {"name": "R1", "strategy": strategy, "open_time": 0, "table_size": "B", "table_number": 1},
            {"name": "R1", "strategy": strategy, "open_time": 0, "table_size": "C", "table_number": 1},
        ]
    )


@pytest.mark.parametrize(
    ("strategy", "customers", "expected_waits", "expected_starts", "expected_leaves", "expected_tables", "avg_wait", "max_wait"),
    [
        (
            "single_snake",
            [
                {"index": 1, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 0, "dinning_time": 10},
                {"index": 2, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 1, "dinning_time": 10},
                {"index": 3, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 2, "dinning_time": 10},
                {"index": 4, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 3, "dinning_time": 10},
            ],
            [0, 0, 0, 7],
            [0, 1, 2, 10],
            [10, 11, 12, 20],
            ["A", "B", "C", "A"],
            1.75,
            7,
        ),
        (
            "size_base",
            [
                {"index": 1, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 0, "dinning_time": 10},
                {"index": 2, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 1, "dinning_time": 10},
                {"index": 3, "restaurant": "R1", "vip": 0, "number": 4, "arrival_time": 0, "dinning_time": 5},
                {"index": 4, "restaurant": "R1", "vip": 0, "number": 5, "arrival_time": 0, "dinning_time": 5},
            ],
            [0, 9, 0, 0],
            [0, 10, 0, 0],
            [10, 20, 5, 5],
            ["A", "A", "B", "C"],
            2.25,
            9,
        ),
        (
            "vip",
            [
                {"index": 1, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 0, "dinning_time": 10},
                {"index": 2, "restaurant": "R1", "vip": 1, "number": 2, "arrival_time": 0, "dinning_time": 10},
                {"index": 3, "restaurant": "R1", "vip": 0, "number": 4, "arrival_time": 0, "dinning_time": 5},
                {"index": 4, "restaurant": "R1", "vip": 0, "number": 5, "arrival_time": 0, "dinning_time": 5},
            ],
            [10, 0, 0, 0],
            [10, 0, 0, 0],
            [20, 10, 5, 5],
            ["A", "A", "B", "C"],
            2.5,
            10,
        ),
    ],
)
def test_end_to_end_summary_metrics_and_outputs(
    tmp_path,
    strategy,
    customers,
    expected_waits,
    expected_starts,
    expected_leaves,
    expected_tables,
    avg_wait,
    max_wait,
):
    output_dir = tmp_path / strategy
    raw_data, summary = run_simulation(
        restaurant(strategy),
        pd.DataFrame(customers),
        output_dir=output_dir,
    )

    ordered = raw_data.sort_values("index").reset_index(drop=True)
    assert ordered["final_wait_time"].tolist() == expected_waits
    assert ordered["start_service_time"].tolist() == expected_starts
    assert ordered["leave_time"].tolist() == expected_leaves
    assert ordered["assigned_table_type"].tolist() == expected_tables

    row = summary.iloc[0]
    assert SUMMARY_COLUMNS.issubset(summary.columns)
    assert row["customers"] == 4
    assert row["served"] == 4
    assert row["unserved"] == 0
    assert row["avg_wait_time"] == pytest.approx(avg_wait)
    assert row["max_wait_time"] == pytest.approx(max_wait)
    assert row["max_queue_length"] == 1

    expected_outputs = {
        "summary_metrics_by_restaurant.csv",
        "occupation_rate.png",
        "table_utilization_line.png",
        "table_utilization_bar.png",
        "waiting_time_density.png",
        "queue_length_over_time.png",
    }
    assert expected_outputs.issubset({path.name for path in output_dir.iterdir()})
