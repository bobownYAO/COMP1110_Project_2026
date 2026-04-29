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

#### 2.4 Research Contribution to the Final System

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
| Yao Lijia | VIP strategy, THE GULU | File input, database management, data model, data generation, Algorithm 1, video demo| Vision, optimization, and data-model explanation |
| Yu Wei | Size-based queue, Meituan / KeeTa | Algorithm 2, sample testing, group report writing | Problem definition, significance, and algorithm explanation |
| Jiang Hongyi | Single snake and table sharing, Meiwei Bu Yong Deng | Algorithm 3, scenario design | Evaluation, limitations, and algorithm explanation |
| Zhang Zhanhao | Single snake strategy, Haidilao | File output, case simulation, output analysis | Comparative analysis and case-simulation explanation |

This planned structure is also reflected in the repository itself. The folder layout moves from `Plan` to `Research`, then to `Modeling&Coding`, `Testing`, and finally `Final_report`, which shows a clear workflow from conceptual planning to implementation and evaluation.

### 5. Code Logic and Implementation

The codebase in `Modeling&Coding` contains the main implementation of the project. Read together with the testing files, it shows that the project developed not only queue algorithms, but also a basic data pipeline, result analysis functions, and visualization scripts.

#### 5.1 Main Program Flow

The executable workflow of the project contains three connected stages: data preparation, simulation execution, and result presentation.

Before the main simulation begins, the project also provides a separate data-generation utility in `Testing/data_generate.py`. This script is used to generate synthetic restaurant and customer CSV files at three scales, namely `small`, `medium`, and `large`. In this sense, the overall pipeline does not begin only from manual or file input; it may also begin from automatically generated testing data prepared in advance for later simulation.

The main simulation entry point is `main.py`. The program first asks the user whether dining time should be random or fixed, and then asks how data should be loaded. The supported input modes are:

- manual input from the console
- CSV input
- default CSV files

After loading data, the program sends the restaurant and customer datasets into the packaging and simulation pipeline. It then performs performance analysis and, at the final stage, generates several visualization outputs.

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

It is therefore more accurate to view `data_generate.py` not as an isolated helper file, but as the first stage of the testing-oriented workflow. It prepares the input data used by the rest of the system and supports repeated simulation under different workload scales.

#### 5.8 Output and Visualization Code

In addition to numerical output printed in the terminal, the project also includes a dedicated visualization layer for the final stage of analysis. After the main simulation is completed, `main.py` calls several plotting modules to present the results in graphical form.

These visualization files include:

- `visualise.py`, which draws occupation-rate curves over time
- `plot_table_utilization_line.py`, which presents table utilization as a time-series line chart
- `plot_table_utilization_bar.py`, which compares average utilization across table types
- `plot_waiting_time_density.py`, which shows the distribution of customer waiting times
- `plot_queue_length_over_time.py`, which visualizes the change of queue length over time

This means that the output stage of the project is not limited to raw simulation records. Instead, the system attempts to transform the results into interpretable charts that make it easier to compare restaurant behavior and strategy performance. From the perspective of the final report, these visualization scripts are important because they provide the basis for future case-study discussion and comparative analysis.

### 6. Case Study and Limitation Analysis

#### 6.1 Case Study Design

The testing stage uses four groups of case studies to examine how the queue strategies behave under different demand conditions. Each case is built around the same basic simulation scale: five restaurants, 200 customer groups per restaurant, and fixed dining time. This gives each tested strategy 1,000 customer groups in total, while keeping the restaurant capacity structure comparable across cases.

The evaluation focuses on the same indicators used by the output and visualization modules:

- average, median, and maximum waiting time
- table occupation rate and table utilization
- queue length over time
- waiting-time distribution

The four case groups are not intended to prove that one strategy is always best. Instead, they show how the same strategy may perform differently when demand pressure, VIP ratio, or party-size distribution changes.

#### 6.2 Baseline Case: Normal Demand

##### 1. Executive Summary

This report presents a technical evaluation of three queuing strategies— Single Snake ,  Size-based , and  VIP Priority —benchmarked against varying arrival densities. The analysis adopts a dual-lens framework:  High-Pressure Resilience  (evaluating performance during compressed arrival waves) and  Low-Pressure Efficiency  (evaluating flow during dispersed arrivals).

Key Findings:

* High-Pressure Resilience:  Single Snake is the most robust strategy for concentrated arrivals. It demonstrates superior resilience by suppressing waiting-time escalation, maintaining an average wait of 136.94 minutes compared to the >150-minute averages seen in Size-based and VIP strategies.
* Low-Pressure Efficiency:  Under dispersed conditions, strategy choice becomes secondary to operational simplicity. All strategies achieve near-zero waiting (~0.42 minutes), indicating that the system possesses sufficient capacity to absorb demand regardless of the queuing rule.
* Strategic Conclusion:  Single Snake is recommended as the "safest default." It provides critical protection against "runaway" congestion during peak waves without incurring any performance penalties during off-peak periods.

##### 2. Analytical Framework

To evaluate these strategies, we prioritize customer-side outcomes over mere resource allocation. The following metrics serve as the primary diagnostic tools:

| Metric | Significance | Interpretation Criteria |
| ------ | ------ | ------ |
| Average Wait Time | Direct quantitative measure of customer-side friction. | Lower is better, specifically under short-interval pressure. |
| Average Queue Length | Indicates the stability of the system. | Smaller, shorter-lived queues indicate higher strategy resilience. |
| Waiting-time Density | Visualizes the distribution of the customer experience. | The left side of the distribution matters more than a single mean ; higher density at low wait times is preferred. |
| Table Utilization | A diagnostic variable for resource flow. | Used to identify bottlenecks; high values explain why congestion occurs. |

##### 3. Resource Utilization Efficiency

Analysis of physical capacity occupancy reveals that utilization is a diagnostic indicator rather than a primary performance measure.

* Occupation Rates (Restaurant 1):  In the baseline scenario, Single Snake maintains a 62.9% occupation rate, while Size-based and VIP Priority strategies utilize a higher 65.2%.
* Critical Resource Bottleneck:  Regardless of the strategy, Table Type C is a persistent bottleneck. Its utilization consistently exceeds 90%, specifically ranging from  91.9% to 95.3%  in Restaurant 1. This extreme utilization explains the persistence of queues even when Table Types A or B remain available.

![Baseline single snake occupation rate](../Testing/Baseline/single/baseline_single_occupation_rate.png)
![Baseline size_base occupation rate](../Testing/Baseline/size_base/baseline_size_base_occupation_rate.png)
![Baseline vip occupation rate](../Testing/Baseline/vip/baseline_vip_occupation_rate.png)

##### 4. Queue & Waiting Experience

A comparative analysis across arrival densities reveals how Single Snake suppresses the escalation of wait times during the transition from baseline to high-pressure conditions.

| Strategy | Baseline (Medium) | High-Pressure (Short) | Growth Rate (%) |
| ------ | ------ | ------ | ------ |
| Single Snake | 42.67 min | 136.94 min | +220.9% |
| Size-based | 45.55 min | 150.73 min | +230.9% |
| VIP Priority | 45.40 min | 150.36 min | +231.2% |

Analytical Synthesis:

* Specific Performance (R3):  In Restaurant 3, Single Snake achieved an average wait of 70.48 minutes, significantly outperforming the 80.47 minutes recorded under the Size-based strategy.
* The "Shared Queue" Mechanism:  Single Snake’s resilience stems from its single shared queue, which reduces the mismatch between customer group sizes and service opportunities. This flexibility prevents the system from "locking" resources to specific segments while others remain idle.
* Resilience and Inherited Delay:  Single Snake’s growth rate (+220.9%) is notably lower than the >230% observed in alternatives. By suppressing the peak queue size, it limits the  inherited delay —the phenomenon where later arrivals inherit the congestion created by earlier waves—thereby reducing the majority burden by approximately 9% compared to alternatives.

![Baseline single snake waiting-time density](../Testing/Baseline/single/baseline_single_waiting_time_density.png)
![Baseline size base waiting-time density](../Testing/Baseline/size_base/baseline_size_base_waiting_time_density.png)
![Baseline vip waiting-time density](../Testing/Baseline/vip/baseline_vip_waiting_time_density.png)

##### 5. Final Recommendation

Based on the simulation data, the optimal operational logic is summarized in the following decision matrix:

| Condition | Recommended Strategy | Rationale |
| ------ | ------ | ------ |
| High-Pressure | Single Snake | Lowest average wait time and queue length; best at suppressing "runaway" congestion. |
| Low-Pressure | Any Strategy | All strategies deliver near-zero waiting (~0.42m). Operational simplicity is the priority. |
| Overall Logic | Single Snake | The  Safest Default . It offers a ~9% performance advantage during peaks without a low-pressure disadvantage. |

#### 6.3 More VIP Case: Priority Pressure

##### 1 Executive Summary

This evaluation synthesizes the core findings of a simulation comparing a "Baseline" scenario (20% VIP proportion) with a "More VIP" scenario (50% VIP proportion). The data confirms a state of  Global Efficiency Invariance : despite a 150% increase in the VIP segment, system-wide performance metrics—total throughput and aggregate wait times—remain strictly static. These results indicate that global efficiency is fundamentally dictated by physical system capacity rather than the nuances of customer segmentation or priority logic.

##### 2 Analytical Framework

To evaluate the strategic impact of queue management, we utilize two primary operational lenses:

| Decision Lens | Arrival Condition | Main Interpretation |
| ------ | ------ | ------ |
| High-Pressure Resilience | Short interval / concentrated arrivals | Measures the system's ability to suppress sharp waiting-time escalation. |
| Low-Pressure Efficiency | Long interval / dispersed arrivals | Evaluates whether the system maintains a "near-zero wait" and stable flow. |

Metric Prioritization:  Instead of relying solely on occupation rates, this report prioritizes  Waiting-Time Density  and  Average Queue Length . These metrics provide a more accurate diagnostic of the customer experience, revealing the distribution of delays and the persistence of congestion that simple utilization figures often mask.

##### 3 Resource Utilization Efficiency

Analysis of internal capacity across both scenarios reveals a hard ceiling on operational performance.

* System-Wide Occupation:  The  Overall Occupation Rate for R1  remains fixed at  65.2% , regardless of whether the VIP proportion is 20% or 50%.
* Structural Bottleneck:  The  Table Utilization Rate for Table C  peaks at  95.3%  in both simulations.

![Baseline vip occupation rate](../Testing/Baseline/vip/baseline_vip_occupation_rate.png)
![more VIP occupation rate](../Testing/MoreVIP/vip/moreVIP_vip_occupation_rate.png)
![More VIP table utilization](../Testing/MoreVIP/vip/moreVIP_vip_table_utilization_bar.png)

Strategic Insight:  Table C represents a structural hardware bottleneck. The data confirms that no amount of software-based priority shifting can bypass the physical unavailability of specific table resources. The system is capacity-constrained, not priority-constrained.

##### 4 Queue & Waiting Experience

A contrast of customer-side metrics reveals that the aggregate wait remains indifferent to the VIP ratio.

* Mean Waiting Time (R1):  Recorded at  55.65 minutes  in both scenarios (as visualized in the baseline density distribution).
* Average Queue Length (R1):  Remains steady at  12.66 groups .

![More VIP waiting-time density](../Testing/MoreVIP/vip/moreVIP_vip_waiting_time_density.png)
![More VIP queue length](../Testing/MoreVIP/vip/moreVIP_vip_queue_length_over_time.png)

The "Wait-Time Paradox":  While the identity of the customer in the seat changes (favoring VIPs), the  Table Turnover Rate  remains stagnant because service times and table counts are constant. While individual VIPs may perceive a faster entry, the aggregate system does not clear the queue any faster.

##### 5 Structural Analysis: Why Global Metrics Remain Static

The invariance observed when increasing VIPs from 20% to 50% is driven by three technical factors:

* Fixed Capacity:  Table counts act as an unyielding hard constraint.
* Arrival Invariance:  The total volume and pattern of demand are identical in both simulations.
* Priority Dilution:  This is the most critical strategic takeaway. As the VIP proportion increases toward 50%, the mathematical advantage of priority is diluted. If half the guest base is "priority," the priority queue itself becomes a new bottleneck, effectively nullifying the benefit of the status.
* Re-shuffling vs. Reduction:  Priority strategies only  re-shuffle  the order of service; they do not increase the  rate  of service.

##### 6 Final Recommendation

Strategic Outlook:

* Marketing vs. Operations:  Management must view VIP scaling exclusively as a  loyalty marketing tool  to manage perception. It is not an operational tool and will not resolve congestion.
* The Operational Mandate:  For high-pressure arrival windows, the  "Single Snake"  strategy is the strongest resilience option. The data shows that Single Snake reduces average wait times by approximately  9%  (136.94 min) compared to VIP-based strategies (150.36 min) under extreme pressure.
* Policy Direction:  Do not invest operational resources into segmenting queues during peak hours; instead, implement a Single Snake baseline to maximize the service rate and suppress queue escalation.

#### 6.4 More Small Groups Case: Table-Category Bottleneck

##### 1 Executive Summary

In scenarios where 1-2 person groups represent 90% of the customer mix, the choice of queuing strategy dictates the system's ability to handle arrival volatility. This analysis finds that while extreme pressure (short-interval arrivals) causes significant delays across all models, the  Single Snake  strategy demonstrates superior  High-Pressure Resilience . By utilizing "stochastic pooling"—allowing the dominant customer segment to access any available capacity—Single Snake suppresses the escalation of waiting times more effectively than rigid, size-based models.

The Bottom Line:  Single Snake is the most resilient strategy for restaurants facing concentrated arrival waves. It yields an average wait time of 136.94 minutes under high pressure, outperforming the Size-based strategy (150.73 minutes) by limiting the catastrophic queue buildup inherent in rigid allocation.

##### 2 Analytical Framework

To determine operational viability, we evaluate performance through two distinct decision lenses:

* High-Pressure Resilience:  Measured during short-interval/concentrated arrivals to assess a strategy's ability to suppress sharp waiting-time escalation.
* Low-Pressure Efficiency:  Measured during long-interval/dispersed arrivals to ensure a frictionless, near-zero-wait experience.

| Key Metric | Definition | Purpose in Analysis |
| ------ | ------ | ------ |
| Average Wait Time | Mean customer wait from arrival to seating. | Primary indicator of service speed and customer burden. |
| Average Queue Length | Mean number of groups waiting in the system. | Indicates if congestion is temporary or persistent. |
| Waiting-time Density | Statistical distribution of wait times. | Shows the burden on the majority of the customer base. |
| Occupation Rate | Percentage of total seats occupied. | Diagnostic of flow efficiency and resource utilization. |

##### 3 Wait Time and Queue Analysis

Analysis of the simulation data reveals that Single Snake provides the most robust defense against arrival surges. While no strategy completely eliminates congestion under extreme concentration, Single Snake maintains a lower threshold of failure.

| Strategy | Avg Wait Time (Short) | Avg Queue Length (Short) | Short Growth (%)* |
| ------ | ------ | ------ | ------ |
| Single Snake | 136.94 min | 31.21 groups | +220.9% |
| Size-based | 150.73 min | 35.44 groups | +230.9% |
| VIP | 150.36 min | 35.40 groups | +231.2% |
| *Growth relative to the Medium/Baseline condition. |  |  |  |

![Average Wait Time single snake](../Testing/Testdata-MoreA/single_normal/single_normal_waiting_time_density.png)
![Average Wait Time size base](../Testing/Testdata-MoreA/size_base_normal/size_base_normal_waiting_time_density.png)

The Mechanism of Resilience:  The Single Snake strategy reduces average wait times by approximately 9.1% compared to the Size-based model. More importantly, it achieves an 11.9% reduction in average queue length. Because Single Snake pools all arrivals into one shared line, it avoids the "mismatch" penalty of Size-based systems, where small groups wait in an overloaded queue while larger tables sit idle.

##### 4 Resource Utilization Efficiency

A deep dive into Restaurant R1 data highlights the "Utilization Paradox." In a Size-based system, high seat counts do not guarantee throughput if the queue logic is too rigid.

* Single Snake (R1):  Maintains an average table utilization of  89.8% , effectively converting capacity into service.
* Size-based (R1):  Occupation rate collapses to  30.8% .

This disparity is driven by the  Type C Paradox : In a 90% small-group surge, Size-based logic forbids 1-2 person groups from occupying 5-6 person tables (Type C). In R1 simulations, this resulted in  0.0% utilization for Table Type C , representing total resource waste while the small-group queue surged to over 35 groups. Single Snake's capacity flexibility ensures these resources are pooled to absorb the 90% majority.

![Average Table Utilization single snake](../Testing/Testdata-MoreA/single_normal/single_normal_table_utilization_bar.png)
![Average Table Utilization size base](../Testing/Testdata-MoreA/size_base_normal/size_base_normal_table_utilization_bar.png)

##### 5 Final Recommendation

The "Senior Analyst" recommendation prioritizes the suppression of system failure during peak periods.

| Criterion | Best Strategy | Reasoning |
| ------ | ------ | ------ |
| High-Pressure Resilience | Single Snake | Lowest wait-time growth (+220.9%) and smallest queue burden. |
| Low-Pressure Efficiency | Size-based | Marginally higher reduction rate (99.06%), though practically negligible. |

Final Command:   Single Snake should be the default operating logic. It offers the strongest protection against waiting-time escalation (+220.9% growth vs. +230.9% for Size-based) and maintains operational fluidity across all arrival densities without the resource waste seen in size-restricted queuing.

#### 6.5 Long vs Short Arrival Intervals: Demand Intensity

The long/short case compares two arrival-pressure settings. The long-interval datasets spread the same total demand over a much wider time window, while the short-interval datasets compress arrivals into a shorter period. The customer mix remains the baseline distribution, with A/B/C groups at 61.1%, 18.6%, and 20.3%.

The summary metrics show a sharp difference:

| Dataset | Strategy | Average waiting time | Median waiting time | Maximum waiting time | Average queue length |
|---|---|---:|---:|---:|---:|
| single_long | single_snake | 0.42 min | 0.00 min | 55.00 min | 0.05 |
| size_base_long | size_base | 0.43 min | 0.00 min | 55.00 min | 0.05 |
| vip_long | vip | 0.43 min | 0.00 min | 55.00 min | 0.05 |
| single_short | single_snake | 136.94 min | 94.00 min | 812.00 min | 31.21 |
| size_base_short | size_base | 150.73 min | 113.50 min | 768.00 min | 35.44 |
| vip_short | vip | 150.36 min | 122.50 min | 758.00 min | 35.40 |

![Long/short average wait-time comparison](../Testing/Testdate-longshort/restaurant_run_outputs_latest_long_short_fast/comparison_avg_wait_time.png)

This comparison shows that arrival intensity is one of the strongest drivers of queue performance. Under long arrival intervals, all three strategies perform almost identically, with average waiting time around 0.42 to 0.43 minutes. In this low-pressure setting, strategy choice matters less because tables usually become available before a large queue forms.

Under short arrival intervals, the same restaurant capacity becomes heavily stressed. Average waiting time rises to 136.94 minutes for single snake, 150.73 minutes for size-based, and 150.36 minutes for VIP. The single-snake strategy remains the best of the three in average waiting time, but the large increase across all strategies shows that algorithm choice cannot fully compensate for demand that exceeds service capacity. In real operations, this would suggest the need for capacity expansion, time-slot control, estimated-wait communication, or customer-flow smoothing.

#### 6.6 Limitation Analysis

The case studies are useful for comparing strategy behavior, but several limitations remain. First, all datasets are synthetic. They are helpful for controlled testing, but they cannot fully represent real restaurant behavior, such as meal-period peaks, group cancellations, walk-away customers, or customers changing party size.

Second, the case analysis uses fixed dining time. This makes the strategies easier to compare, but real dining time is variable and affected by menu type, service speed, and customer behavior. A more realistic model would run repeated simulations with random dining time and compare the average result across multiple random seeds.

Third, the current table-category model is rigid. The MoreA case shows that strict matching between party size and table category can create bottlenecks when demand is concentrated in one category. A future version could allow controlled fallback rules, such as seating a small group at a larger table after a maximum waiting threshold.

Fourth, the model assumes all customers eventually wait until they are served. In real restaurants, long waits may cause customers to leave. Adding abandonment behavior would make the queue simulation more realistic and would also change how waiting-time results should be interpreted.

Finally, the available testing outputs are not equally detailed across all cases. The long/short and MoreA cases include processed CSV summaries that support exact numerical comparison, while the baseline and MoreVIP cases rely more heavily on generated figures and input-distribution analysis. For a stronger evaluation, future tests should export the same summary metrics for every case.

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
