# Final Report

## Restaurant Queue Simulation Project

### Abstract

This project examines the effect of different queue-management strategies on restaurant operations. A Python-based discrete-time simulation framework was developed to model restaurant seating decisions under three representative strategies: `single_snake`, `vip`, and `size_base`. The system reads restaurant and customer data, estimates dining duration, simulates the allocation of tables over time, and records each party's waiting time, service start time, and departure time. The project combines practical research on restaurant queueing systems with a modular computational implementation intended for comparative analysis. This report presents the problem background, project objectives, system design, core algorithms, implementation status, limitations, and directions for further development.

### 1. Introduction

Queue management is a central operational problem in high-demand restaurant environments. Restaurants must balance multiple objectives simultaneously, including the reduction of customer waiting time, the improvement of table utilization, the maintenance of perceived fairness, and the accommodation of customers with different party sizes and service priorities. Although a simple first-come-first-served rule is easy to implement, it does not always produce efficient or commercially desirable outcomes. In practice, many restaurants adopt more flexible queueing policies, such as priority service for selected customers, queue segmentation by party size, or dynamic assignment of tables according to seating capacity.

The present project models these practical ideas in a simplified simulation environment. Rather than focusing on interface design, the project concentrates on algorithmic decision-making and the quantitative consequences of different seating strategies. The result is a simulation framework that can be used to compare alternative queueing policies under a common input format.

### 2. Project Objectives

The project was designed with the following objectives:

- to construct a reusable simulation framework for restaurant queue management
- to model customers, tables, waiting queues, and seating decisions in a structured form
- to implement multiple queue-management strategies within a common architecture
- to generate customer-level output metrics, including waiting time and service timing
- to connect the computational model with real-world queueing practices identified through background research

Accordingly, the main deliverable of the project is not a user interface, but a strategy-comparison simulation engine capable of producing interpretable operational results.

### 3. Research Background

Prior to implementation, the project drew upon several strands of practical and conceptual research related to restaurant queueing. The research materials collected in the repository focus on four major ideas:

- `Single Snake Queue`, which emphasizes pooled waiting and procedural fairness
- `VIP Queue`, which emphasizes differentiated service and priority handling
- `Multi-Queue / Size-Based Queue`, which emphasizes the matching of table capacity to party size

These research directions were relevant because each represents a different operational objective. The single-snake approach is primarily associated with fairness and consistency; VIP queueing is associated with business value and customer segmentation; size-based queueing is associated with efficiency in table allocation; and table sharing is associated with maximizing occupancy. The research stage therefore provided both practical motivation and conceptual guidance for the simulation design.

### 4. System Architecture

The implementation is organized into a set of relatively independent Python modules:

- `main.py`, which serves as the program entry point
- `io_file.py`, which manages data input, preprocessing, and strategy dispatch
- `queue_structure.py`, which defines the shared queue-state abstraction
- `strategy_single_snake.py`, which implements a global waiting-line strategy
- `strategy_vip.py`, which implements VIP-priority allocation within table categories
- `strategy_size_base.py`, which implements size-based first-in-first-out allocation

This modular structure is appropriate for the aims of the project. Shared state management is separated from strategy-specific decision logic, making the codebase easier to understand, maintain, and extend. It also permits additional strategies to be introduced later without requiring a redesign of the entire system.

### 5. Data Model and Assumptions

The simulation relies on two primary input datasets: restaurant data and customer data.

#### 5.1 Restaurant Data

The restaurant dataset includes the following fields:

- `name`
- `strategy`
- `open_time`（by default the open time is 0)
- `table_size`
- `table percentage`
- `table_number`
- `custormer per restaurant`
- `vip percentage`

Within the current model, table sizes are represented by three abstract categories:

- `A`, representing small tables
- `B`, representing medium tables
- `C`, representing large tables

#### 5.2 Customer Data

The customer dataset includes the following fields:

- `index`
- `restaurant`
- `vip`
- `number`
- `arrival_time`

During preprocessing, an additional field, `dinning_time`, is generated. In the current implementation, dining duration is estimated as a function of party size, optionally combined with a random offset:

`dinning_time = number * 10 + 20 + random_offset`

Although this assumption is simplified, it provides a reasonable first approximation in which larger parties generally occupy tables for longer periods.

#### 5.3 Modeling Assumptions

To keep the simulation manageable, several simplifying assumptions are adopted:

- time advances in discrete integer steps
- all customer arrival times are known
- each party occupies exactly one table
- a party may be seated only at a table category with sufficient capacity
- service begins immediately once a suitable table becomes available
- no customers abandon the queue after joining
- table combination and true table-sharing behavior are not yet implemented

These assumptions reduce real-world complexity and improve tractability, but they also limit the realism of the current model.

### 6. Core Data Structure

The shared state of the simulation is implemented in `queue_structure.py` through the `State` class. This class manages two forms of operational information:

- occupied tables, stored as min-heaps ordered by departure time
- waiting queues, stored separately for VIP and non-VIP customers

This structure allows the simulation to answer two recurrent questions efficiently: which tables should be released at the current time step, and which customer should be assigned next under the selected strategy. The use of min-heaps is appropriate because table release is inherently time-ordered. The separation of VIP and non-VIP queues also makes it possible to implement priority rules without modifying the underlying simulation framework.

The `State` abstraction is one of the principal design strengths of the project. It provides a common operational backbone for all implemented strategies and supports code reuse across the system.

### 7. Strategy Design and Implementation

#### 7.1 Single Snake Strategy

The `single_snake` strategy maintains one global waiting queue for all arriving customers. At each time step, the algorithm scans the queue from front to back and attempts to assign each waiting party to the smallest available table category that can accommodate it.

This strategy is attractive for two principal reasons. First, it approximates a fairer waiting process because all customers enter a common queue. Second, it can improve utilization by permitting smaller parties to occupy larger tables when no smaller table is available. However, the strategy still reflects capacity constraints, and therefore strict chronological service is not always preserved in practice.

#### 7.2 VIP Strategy

The `vip` strategy assigns customers to table categories according to party size. Within each table category, VIP and non-VIP customers are placed into separate queues. Whenever a table becomes available, the VIP queue is served before the regular queue for that category.

This approach reflects practices commonly associated with premium service, loyalty programs, or differentiated customer treatment. From an implementation perspective, it is straightforward because priority is enforced locally within each category. Nevertheless, it introduces a clear trade-off: service for higher-priority customers may be improved at the cost of longer waiting times and lower perceived fairness for ordinary customers.

#### 7.3 Size-Based Strategy

The `size_base` strategy also maps customers to the `A`, `B`, and `C` categories according to party size, but it does not distinguish between VIP and non-VIP customers. Each category therefore follows a standard first-in-first-out rule.

This strategy is useful when the primary objective is to match seating capacity closely to party size. Its main advantage lies in its clarity and efficiency of allocation. Its main weakness is reduced flexibility: congestion may arise in one category even when tables in another category remain comparatively underutilized.

### 8. Simulation Workflow

Across all implemented strategies, the simulation follows the same overall processing loop:

1. release any tables whose departure time has been reached
2. add newly arrived customers to the relevant waiting queue
3. allocate available tables according to the selected strategy
4. record each customer's waiting time, service start time, and departure time
5. advance the system clock by one time unit

This workflow provides a consistent foundation for comparing strategies while keeping strategy-specific code focused on allocation logic rather than data handling. The resulting structure is sufficiently clear for further extension and debugging.

### 9. Current Implementation Status

The present repository indicates that the core framework of the project has already been established. At the current stage, the project has achieved the following:

- a reusable queue-state structure has been implemented
- three queue-management strategies have been completed
- restaurant and customer data can be loaded from CSV files
- customer-level timing outputs are generated after simulation
- research materials have been collected to support the conceptual basis of the strategies

These outcomes demonstrate that the project has moved beyond the planning stage and already constitutes a working simulation prototype. The main remaining tasks concern more systematic testing, clearer summary metrics, and stronger presentation of results.

### 10. Case Simulation and Data Summary

This section is intentionally left blank at the current stage.

Case-based simulation results, summary tables, and comparative numerical analysis will be added later after the final testing scenarios have been completed.

### 11. Limitations

Several limitations of the current version should be acknowledged.

- the available sample datasets are limited and do not yet support a comprehensive comparative evaluation
- table sharing was investigated during the research stage but has not yet been implemented as a strategy
- customer behaviors such as reneging, cancellation, and no-show are not represented
- dining-time estimation remains highly simplified and is not based on empirical restaurant data
- the program entry workflow still requires refinement before it can serve as a polished demonstration version

These limitations do not undermine the value of the project, but they define the scope of the present version and indicate where further development is required.

### 12. Future Work

Several extensions would substantially strengthen the project:

- expanding the test datasets so that all strategies can be evaluated under shared scenarios
- calculating summary performance indicators such as average waiting time, maximum waiting time, and table utilization
- adding visualizations to support interpretation of strategy performance
- implementing additional advanced strategies, such as table sharing or hybrid priority rules
- improving the robustness and usability of the main execution workflow

If these improvements are completed, the project could develop from a proof-of-concept simulator into a more persuasive comparative study of restaurant queue-management strategies.

### 13. Conclusion

This project represents a well-defined attempt to model restaurant queue management through simulation. Its main contribution lies in translating practical queueing strategies into modular Python implementations that can be compared within a shared framework. The repository already demonstrates meaningful progress in system design, data modeling, and algorithmic implementation, particularly through its separation of common queue state from strategy-specific logic.

Although the case-based results section remains to be completed, the existing work already provides a solid basis for the final submission. The project is supported by a clear problem definition, relevant background research, and a coherent implementation structure. With the later addition of systematic experimental results and quantitative comparison, the final report will become substantially stronger and more complete.

### References

ArchDaily. (2024). *Beyond private dining: Exploring the communal table as public space infrastructure*. https://www.archdaily.com/1034907/beyond-private-dining-exploring-the-communal-table-as-public-space-infrastructure

Erlang, A. K. (1909). *The theory of probabilities and telephone conversations*.

Gorilla Group Limited. (n.d.). *THE GULU official website*. https://web.thegulu.com/

Gross, D., Shortle, J. F., Thompson, J. M., & Harris, C. M. (2018). *Fundamentals of queueing theory* (5th ed.). Wiley.

Haidilao International Holding Ltd. (2026). *2025 annual results announcement*.

KeeTa. (n.d.). *KeeTa app*. https://apps.apple.com/hk/app/keeta/id1666524103

Little, J. D. C. (1961). A proof for the queuing formula: L = λW. *Operations Research*.

Loh, C. M., Perdana, A., & Lee, K. H. (2024/2025). *From hot pot to high tech: Haidilao’s transformation through digital technologies for sustainable business*.

Lu, G. (2022). *Haidilao’s innovation in using new digital technology to enhance customers’ consumption experience*.

Meituan. (n.d.). *Official website*. https://about.meituan.com/en

Meituan Tech. (2020). *Meituan delivery dispatch algorithm*. https://tech.meituan.com/2020/07/16/meituan-delivery-dispatch-algorithm.html

Mwee. (n.d.). *Meiwei Bu Yong Deng official website*. https://mwee.cn/

Qminder. (n.d.). *Queueing theory guide*. https://www.qminder.com/blog/queue-management/queuing-theory-guide/

TableCheck. (n.d.). *VIPs and foodies*. https://www.tablecheck.com/blog/vips-and-foodies/

Tiwari, S. K., & Gupta, V. K. (2016). *M/M/S queueing theory model to solve waiting line and to minimize estimated total cost*. *International Journal of Science and Research*.

Wharton Faculty. (2017). *At your service on the table: Impact of tabletop technology on restaurant performance*. https://faculty.wharton.upenn.edu/wp-content/uploads/2017/09/2017.9.10_Tabletop_For_Submission_WithNames.pdf

Wikipedia contributors. (n.d.). *Table sharing*. Wikipedia. https://en.wikipedia.org/wiki/Table_sharing
