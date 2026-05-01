from pathlib import Path
import sys

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "Modeling&Coding"

sys.path.insert(0, str(MODEL_DIR))

import strategy_single_snake  # noqa: E402
import strategy_size_base  # noqa: E402
import strategy_vip  # noqa: E402


RESULT_COLUMNS = {
    "final_wait_time",
    "start_service_time",
    "leave_time",
    "assigned_table_type",
}


def restaurant(strategy, table_counts=None):
    table_counts = table_counts or {"A": 1, "B": 1, "C": 1}
    return pd.DataFrame(
        [
            {
                "name": "R1",
                "strategy": strategy,
                "open_time": 0,
                "table_size": table_type,
                "table_number": count,
            }
            for table_type, count in table_counts.items()
        ]
    )


def customers(rows):
    return pd.DataFrame(rows)


@pytest.mark.parametrize(
    ("algorithm", "strategy"),
    [
        (strategy_single_snake.algorithm, "single_snake"),
        (strategy_size_base.algorithm, "size_base"),
        (strategy_vip.algorithm, "vip"),
    ],
)
def test_strategy_outputs_include_common_result_columns(algorithm, strategy):
    result = algorithm(
        restaurant(strategy),
        customers(
            [
                {
                    "index": 1,
                    "restaurant": "R1",
                    "vip": 0,
                    "number": 2,
                    "arrival_time": 0,
                    "dinning_time": 10,
                }
            ]
        ),
    )

    assert RESULT_COLUMNS.issubset(result.columns)
    assert result.loc[0, "final_wait_time"] == 0
    assert result.loc[0, "start_service_time"] == 0
    assert result.loc[0, "leave_time"] == 10
    assert result.loc[0, "assigned_table_type"] == "A"


def test_size_base_uses_matching_table_queue_and_fifo_waiting():
    result = strategy_size_base.algorithm(
        restaurant("size_base", {"A": 1, "B": 1, "C": 1}),
        customers(
            [
                {"index": 1, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 0, "dinning_time": 10},
                {"index": 2, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 1, "dinning_time": 10},
                {"index": 3, "restaurant": "R1", "vip": 0, "number": 4, "arrival_time": 0, "dinning_time": 5},
                {"index": 4, "restaurant": "R1", "vip": 0, "number": 5, "arrival_time": 0, "dinning_time": 5},
            ]
        ),
    )

    assert result.loc[0, "assigned_table_type"] == "A"
    assert result.loc[2, "assigned_table_type"] == "B"
    assert result.loc[3, "assigned_table_type"] == "C"
    assert result.loc[1, "start_service_time"] == 10
    assert result.loc[1, "final_wait_time"] == 9


def test_vip_serves_vip_before_non_vip_within_same_table_type():
    result = strategy_vip.algorithm(
        restaurant("vip", {"A": 1, "B": 0, "C": 0}),
        customers(
            [
                {"index": 1, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 0, "dinning_time": 10},
                {"index": 2, "restaurant": "R1", "vip": 1, "number": 2, "arrival_time": 0, "dinning_time": 10},
            ]
        ),
    )

    assert result.loc[1, "start_service_time"] == 0
    assert result.loc[1, "final_wait_time"] == 0
    assert result.loc[0, "start_service_time"] == 10
    assert result.loc[0, "final_wait_time"] == 10
    assert result["assigned_table_type"].tolist() == ["A", "A"]


def test_single_snake_can_assign_small_group_to_larger_available_table():
    result = strategy_single_snake.algorithm(
        restaurant("single_snake", {"A": 0, "B": 1, "C": 0}),
        customers(
            [
                {"index": 1, "restaurant": "R1", "vip": 0, "number": 2, "arrival_time": 0, "dinning_time": 10},
            ]
        ),
    )

    assert result.loc[0, "assigned_table_type"] == "B"
    assert result.loc[0, "start_service_time"] == 0
    assert result.loc[0, "final_wait_time"] == 0
