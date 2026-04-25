# Final Report 

## Restaurant Queue Simulation Project

### 1. Introduction

Restaurant queue management is a common problem in busy dining environments. A restaurant must decide how to seat customers with different party sizes, arrival times, and service priorities while making efficient use of limited table resources. If the queue is managed poorly, customers may wait too long, tables may remain underused, and the restaurant may lose both revenue and customer satisfaction.

This project addresses that problem through simulation. Instead of designing a front-end reservation system, the project focuses on the operational logic behind restaurant queue management. The main goal is to compare different queue strategies in a unified Python framework and to analyse how strategy choice affects waiting time, seating order, and table utilization.

### 2. Research Background

The research stage of the project was broad and intentionally divided across several queue-management ideas and real-world applications. Based on the materials in the `Research` folder, the project began from four strategic directions.

#### 2.1 Single Snake Queue

The single snake strategy is based on the idea of a single shared waiting line feeding multiple service resources. The research emphasized two major strengths of this approach. First, it reduces the unfairness created when customers choose different lines with different speeds. Second, it improves consistency because all waiting demand is pooled together. The related case study connected this idea to digital queueing practices used in large restaurant brands such as Haidilao.

#### 2.2 VIP Queue

The VIP strategy was studied as a differentiated-service model. Its main purpose is not only operational efficiency but also business prioritization. In this approach, customers with higher value or membership status receive priority when tables become available. The research highlighted the trade-off between commercial value and perceived fairness, and connected this logic to systems such as THE GULU, where priority treatment can coexist with categorized table queues.

#### 2.3 Size-Based / Multi-Queue Strategy

The size-based strategy separates customers according to party size and then matches them to different table categories. This idea was motivated by the inefficiency of seating small groups at oversized tables or forcing large groups to wait unnecessarily when small tables remain idle. The research associated this strategy with digital queueing ecosystems such as Meituan and KeeTa, where segmentation and matching are central to operational efficiency.

#### 2.4 Table Sharing

The research also explored table sharing as a further extension of queue optimization. In this model, separate customer groups may share available seating space in order to increase occupancy and reduce waiting time. Although the current repository does not yet implement a table-sharing algorithm, this research direction remained important because it broadened the project beyond conventional first-come-first-served logic and highlighted the possibility of future expansion.

#### 2.5 Research Contribution to the Final System

Taken together, the research stage shaped the final implementation in two ways. First, it established the main performance concerns of the project: fairness, waiting time, table utilization, and service priority. Second, it provided the conceptual basis for selecting the three strategies that were actually implemented in code: `single_snake`, `vip`, and `size_base`. In other words, the final code reflects a narrowed and more feasible subset of the original research scope.

### 3. Modeling Approach

The modeling stage translated the research ideas into a simulation structure that could be executed repeatedly on different datasets.

#### 3.1 Basic Entities

The simulation uses two core datasets:

- restaurant data, including `name`, `strategy`, `open_time`, `table_size`, and `table_number`
- customer data, including `index`, `restaurant`, `vip`, `number`, and `arrival_time`

In the current model, restaurant tables are grouped into three abstract categories:

- `A` for small tables
- `B` for medium tables
- `C` for large tables

Customers are then matched to these categories according to group size.

#### 3.2 Time and Service Assumptions

The system adopts a discrete-time simulation. Time advances in integer steps, and all arrivals up to the current time step are processed together. Dining time is estimated during preprocessing using the following formula:

`dinning_time = number * 10 + 20 + random_offset`

This means larger parties are assumed to occupy tables for longer periods. The model is intentionally simplified so that the queue logic remains clear and comparable across strategies.

#### 3.3 Queue-State Design

The central modeling idea is the shared queue state defined in `queue_structure.py`. The `State` class stores:

- occupied tables as min-heaps ordered by leave time
- VIP waiting queues by table type
- non-VIP waiting queues by table type

This design allows the simulation to repeatedly perform three operations:

1. release tables when a dining party leaves
2. add newly arrived customers into the correct queue
3. assign available tables according to the selected strategy

#### 3.4 Strategy Scope

Although the original research considered four strategic directions, the implemented modeling scope was reduced to three executable strategies:

- `single_snake`
- `vip`
- `size_base`

Table sharing remained at the conceptual research level and was not developed into a full simulation module.

### 4. Division of Work

The `Project Plan` shows that the team organized the project around five stages: research, problem modeling, code realization, case studies, and report writing. The work was distributed across four members: Yao Lijia, Yu Wei, Jiang Hongyi, and Zhang Zhanhao.

The planned division of labor can be summarized as follows:

| Member | Planned Research Focus | Planned Modeling / Coding Focus | Planned Report Focus |
|---|---|---|---|
| Yao Lijia | VIP strategy, THE GULU | File input, database management, data model, data generation | Vision, optimization, and data-model explanation |
| Yu Wei | Size-based queue, Meituan / KeeTa | Algorithm 1 and 2, sample testing | Problem definition, significance, and algorithm explanation |
| Jiang Hongyi | Single snake and table sharing, Meiwei Bu Yong Deng | Algorithm 3 and 4, scenario design | Evaluation, limitations, and algorithm explanation |
| Zhang Zhanhao | Single snake strategy, Haidilao | File output, case simulation, output analysis | Comparative analysis and case-simulation explanation |

This planned structure is also reflected in the repository itself. The folder layout moves from `Plan` to `Research`, then to `Modeling&Coding`, `Testing`, and finally `Final_report`, which shows a clear workflow from conceptual planning to implementation and evaluation.

### 5. Code Logic and Implementation

The codebase in `Modeling&Coding` contains the main implementation of the project. Read together with the testing files, it shows that the project developed not only queue algorithms, but also a basic data pipeline, result analysis functions, and visualization scripts.

#### 5.1 Main Program Flow

The entry point is `main.py`. The program first asks the user whether dining time should be random or fixed, and then asks how data should be loaded. The supported input modes are:

- manual input from the console
- CSV input
- default CSV files

After loading data, the program sends the restaurant and customer datasets into the packaging and simulation pipeline. It then performs performance analysis and generates several visual outputs.

#### 5.2 Data Input and Preprocessing

The file `io_file.py` is responsible for:

- reading restaurant and customer CSV files
- reading structured console input
- preprocessing dining time
- resetting restaurant open time to the earliest customer arrival
- dispatching each restaurant to the correct queue strategy

The `package()` function is the main controller for strategy execution. It groups data by restaurant, reads the strategy name, calls the corresponding algorithm module, and writes the results back into the customer table. The main output columns are:

- `final_wait_time`
- `start_service_time`
- `leave_time`

These three fields form the basis for later analysis and visualization.

#### 5.3 Shared Queue Structure

The `State` class in `queue_structure.py` is the common infrastructure used by multiple strategies. Occupied tables are stored as min-heaps, while waiting customers are stored in queues. This structure makes it possible to separate strategy logic from state management. Instead of each algorithm managing its own low-level data structures independently, all strategies use the same core representation of queue state.

This design is important because it gives the project a modular structure. It also makes it easier to compare strategies fairly, since they all operate on the same basic customer and table model.

#### 5.4 Implemented Queue Strategies

##### Single Snake

The `strategy_single_snake.py` module creates one global waiting queue for all customers. At each time step, the algorithm checks whether a suitable table is available for each waiting group, beginning with the minimum table size that can accommodate that group. This strategy is the closest implementation of pooled waiting among the implemented modules.

##### VIP

The `strategy_vip.py` module first assigns each customer to a table category according to group size. Within each table type, the algorithm serves the VIP queue before the non-VIP queue. This means priority operates locally inside each table category rather than globally across the whole restaurant.

##### Size-Based

The `strategy_size_base.py` module also assigns customers to table categories according to party size, but does not distinguish VIP customers. Each category therefore follows a standard first-in-first-out rule. Among the three implemented strategies, this one most directly reflects the multi-queue logic developed in the research stage.

#### 5.5 Result Analysis

The file `output_file.py` provides the main numerical analysis layer. For each restaurant, it prints:

- maximum waiting time
- minimum waiting time
- average waiting time
- average occupation rate
- minute-by-minute occupation detail

This means the project already contains the beginnings of an evaluation framework, even though the final case-based comparison has not yet been written into the report.

#### 5.6 Visualization Layer

Several plotting scripts extend the project beyond raw table output:

- `visualise.py` plots occupation rate over time
- `plot_table_utilization_line.py` plots time-series table utilization
- `plot_table_utilization_bar.py` plots average utilization by table type
- `plot_waiting_time_density.py` plots the density of customer waiting times
- `plot_queue_length_over_time.py` plots queue length over time

These files show that the project aimed not only to simulate queue behavior, but also to present it in a form suitable for comparison and interpretation.

#### 5.7 Testing Assets

The `Testing` folder contains both a testing description and a data-generation script. The file `data_generate.py` defines three testing scales:

- `small`
- `medium`
- `large`

The repository already includes generated CSV datasets for all three scales. Based on the current files:

- the small dataset contains 3 restaurants and 194 customer groups
- the medium dataset contains 14 restaurants and 1,806 customer groups
- the large dataset contains 75 restaurants and 15,462 customer groups

This testing setup shows that the project was designed to move beyond toy examples and to explore the behavior of different strategies under larger workloads.

### 6. Case Study and Limitation Analysis

This section is intentionally left blank for now.

The final report will later add case-based simulation discussion and limitation analysis after the team completes the corresponding case studies.

### References

ArchDaily. (2024). *Beyond private dining: Exploring the communal table as public space infrastructure*. https://www.archdaily.com/1034907/beyond-private-dining-exploring-the-communal-table-as-public-space-infrastructure

Gorilla Group Limited. (n.d.). *THE GULU official website*. https://web.thegulu.com/

Gross, D., Shortle, J. F., Thompson, J. M., & Harris, C. M. (2018). *Fundamentals of queueing theory* (5th ed.). Wiley.

KeeTa. (n.d.). *KeeTa app*. https://apps.apple.com/hk/app/keeta/id1666524103

Little, J. D. C. (1961). A proof for the queuing formula: L = λW. *Operations Research*.

Meituan. (n.d.). *Official website*. https://about.meituan.com/en

Meituan Tech. (2020). *Meituan delivery dispatch algorithm*. https://tech.meituan.com/2020/07/16/meituan-delivery-dispatch-algorithm.html

Mwee. (n.d.). *Meiwei Bu Yong Deng official website*. https://mwee.cn/

Qminder. (n.d.). *Queueing theory guide*. https://www.qminder.com/blog/queue-management/queuing-theory-guide/

Tiwari, S. K., & Gupta, V. K. (2016). *M/M/S queueing theory model to solve waiting line and to minimize estimated total cost*. *International Journal of Science and Research*.

Wharton Faculty. (2017). *At your service on the table: Impact of tabletop technology on restaurant performance*. https://faculty.wharton.upenn.edu/wp-content/uploads/2017/09/2017.9.10_Tabletop_For_Submission_WithNames.pdf

Wikipedia contributors. (n.d.). *Table sharing*. Wikipedia. https://en.wikipedia.org/wiki/Table_sharing
