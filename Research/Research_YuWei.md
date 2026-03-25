# Multi-Queue Strategy Simulation - Concise Research Report

## 1: Strategic Research - Multi-Size Queue Strategy

### Concept & Evolution

The Multi-Size Queueing concept evolved from the limitations of the traditional "First-In, First-Out" (FIFO) single-line system in restaurant management. This older model often led to inefficient table utilization, where a party of two might occupy a table for four, or a large group would wait indefinitely while smaller tables sat empty. The modern strategy, pioneered by digital platforms like Meituan, is a "divide and conquer" framework. It segments customers into parallel virtual queues based on party size (e.g., Small, Medium, Large), matching them to corresponding table inventories. This shifts the core logic from a simple chronological sequence to a dynamic, resource-optimization problem, maximizing table turnover and customer throughput.

### Scope: Best F&B Use Cases

Multi-Size Queuing is most effective in:

- **High-turnover casual dining**: Where maximizing seat utilization per hour is critical (e.g., ramen shops, fast-casual chains).
- **Family-style restaurants**: Venues with a diverse mix of table sizes (2-tops, 4-tops, 8-tops) catering to varied group demographics.
- **High-demand urban venues**: Environments where physical queue space is limited and reducing on-site congestion is a priority.
- **Large-scale establishments**: Such as Chinese dim sum restaurants or hotpot chains where managing hundreds of waiting customers efficiently is key to profitability and customer satisfaction.

### Pros & Cons

| Dimension | Advantages | Disadvantages |
|-----------|------------|---------------|
| **Wait Time** | Significantly reduces average wait time by matching parties to appropriate tables efficiently. | Can lead to "starvation" for less common party sizes (e.g., L-Queue) if their corresponding tables are few. |
| **Table Utilization** | Increases overall table turnover rate by 15-20% by minimizing idle time and size mismatches. | "Downgrade Matching" (e.g., a 2-person party at a 4-top) can reduce potential revenue during peak hours. |
| **Fairness** | Enhances "perceived fairness" as customers see queues for other party sizes moving independently. | Requires clear communication to manage expectations when a later-arriving small party is seated before an earlier large party. |
| **Revenue** | Directly boosts revenue through increased翻台率 (table turnover rate); provides data for optimizing table layout. | Initial implementation costs for SaaS systems and staff training. |

### Modeling Logic

**System Design: Parallel Queues**

The system operates on a minimum of three parallel, non-blocking queues, each tied to a specific table inventory:
- **S-Queue (1-2 persons)** -> Small Tables
- **M-Queue (3-4 persons)** -> Medium Tables
- **L-Queue (5+ persons)** -> Large Tables / Combinable Tables

**Key Algorithmic Policies:**

- **Downgrade Matching:** If S-Queue wait time exceeds a set threshold (e.g., 15 mins) and an M-Table is idle, the system suggests seating the S-Queue party at the M-Table.
- **Predictive Calling:** The system monitors seated tables' dining progress. When a table enters the "payment" state, the system pre-emptively calls the next party in the corresponding queue to minimize table idle time.
- **Dynamic Table Combination:** For the L-Queue, if no large table is free, the algorithm scans for adjacent, free S or M tables and suggests a physical combination to the staff.

**Table Utilization Cost Function (Conceptual):**
A simplified function to represent the system's optimization goal:
Minimize C = w₁ * T_idle + w₂ * N_mismatch

Where:
- `C` = Total operational cost/inefficiency
- `T_idle` = Sum of idle minutes for all tables
- `N_mismatch` = Number of parties seated at oversized tables
- `w₁`, `w₂` = Weighting factors for idle time vs. mismatch inefficiency

---

## 2: App Research - Meituan/KeeTa Dispatch System

### Overview & History

Meituan is a Chinese technology super-platform founded in 2010, dominating food delivery and local services. Its core competency is a sophisticated real-time logistics and dispatch system, often called the "Super Brain." KeeTa, launched in Hong Kong in 2023, is Meituan's global-facing brand, deploying this mature technology to new markets. The system targets a three-sided marketplace: **users** seeking convenience and speed, **merchants** aiming to expand their reach, and **riders** looking to maximize income through efficient order fulfillment.

### Core Features

- **Dynamic Load Balancing**: The system constantly analyzes real-time order volume ("queue size") against available rider capacity in any given geographical cell.
- **Intelligent Order Bundling**: During medium-load periods, the algorithm automatically groups orders with nearby restaurants and delivery destinations into a single trip for one rider, optimizing route and time.
- **Surge Pricing & Throttling**: In high-load scenarios (e.g., rainstorms), the system dynamically increases delivery fees (for users) and bonuses (for riders) to balance supply and demand. If the order queue becomes critically long, it may temporarily make some restaurants unavailable ("throttling") to prevent system collapse and guarantee service for existing orders.
- **ETA Prediction Engine**: Uses machine learning to provide highly accurate Estimated Time of Arrival by factoring in restaurant prep time, real-time traffic, weather, and rider location.

### Underlying Tech

| Technology | Purpose |
|------------|---------|
| **Cloud Infrastructure (e.g., Tencent/AWS)** | Massive, auto-scaling compute power for handling city-wide, concurrent dispatch calculations. |
| **Real-time GIS & Geofencing** | For precise location tracking of riders, customers, and merchants, and for defining operational zones. |
| **In-Memory Database (e.g., Redis)** | Millisecond-latency access to order statuses, rider locations, and queue data for rapid decision-making. |
| **Machine Learning Engine (e.g., TensorFlow)** | Powers the core dispatch algorithm, ETA predictions, and route optimization. |

### Operational Impact

| Metric | Traditional Dispatch | Meituan/KeeTa Algorithm |
|--------|----------------------|---------------------------|
| Avg. Delivery Time | 45-60 min | ~30 min |
| Rider Efficiency | 10-15 orders/day | 30-50+ orders/day |
| System Throughput | Limited by human dispatchers | Millions of orders per hour |
| Data Visibility | None / Manual | Real-time dashboards on order density, rider performance, etc. |

The system automates the entire lifecycle of an order from placement to delivery, making millions of micro-decisions per second to optimize the efficiency of the entire network.

---

## Citations & Links

- Meituan Official Site: https://about.meituan.com/en
- KeeTa App (iOS): https://apps.apple.com/hk/app/keeta/id1666524103
- Meituan Technical Blog on Dispatch Systems (Example, in Chinese): https://tech.meituan.com/2020/07/16/meituan-delivery-dispatch-algorithm.html
- General Article on Dynamic Pricing: https://www.forbes.com/sites/forbestechcouncil/2021/07/09/the-pros-and-cons-of-dynamic-pricing/
- Article on Restaurant Management Systems: https://www.lightspeedhq.com/blog/restaurant-management-system/

---

*Report for COMP1110 Restaurant Queue Simulation Project*
