from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "Modeling&Coding"
SAMPLE_DIR = PROJECT_ROOT / "Testing" / "sample_cases"

sys.path.insert(0, str(MODEL_DIR))

import io_file  # noqa: E402


def sample_path(filename):
    return SAMPLE_DIR / filename


def test_valid_csv_input_loads_and_adds_dinning_time():
    restaurant, customer = io_file.read_file(
        sample_path("valid_restaurant.csv"),
        sample_path("valid_customer.csv"),
        random_state=0,
    )

    assert list(restaurant["name"].unique()) == ["R1"]
    assert "dinning_time" in customer.columns
    assert customer["dinning_time"].tolist() == [40, 60, 70]


@pytest.mark.parametrize(
    ("restaurant_file", "customer_file", "message"),
    [
        ("missing_column_restaurant.csv", "valid_customer.csv", "missing required column"),
        ("valid_restaurant.csv", "missing_column_customer.csv", "missing required column"),
        ("invalid_strategy_restaurant.csv", "valid_customer.csv", "invalid value"),
        ("invalid_table_type_restaurant.csv", "valid_customer.csv", "table_size"),
        ("missing_table_type_restaurant.csv", "valid_customer.csv", "missing table type"),
        ("valid_restaurant.csv", "invalid_numeric_customer.csv", "numeric values"),
        ("valid_restaurant.csv", "invalid_vip_customer.csv", "only 0 or 1"),
        ("valid_restaurant.csv", "unknown_restaurant_customer.csv", "unknown restaurant"),
        ("valid_restaurant.csv", "negative_value_customer.csv", "negative values"),
    ],
)
def test_invalid_csv_input_raises_clear_value_error(restaurant_file, customer_file, message):
    with pytest.raises(ValueError, match=message):
        io_file.read_file(
            sample_path(restaurant_file),
            sample_path(customer_file),
            random_state=0,
        )
