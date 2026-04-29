# Restaurant Queue Simulation Project

## 1. Project Overview

This project simulates restaurant queue management under different seating strategies. It focuses on how restaurants assign arriving customer groups to limited table resources, and how these decisions affect waiting time, service order, and table utilization.

The simulation is implemented in Python. It reads restaurant and customer data, preprocesses the input, runs a discrete-time queue simulation, and prints performance analysis for each restaurant. The project currently supports three queue strategies:

- `single_snake`: one shared waiting queue is used for all customers, and each group is seated when a suitable table becomes available.
- `size_base`: customers are separated by group size and matched to table categories.
- `vip`: customers are separated by group size, and VIP customers are served before non-VIP customers within the same table category.

The repository also includes generated testing datasets and visualization scripts for comparing strategy behavior across different scenarios.

## 2. Group Members and Roles

The project work was organized around research, modeling, coding, testing, case studies, and report writing. The planned division of work is summarized below.

| Member | Main research focus | Modeling / coding focus | Report focus |
|---|---|---|---|
| Yao Lijia | VIP strategy and THE GULU case study | File input, data model, data generation, database management, Algorithm 1, and video demo | Vision, optimization, and data-model explanation |
| Yu Wei | Size-based queue strategy and Meituan / KeeTa case studies | Algorithm 2, sample testing, and group report writing | Problem definition, project significance, and algorithm explanation |
| Jiang Hongyi | Single snake queue, table sharing, and Meiwei Bu Yong Deng case study | Algorithm 3 and scenario design | Evaluation, limitations, and algorithm explanation |
| Zhang Zhanhao | Single snake strategy and Haidilao case study | File output, case simulation, and output analysis | Comparative analysis and case-simulation explanation |

## 3. Language and Environment

The project is written in Python 3. The current local environment used during inspection is Python 3.13.9, but the code only relies on standard Python syntax and common data-analysis libraries.

Required external libraries:

- `pandas`
- `numpy`
- `matplotlib`

Testing-only dependency:

- `pytest`

Install the required libraries from the repository root:

```bash
python -m pip install -r requirements.txt
```

If needed, the same dependencies can also be installed manually:

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

All generated charts and the numerical summary CSV are saved under `Modeling&Coding/outputs/` when the program is run from the main code folder. The summary file is:

```text
outputs/summary_metrics_by_restaurant.csv
```

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
- `assigned_table_type`

The `assigned_table_type` column records the actual table category used by a served group. This is especially important for the `single_snake` strategy because a small group may be seated at a larger available table.

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
- Actual assigned table type recorded for each served customer group.
- Per-restaurant wait-time analysis, including maximum, minimum, and average waiting time.
- Per-restaurant summary metrics exported to `outputs/summary_metrics_by_restaurant.csv`, including served/unserved counts and queue-length statistics.
- Occupation-rate calculation and minute-by-minute restaurant utilization reporting.
- Visualization scripts for occupation rate, table utilization, waiting-time density, and queue length over time.
- Synthetic testing data generation through `Testing/data_generate.py`.
- Pre-generated testing scenarios for baseline comparison, higher VIP ratio, more small groups, and different arrival intervals.

## 8. Sample Test Cases

The repository includes automated sample tests in `Testing/test_input_validation.py`, strategy behavior tests in `Testing/test_strategy_behavior.py`, and small CSV fixtures in `Testing/sample_cases/`.

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
| Missing file | Missing restaurant CSV path | Raises `FileNotFoundError` with a clear message. |
| Empty or malformed CSV | Temporary invalid CSV files | Raises `ValueError` before simulation starts. |
| Strategy behavior | Direct calls to `single_snake`, `size_base`, and `vip` modules | Confirms result columns, VIP priority, size-based FIFO behavior, and Single Snake table fallback. |

## 9. Case Studies

The final report uses several synthetic case studies to compare the three implemented strategies under different demand conditions. Each main case uses the same basic scale: five restaurants, 200 customer groups per restaurant, and fixed dining time. The comparison focuses on waiting time, queue length, occupation rate, table utilization, and waiting-time distribution. The final report also reorganizes the existing datasets into paired scenarios required by Topic C, so the changed factor and fixed controls are explicit.

Case groups studied:

| Case group | What was tested | Brief conclusion |
|---|---|---|
| Baseline / normal demand | Compared `single_snake`, `size_base`, and `vip` under medium arrival pressure. | The baseline is mainly a reference point. It shows that Table C can become a bottleneck, and that Single Snake is slightly more stable when pressure increases. |
| More VIP | Increased the VIP proportion from the baseline setting to test whether priority service improves global performance. | More VIP customers change who gets seated first, but do not improve overall throughput or average waiting time when table capacity is fixed. |
| More small groups | Increased the share of 1-2 person groups to test table-category imbalance. | Rigid size-based matching can waste larger tables when most customers are small groups. Single Snake performs better because it can use available capacity more flexibly. |
| Long vs short arrival intervals | Compared dispersed arrivals with compressed arrival waves. | Under long intervals, all strategies produce near-zero waiting. Under short intervals, all strategies suffer congestion, but Single Snake has the lowest average wait time and queue length among the tested strategies. |

Overall, the case studies do not prove that one strategy is always best. The main conclusion is that `single_snake` is the safest default when arrival density is uncertain or likely to be concentrated, because it reduces queue build-up better than the other tested strategies. When arrivals are well spread out, strategy choice matters much less because all three approaches can keep waiting time close to zero.

## 10. Limitations and Future Improvements

The project provides a working simulation framework, but it is still a simplified academic model. The main limitations and possible future improvements are summarized below.

| Limitation | Future improvement |
|---|---|
| Code structure is still script-oriented. Some responsibilities, such as input handling, strategy dispatching, analysis, and plotting, are separated into files but could be organized more clearly. | Refactor the project into clearer modules such as data validation, simulation engine, strategies, analysis, and visualization. This would make the code easier to maintain and extend. |
| Input format is still strict. The program expects fixed CSV columns, fixed strategy names, and fixed table categories `A`, `B`, and `C`. | Support more flexible configuration, command-line arguments, custom table labels, and clearer user guidance for fixing invalid input files. |
| The current model still uses fixed `A`/`B`/`C` table categories and assumes no customer walkaway behavior. | Add configurable table categories and customer-abandonment rules for more realistic stress testing. |
| The simulation is simplified and cannot fully reproduce real restaurant behavior. It does not model cancellations, customers leaving the queue, late arrivals, party-size changes, reservations, staff capacity, kitchen speed, or table sharing. | Add more realistic behaviors such as customer abandonment, reservation/no-show handling, dynamic table assignment, table sharing, staff constraints, and peak-hour arrival patterns. |
| Dining time is estimated with a simple formula based mainly on group size. The random mode only adds a small random offset. | Use more realistic probability distributions for dining time, and run repeated simulations with different random seeds to compare average results. |
| Strategy coverage is limited to `single_snake`, `size_base`, and `vip`. Other strategies discussed during research are not fully implemented. | Add hybrid strategies, such as VIP plus single snake, size-based fallback rules, or allowing small groups to use larger tables after a maximum waiting threshold. |
| Evaluation outputs are not fully standardized across all case studies. Some cases have detailed processed summaries, while others rely more on generated figures. | Export consistent summary metrics for every case, including average wait time, queue length, table utilization, occupation rate, and output CSV files. |
| The user workflow is mostly console-based. Users need to type file paths manually and inspect output files separately. | Add command-line options, batch-running support, a default output directory, or a simple GUI/web dashboard for easier use and result comparison. |
