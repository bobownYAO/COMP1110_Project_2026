# Project Plan

Initial project plan including task breakdown, role assignment, timeline, and milestone planning for the restaurant queue simulation project.

## Final Scope Summary

The final repository implements Topic C, Restaurant Queue Simulation, as a Python-based discrete-time simulation. The implemented scope is intentionally limited to text/CSV input and file-based output. It does not implement a GUI, database, reservation system, customer walkaway behavior, or table sharing.

The final simulation compares three executable queue strategies:

- `single_snake`: one pooled queue where groups can use the smallest suitable available table, including larger table categories when needed.
- `size_base`: separate FIFO queues by group/table category.
- `vip`: separate queues by group/table category, with VIP customers served before non-VIP customers within the same category.

## Final Output Metrics

The final code reports and exports the following evidence for each restaurant run:

- served and unserved customer-group counts
- maximum and average waiting time
- average and maximum queue length
- average occupation rate
- total tables and total seats
- generated charts for occupation rate, table utilization, waiting-time density, and queue length over time

The main summary file produced by `Modeling&Coding/main.py` is:

```text
Modeling&Coding/outputs/summary_metrics_by_restaurant.csv
```

## Mapping From Original Algorithm Labels

The original project plan used broad labels such as Algorithm 1, Algorithm 2, Algorithm 3, and Algorithm 4 during planning. The final code uses the following concrete strategy names instead:

| Planning label | Final implementation name | Main file |
|---|---|---|
| VIP / priority strategy work | `vip` | `Modeling&Coding/strategy_vip.py` |
| Size-based queue strategy work | `size_base` | `Modeling&Coding/strategy_size_base.py` |
| Single snake queue strategy work | `single_snake` | `Modeling&Coding/strategy_single_snake.py` |
| Table sharing / extra strategy research | Conceptual research only | `Research/Research_JiangHongyi.md`, `Final_report/final_report.md` |

This means the final implementation narrowed the original research directions into three executable strategies plus one conceptual research direction.
