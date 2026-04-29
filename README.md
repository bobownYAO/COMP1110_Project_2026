# Restaurant Queue Simulation Project

## 1. Project Overview

This project simulates restaurant queue management under different seating strategies. It focuses on how restaurants assign arriving customer groups to limited table resources, and how these decisions affect waiting time, service order, and table utilization.

The simulation is implemented in Python. It reads restaurant and customer data, preprocesses the input, runs a discrete-time queue simulation, and prints performance analysis for each restaurant. The project currently supports three queue strategies:

- `single_snake`: one shared waiting queue is used for all customers, and each group is seated when a suitable table becomes available.
- `size_base`: customers are separated by group size and matched to table categories.
- `vip`: customers are separated by group size, and VIP customers are served before non-VIP customers within the same table category.

The repository also includes generated testing datasets and visualization scripts for comparing strategy behavior across different scenarios.

## 2. Group Members and Roles

## 3. Language and Environment

The project is written in Python 3. The current local environment used during inspection is Python 3.13.9, but the code only relies on standard Python syntax and common data-analysis libraries.

Required external libraries:

- `pandas`
- `numpy`
- `matplotlib`

Testing-only dependency:

- `pytest`

There is currently no `requirements.txt` or other dependency-management file in the repository. Install the required libraries manually before running the project:

```bash
python -m pip install pandas numpy matplotlib
```

Install `pytest` as well if you want to run the automated sample tests:

```bash
python -m pip install pytest
```

## 4. Repository Structure

```text
COMP1110_Project_2026/
|-- README.md
|-- Modeling&Coding/
|   |-- main.py
|   |-- io_file.py
|   |-- queue_structure.py
|   |-- strategy_single_snake.py
|   |-- strategy_size_base.py
|   |-- strategy_vip.py
|   |-- output_file.py
|   |-- plot_occupation.py
|   |-- plot_table_utilization_line.py
|   |-- plot_table_utilization_bar.py
|   |-- plot_waiting_time_density.py
|   |-- plot_queue_length_over_time.py
|   |-- testdata_restaurant.csv
|   `-- testdata_customer.csv
|-- Testing/
|   |-- data_generate.py
|   |-- Baseline/
|   |-- MoreVIP/
|   |-- Testdata-MoreA/
|   `-- Testdate-longshort/
|-- Final_report/
|-- Plan/
`-- Research/
```

Main folders:

- `Modeling&Coding/`: contains the executable simulation code, data loading functions, queue-state structure, strategy algorithms, result analysis, plotting scripts, and small sample CSV files.
- `Testing/`: contains generated restaurant/customer datasets, scenario folders, previous output charts, and `data_generate.py` for creating new synthetic test data.
- `Final_report/`: contains the final report and generated figures used for project analysis.
- `Plan/`: contains planning materials for the project.
- `Research/`: contains research notes that motivated the selected queue strategies.

## 5. How to Run

First, install the required Python packages:

```bash
python -m pip install pandas numpy matplotlib
```

Then move into the main code folder:

```bash
cd "COMP1110_Project_2026\Modeling&Coding"
```

Run the main program:

```bash
python main.py
```

The program will ask two questions.

For dining time prediction:

- Choose `A` for random dining time.
- Choose `B` for fixed dining time.

For data loading:

- Choose `A` to type restaurant and customer rows manually in the console.
- Choose `B` to load CSV files by entering file paths.

CSV mode requires explicit restaurant and customer CSV paths. For example, use the sample files:

```text
COMP1110_Project_2026\Modeling&Coding\testdata_restaurant.csv
COMP1110_Project_2026\Modeling&Coding\testdata_customer.csv
```

After the simulation finishes, the program prints a restaurant performance report and saves visualization charts such as occupation rate, table utilization, waiting-time density, and queue length over time.

To generate new synthetic CSV datasets, run the testing data generator:

```bash
cd "COMP1110_Project_2026\Testing"
python data_generate.py
```

The generator asks for strategy, number of restaurants, number of customers, VIP probability, group-size distribution, and arrival interval mode. It then writes restaurant and customer CSV files to the selected output directory.

To run the automated input-validation tests from the project root:

```bash
python -m pytest Testing
```

## 6. Input File Format

The simulation uses two CSV files: one for restaurant settings and one for customer arrivals.

### Restaurant CSV

Required columns:

| Column | Description |
|---|---|
| `name` | Restaurant identifier, such as `R1`. Rows with the same name belong to the same restaurant. |
| `strategy` | Queue strategy used by the restaurant. Accepted values are `single_snake`, `size_base`, and `vip`. |
| `open_time` | Initial opening time. During preprocessing, this value is replaced by the earliest arrival time for that restaurant. |
| `table_size` | Table category. The implemented categories are `A`, `B`, and `C`. |
| `table_number` | Number of tables available for this table category. |

Example:

```csv
name,strategy,open_time,table_size,table_number
R1,vip,0,A,5
R1,vip,0,B,3
R1,vip,0,C,2
```

Table categories are interpreted as:

- `A`: small table category, used for groups of 1-2 people.
- `B`: medium table category, used for groups of 3-4 people.
- `C`: large table category, used for groups of 5 or more people.

### Customer CSV

Required columns:

| Column | Description |
|---|---|
| `index` | Customer group identifier within the dataset or restaurant. |
| `restaurant` | Restaurant name. This should match a `name` value in the restaurant CSV. |
| `vip` | VIP status. Use `1` for VIP customers and `0` for non-VIP customers. |
| `number` | Number of people in the customer group. |
| `arrival_time` | Arrival time in integer time units. |

Example:

```csv
index,restaurant,vip,number,arrival_time
1,R1,0,3,0
2,R1,0,1,5
3,R1,1,4,10
```

During preprocessing, the program adds a calculated `dinning_time` column using the customer group size and the selected fixed/random dining-time mode. During simulation, it also adds result columns:

- `final_wait_time`
- `start_service_time`
- `leave_time`

### Validation Rules

The input reader checks data before the simulation strategies run. Invalid files raise `ValueError` with a message describing the problem.

Restaurant data must:

- contain all required columns
- contain at least one row
- use only the strategies `single_snake`, `size_base`, and `vip`
- use only table categories `A`, `B`, and `C`
- provide `A`, `B`, and `C` table rows for every restaurant
- use numeric, non-negative values for `open_time` and `table_number`
- avoid missing values in required columns

Customer data must:

- contain all required columns
- contain at least one row
- reference only restaurants that exist in the restaurant CSV
- use numeric, non-negative values for `index`, `vip`, `number`, and `arrival_time`
- use only `0` or `1` in the `vip` column
- use a group size greater than `0`
- avoid missing values in required columns

## 7. Features Implemented

- CSV input loading for restaurant settings and customer arrival data.
- Console input mode for manually entering restaurant and customer rows.
- Data preprocessing, including dining-time estimation and restaurant opening-time adjustment.
- Fixed and random dining-time modes.
- Discrete-time simulation of arrivals, waiting queues, occupied tables, and table release.
- Shared queue-state structure using FIFO queues for waiting customers and min-heaps for occupied tables.
- `single_snake` strategy with one global waiting queue.
- `size_base` strategy with table-category queues based on customer group size.
- `vip` strategy with VIP priority within each table category.
- Per-restaurant wait-time analysis, including maximum, minimum, and average waiting time.
- Occupation-rate calculation and minute-by-minute restaurant utilization reporting.
- Visualization scripts for occupation rate, table utilization, waiting-time density, and queue length over time.
- Synthetic testing data generation through `Testing/data_generate.py`.
- Pre-generated testing scenarios for baseline comparison, higher VIP ratio, more small groups, and different arrival intervals.

## 8. Sample Test Cases

The repository includes automated sample tests in `Testing/test_input_validation.py` and small CSV fixtures in `Testing/sample_cases/`.

Run them from the project root:

```bash
python -m pytest Testing
```

Sample cases covered:

| Case | Files | Expected result |
|---|---|---|
| Valid input | `valid_restaurant.csv`, `valid_customer.csv` | Loads successfully and adds `dinning_time`. |
| Missing restaurant column | `missing_column_restaurant.csv`, `valid_customer.csv` | Raises `ValueError` for missing required column. |
| Missing customer column | `valid_restaurant.csv`, `missing_column_customer.csv` | Raises `ValueError` for missing required column. |
| Invalid strategy | `invalid_strategy_restaurant.csv`, `valid_customer.csv` | Raises `ValueError` for invalid strategy value. |
| Invalid table type | `invalid_table_type_restaurant.csv`, `valid_customer.csv` | Raises `ValueError` for invalid table category. |
| Missing table type | `missing_table_type_restaurant.csv`, `valid_customer.csv` | Raises `ValueError` because each restaurant must include `A`, `B`, and `C`. |
| Invalid numeric value | `valid_restaurant.csv`, `invalid_numeric_customer.csv` | Raises `ValueError` for a non-numeric field. |
| Invalid VIP value | `valid_restaurant.csv`, `invalid_vip_customer.csv` | Raises `ValueError` because `vip` must be `0` or `1`. |
| Unknown restaurant | `valid_restaurant.csv`, `unknown_restaurant_customer.csv` | Raises `ValueError` for a customer referencing a missing restaurant. |
| Negative value | `valid_restaurant.csv`, `negative_value_customer.csv` | Raises `ValueError` for a negative numeric field. |

## 9. Case Studies

## 10. Limitations and Future Improvements
