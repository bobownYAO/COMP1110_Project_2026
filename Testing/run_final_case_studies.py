from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "Modeling&Coding"
OUTPUT_ROOT = PROJECT_ROOT / "Testing" / "final_case_outputs"

sys.path.insert(0, str(MODEL_DIR))

from main import run_from_csv  # noqa: E402


CASES = [
    (
        "baseline_single",
        "Testing/Baseline/testdata_restaurant_single_5r_200c_normal.csv",
        "Testing/Baseline/testdata_customer_single_5r_200c_normal.csv",
    ),
    (
        "baseline_size_base",
        "Testing/Baseline/testdata_restaurant_size_base_5r_200c_normal.csv",
        "Testing/Baseline/testdata_customer_size_base_5r_200c_normal.csv",
    ),
    (
        "baseline_vip",
        "Testing/Baseline/testdata_restaurant_vip_5r_200c_normal.csv",
        "Testing/Baseline/testdata_customer_vip_5r_200c_normal.csv",
    ),
    (
        "more_vip",
        "Testing/MoreVIP/testdata_restaurant_vip_5r_200c_normal.csv",
        "Testing/MoreVIP/testdata_customer_vip_5r_200c_normal.csv",
    ),
    (
        "more_small_single",
        "Testing/Testdata-MoreA/testdata_restaurant_single_5r_200c_normal.csv",
        "Testing/Testdata-MoreA/testdata_customer_single_5r_200c_normal.csv",
    ),
    (
        "more_small_size_base",
        "Testing/Testdata-MoreA/testdata_restaurant_size_base_5r_200c_normal.csv",
        "Testing/Testdata-MoreA/testdata_customer_size_base_5r_200c_normal.csv",
    ),
    (
        "more_small_vip",
        "Testing/Testdata-MoreA/testdata_restaurant_vip_5r_200c_normal.csv",
        "Testing/Testdata-MoreA/testdata_customer_vip_5r_200c_normal.csv",
    ),
    (
        "single_short",
        "Testing/Testdate-longshort/testdata_restaurant_single_5r_200c_short.csv",
        "Testing/Testdate-longshort/testdata_customer_single_5r_200c_short.csv",
    ),
    (
        "single_long",
        "Testing/Testdate-longshort/testdata_restaurant_single_5r_200c_long.csv",
        "Testing/Testdate-longshort/testdata_customer_single_5r_200c_long.csv",
    ),
    (
        "size_base_short",
        "Testing/Testdate-longshort/testdata_restaurant_size_base_5r_200c_short.csv",
        "Testing/Testdate-longshort/testdata_customer_size_base_5r_200c_short.csv",
    ),
    (
        "size_base_long",
        "Testing/Testdate-longshort/testdata_restaurant_size_base_5r_200c_long.csv",
        "Testing/Testdate-longshort/testdata_customer_size_base_5r_200c_long.csv",
    ),
    (
        "vip_short",
        "Testing/Testdate-longshort/testdata_restaurant_vip_5r_200c_short.csv",
        "Testing/Testdate-longshort/testdata_customer_vip_5r_200c_short.csv",
    ),
    (
        "vip_long",
        "Testing/Testdate-longshort/testdata_restaurant_vip_5r_200c_long.csv",
        "Testing/Testdate-longshort/testdata_customer_vip_5r_200c_long.csv",
    ),
]


def main():
    for case_name, restaurant_csv, customer_csv in CASES:
        print(f"\n=== Running {case_name} ===")
        run_from_csv(
            PROJECT_ROOT / restaurant_csv,
            PROJECT_ROOT / customer_csv,
            OUTPUT_ROOT / case_name,
            random_state=0,
        )

    print(f"\nAll case-study outputs saved under: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
