## 2. Analytical Framework

This report evaluates restaurant queue-management strategies under three customer-arrival-density conditions: **Short**, **Medium/Baseline**, and **Long**. The analysis focuses on two core questions:

1. **High-Pressure Resilience:** When customers arrive in a highly concentrated pattern, which strategy can prevent waiting time and queue length from escalating most severely?
2. **Low-Pressure Efficiency:** When customer arrivals are more dispersed, which strategy can deliver a near-zero waiting experience and keep the restaurant operation smooth?

The three queue-management strategies compared in this report are:

| Strategy | Operational Meaning | Main Analytical Focus |
|---|---|---|
| Single Snake | Customers join one shared queue and are allocated to available tables | Whether pooling demand into one queue reduces inefficient waiting |
| Size-based | Customers are separated according to group size or table-size compatibility | Whether matching demand to table type improves seating efficiency |
| VIP | Selected customers receive priority treatment | Whether priority rules improve overall system performance or mainly redistribute waiting |

The three arrival-density scenarios are interpreted as follows:

| Arrival Scenario | Meaning | Analytical Role |
|---|---|---|
| Long interval | Customers arrive more sparsely | Tests whether a strategy can create a near-zero-wait experience |
| Medium / Baseline | Customers arrive at a normal reference density | Provides the comparison benchmark |
| Short interval | Customers arrive very intensively | Tests whether a strategy can resist queue explosion under pressure |

The key performance indicators are:

| Indicator | Meaning | Why It Matters |
|---|---|---|
| Average waiting time | Mean time customers spend waiting before being seated | Direct measure of customer experience |
| Average queue length | Mean number of waiting groups | Measures visible congestion and service pressure |
| Waiting-time distribution | Shape of customer waiting experience | Shows whether most customers wait briefly or whether many suffer long delays |
| Restaurant occupation rate | Overall restaurant occupancy | Shows whether the restaurant runs smoothly or remains underused / overloaded |
| Table-utilization rate | Utilization by table type | Indicates whether specific table types create bottlenecks |

The analysis does not treat low utilization as a simple table-allocation problem. Instead, utilization is interpreted as an operational signal: if waiting time remains low while utilization is moderate, the strategy may be suitable for dispersed arrivals; if utilization is high but waiting time rises sharply, the strategy may be overloaded under concentrated demand.

---

## 3. Overall Performance Comparison Across Datasets

The cross-dataset results show a clear split between the **Short** and **Long** arrival scenarios. Under Short arrivals, all three strategies experience much longer waiting times and larger queues. Under Long arrivals, waiting time and queue length are almost eliminated.

| Dataset | Average Waiting Time (min) | Average Queue Length | Average Table Utilization (%) | Average Occupation Rate (%) |
|---|---:|---:|---:|---:|
| single_long | 0.42 | 0.05 | 25.96 | 25.17 |
| single_short | 136.94 | 31.21 | 56.35 | 54.44 |
| size_base_long | 0.43 | 0.05 | 25.96 | 25.17 |
| size_base_short | 150.73 | 35.44 | 57.63 | 55.71 |
| vip_long | 0.43 | 0.05 | 25.96 | 25.17 |
| vip_short | 150.36 | 35.40 | 57.76 | 55.83 |

The most important pattern is that arrival density dominates the customer experience. Moving from Long to Short arrivals changes average waiting time from approximately **0.42–0.43 minutes** to **136.94–150.73 minutes**. This is not a small operational fluctuation; it is a system-level transition from almost no queuing to severe congestion.

However, the strategies do not perform equally under pressure. In the Short scenario, **Single Snake** produces the lowest average waiting time (**136.94 minutes**) and the lowest average queue length (**31.21 groups**). Size-based and VIP perform worse, with waiting times of **150.73 minutes** and **150.36 minutes**, and queue lengths of **35.44** and **35.40** groups respectively. This suggests that under concentrated arrivals, the shared-queue structure of Single Snake absorbs pressure more effectively than segmentation or priority treatment.

---

## 4. Role of the Medium / Baseline Scenario

The Medium/Baseline scenario is not treated as the final recommendation. Its main function is to act as a **reference point** for measuring how each strategy behaves when arrival density changes. Without the Medium case, the analysis would only show that Short is worse than Long. With the Medium case, it becomes possible to quantify whether each strategy is more resilient under high pressure and more efficient under low pressure.

This section compares each strategy across **Long**, **Medium**, and **Short** arrivals using two measures:

- **Net Change:** the absolute change in waiting time between two density conditions.
- **Percentage Change:** the proportional increase or decrease relative to the Medium/Baseline condition.

The formulas are:

```text
High-pressure net change = T_short - T_medium
High-pressure percentage change = (T_short - T_medium) / T_medium × 100%

Low-pressure net change = T_long - T_medium
Low-pressure percentage change = (T_long - T_medium) / T_medium × 100%
Low-pressure reduction rate = (T_medium - T_long) / T_medium × 100%
```

### 4.1 Cross-Density Quantitative Comparison

| Strategy | Long Avg Wait (min) | Medium Avg Wait (min) | Short Avg Wait (min) | Short - Medium (sec) | Short Growth Rate | Long - Medium (sec) | Long Reduction Rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Single Snake | 0.42 | 42.67 | 136.94 | +5,656 | +220.9% | -2,535 | 99.02% |
| Size-based | 0.43 | 45.55 | 150.73 | +6,311 | +230.9% | -2,707 | 99.06% |
| VIP | 0.43 | 45.40 | 150.36 | +6,298 | +231.2% | -2,698 | 99.05% |

### 4.2 High-Pressure Resilience

High-pressure resilience is judged by the **Short Growth Rate**, because this shows how much waiting time increases when the restaurant moves from Medium/Baseline arrivals to highly concentrated Short arrivals.

The results show that **Single Snake has the strongest high-pressure resilience**. Its waiting time increases by **220.9%**, compared with **230.9%** for Size-based and **231.2%** for VIP. Although all three strategies suffer a major increase in waiting time under Short arrivals, Single Snake has the lowest proportional increase.

This result matters because high-pressure failure is not only about the final waiting-time level. It is also about how quickly waiting time expands once demand becomes concentrated. Single Snake still performs poorly in absolute terms under Short arrivals, with an average wait of **136.94 minutes**, but it suppresses the escalation better than the other two strategies. Compared with the Medium/Baseline case, its waiting time rises by **5,656 seconds**, whereas Size-based rises by **6,311 seconds** and VIP rises by **6,298 seconds**. In practical terms, Single Snake reduces the additional high-pressure waiting burden by roughly **642–655 seconds** compared with the other two strategies.

The likely explanation is demand pooling. A shared queue allows the next available table to be allocated to the next waiting party without locking customers into narrower sub-queues or priority categories. Under Short arrivals, this flexibility becomes valuable because even small inefficiencies compound rapidly. Size-based and VIP do not eliminate this compounding effect; in fact, their higher growth rates suggest that segmentation and priority rules may reduce flexibility when demand becomes extremely concentrated.

Therefore, for **High-Pressure Resilience**, the ranking is:

| Rank | Strategy | Evidence |
|---:|---|---|
| 1 | Single Snake | Lowest Short Growth Rate: **220.9%** |
| 2 | Size-based | Higher Short Growth Rate: **230.9%** |
| 3 | VIP | Highest Short Growth Rate: **231.2%** |

### 4.3 Low-Pressure Flow Efficiency

Low-pressure flow efficiency is judged by the **Long Reduction Rate**, because this shows how much waiting time falls when arrivals become more dispersed than the Medium/Baseline condition.

All three strategies perform extremely well under Long arrivals. Average waiting time falls to approximately **0.42–0.43 minutes**, which is close to a zero-wait experience. The reduction rates are also almost identical: **99.02%** for Single Snake, **99.06%** for Size-based, and **99.05%** for VIP.

Using the strict percentage criterion, **Size-based has the strongest low-pressure flow efficiency**, because it records the highest reduction rate at **99.06%**. VIP follows very closely at **99.05%**, and Single Snake is slightly lower at **99.02%**. The difference is small, but the ranking is still useful because it shows that when customers arrive sparsely, segmentation by group/table size does not create the same pressure problem seen under Short arrivals. Instead, with enough time between arrivals, the system has sufficient capacity to seat customers almost immediately.

In absolute terms, the low-pressure improvement is also substantial. Size-based reduces waiting time by **2,707 seconds** relative to Medium/Baseline, VIP by **2,698 seconds**, and Single Snake by **2,535 seconds**. This means all three strategies move the restaurant very close to zero waiting, but Size-based produces the largest absolute and proportional reduction from its Medium/Baseline position.

Therefore, for **Low-Pressure Flow Efficiency**, the ranking is:

| Rank | Strategy | Evidence |
|---:|---|---|
| 1 | Size-based | Highest Long Reduction Rate: **99.06%** |
| 2 | VIP | Second-highest Long Reduction Rate: **99.05%** |
| 3 | Single Snake | Slightly lower Long Reduction Rate: **99.02%** |

### 4.4 Interpretation of the Medium/Baseline Role

The Medium/Baseline scenario is useful because it separates two different strategic capabilities. **Single Snake is better at resisting the upward shock from Medium to Short arrivals**, while **Size-based is marginally better at converting Medium demand into near-zero waiting under Long arrivals**.

This means the best strategy depends on the restaurant's expected demand pattern. If the restaurant expects customer arrivals to become highly concentrated, the key problem is not table utilization but the prevention of waiting-time explosion. On that criterion, Single Snake is the better option because its waiting-time growth rate is the lowest at **220.9%**. If the restaurant expects customers to arrive more sparsely, the priority shifts to smooth flow and near-zero waiting. On that criterion, Size-based performs slightly better because it achieves the highest reduction rate at **99.06%**.

The Medium/Baseline case should therefore be read as a diagnostic benchmark rather than a standalone operational recommendation. It helps show which strategies are robust when pressure increases and which strategies are efficient when pressure decreases.

---

## 5. High-Pressure Resilience: Short Arrival Scenario

The Short scenario is the most demanding environment in the simulation. Customers arrive in a highly concentrated pattern, so the system must process many groups within a narrow time window. This is where queue-management design matters most.

| Strategy | Average Waiting Time (min) | Average Queue Length | Main Interpretation |
|---|---:|---:|---|
| Single Snake | 136.94 | 31.21 | Best resilience under pressure |
| Size-based | 150.73 | 35.44 | Higher waiting and longer queue |
| VIP | 150.36 | 35.40 | Priority does not reduce overall congestion |

The data show that **Single Snake is the best-performing strategy under Short arrivals**. It reduces average waiting time by **13.79 minutes** compared with Size-based and by **13.42 minutes** compared with VIP. It also reduces average queue length by approximately **4.2 waiting groups** compared with the other two strategies.

The waiting-time distribution supports this conclusion. Under Short arrivals, waiting times are long for all strategies, but Single Snake shifts the distribution slightly closer to lower waiting values. This matters because the objective is not only to reduce the mean but also to reduce the number of customers who suffer extremely long waits.

Operationally, Single Snake is stronger under pressure because it pools customers into one shared waiting line. This reduces fragmentation. In contrast, Size-based may leave some customers waiting even when capacity exists elsewhere, because customers are tied more tightly to table-size categories. VIP can improve the experience for priority customers, but it does not solve the total-capacity problem. It may even delay non-priority customers when pressure is high.

Therefore, under high pressure, the core conclusion is clear: **Single Snake is the most resilient strategy because it produces the lowest waiting time, the shortest queue, and the lowest waiting-time growth rate from Medium to Short arrivals.**

---

## 6. Low-Pressure Efficiency: Long Arrival Scenario

The Long scenario represents a low-pressure environment where customers arrive with more time between groups. The key question is which strategy can provide a near-zero waiting experience and maintain smooth operation.

| Strategy | Average Waiting Time (min) | Average Queue Length | Main Interpretation |
|---|---:|---:|---|
| Single Snake | 0.42 | 0.05 | Near-zero waiting |
| Size-based | 0.43 | 0.05 | Near-zero waiting with highest reduction rate |
| VIP | 0.43 | 0.05 | Near-zero waiting |

The results show that all three strategies perform almost identically under Long arrivals. Average waiting time stays below **0.5 minutes**, and the average queue length is only **0.05 groups**. This means that most customers are seated almost immediately.

Using the percentage-reduction criterion, **Size-based is marginally the best low-pressure strategy**, because its waiting time falls by **99.06%** from Medium/Baseline to Long. VIP is almost identical at **99.05%**, while Single Snake records **99.02%**. The difference is small enough that all three can reasonably be described as near-zero-wait strategies under dispersed arrivals.

This finding has an important implication. Under low pressure, the queueing strategy becomes less decisive because the arrival pattern itself gives the restaurant enough time to absorb demand. In other words, the restaurant does not need an especially powerful queue mechanism when demand is naturally spread out. The system has enough breathing room to seat customers smoothly.

However, Size-based receives the strongest low-pressure ranking because it achieves the highest percentage reduction from Medium/Baseline and the largest absolute fall in waiting time. This suggests that when demand is sparse, group/table-size matching can work smoothly because it no longer faces the bottleneck pressure created by concentrated arrivals.

---

## 7. Strategic Recommendation

The recommendation should distinguish between **high-pressure resilience** and **low-pressure efficiency** rather than selecting one strategy in all situations.

| Operational Scenario | Recommended Strategy | Reason |
|---|---|---|
| Short / concentrated arrivals | Single Snake | Lowest Short waiting time, lowest queue length, and lowest waiting-time growth rate (**220.9%**) |
| Long / dispersed arrivals | Size-based | Highest waiting-time reduction rate from Medium to Long (**99.06%**) |
| Uncertain or mixed demand | Single Snake as default | More robust when pressure increases; low-pressure differences are minimal |

The strongest overall recommendation is to use **Single Snake as the default strategy when demand uncertainty exists**. The reason is that the cost of choosing the wrong strategy is much higher under Short arrivals than under Long arrivals. In Long arrivals, all strategies already create near-zero waiting. In Short arrivals, however, the choice of strategy affects whether waiting time grows less severely or becomes even more difficult to control.

Single Snake is not perfect under Short arrivals, but it is the best available option among the three tested strategies. It reduces the average waiting burden and limits the proportional growth in waiting time more effectively than Size-based and VIP. If the restaurant expects peak-hour crowding, event-driven surges, or concentrated arrivals, Single Snake should be prioritized.

Size-based is better suited for stable, low-pressure environments where arrivals are dispersed and table matching can occur without creating delays. VIP should not be selected as the main queue-management strategy if the goal is to reduce overall waiting time. It may help a priority segment, but the aggregate results show that it does not outperform Single Snake under high pressure or Size-based under low pressure.

The final conclusion is therefore conditional but clear: **Single Snake is the strongest high-pressure strategy, Size-based is marginally the strongest low-pressure strategy, and Single Snake is the safest default when the restaurant faces uncertain arrival density.**
