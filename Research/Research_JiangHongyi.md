# Restaurant Queue Simulation - Concise Research Report

## 1: Strategic Research - Table Sharing Queue Strategy

Table sharing is defined as the practice of seating multiple separate parties—individual customers or groups—who are previously unacquainted at the same restaurant table. Historically, this custom has roots in diverse cultural rituals: from Greek symposia and medieval feasts to the communal tables of European bakeries. In East Asia, especially in Japan and Hong Kong, table sharing evolved as a routine necessity of high-density urban life. In modern hospitality, the concept has transitioned from a rustic necessity into a high-performance operational strategy used to mitigate high urban rents and meet the demands of younger consumers who seek social connectivity and shared experiences. Today, communal tables are viewed as "public space infrastructure" that facilitates social interaction while maximizing seat utilization.

### Scope: Best F&B Use Cases

Table Sharing is most effective in:

-   **Cafes and Bakeries**: These places favor this strategy as it can create an inviting atmosphere and encourages customers to have social interactions.
-   **Fast-Casual Chains**: Establishments like Wagamama and Le Pain Quotidien utilize long communal benches to prioritize high-volume flow and speed.
-   **Dim Sum Halls and Urban Food Halls**: These high-density environments rely on table sharing to handle massive peak-hour crowds.
-   **Waiting Areas**: Pub tables in waiting areas usually adopt the strategy to manage guests before they move to private dining.

### Pros & Cons

| Dimension | Advantages | Disadvantages |
|----|----|----|
| **Wait Time** | Seating guests at shared tables is significantly faster than waiting for a private table to clear. | If not communicated clearly by staff, being asked to share can cause frustration and anxiety from guests. |
| **Table Utilization** | Unseated seats that are created when small groups occupy large tables can be utilized. | Inefficient seating layouts can still occur if hosts seat groups poorly, leaving single empty seats that are hard to fill. |
| **Fairness** | Provides a "social spark" and a sense of belonging to a larger community. | Cultural resistance is high in Western markets (e.g., the US) where personal space and independence are prioritized. |
| **Revenue** | Boosts Revenue by allowing more customers per shift without increasing the restaurant's footprint. | The noise and the crowding shared environment may result in the loss of customers. |

### Modeling Logic

To simulate or implement a table sharing strategy effectively, the following modeling logic is applied:

-   **Data Structure Definition**: The system must define entities for Customer Groups (size, arrival time, dining duration) and Tables (capacity and current occupancy status).
-   **Queue Segmentation**: Arriving groups are assigned to matching queues based on party size ranges, such as 1–2, 3–4, or 5+ people.
-   **Allocation**: Whenever a seat or table becomes available, the simulation identifies and seats the earliest-waiting group from the matching queue.
-   **Advance**: The model uses event-based or step-by-step logic to process arrivals, update dining status as groups finish, and immediately reset seats for the next waiting party.
-   **Performance Tracking**: Success is evaluated by computing metrics such as average/max wait time, max queue length, table utilization percentage (time occupied), and service level (percentage of groups seated within a target time).

## 2: App Research - Meiwei Bu Yong Deng

### Overview & History

"Meiwei Bu Yong Deng" (MWBYD) is a prominent smart dining service provider in China, specializing in B2B SaaS products and C-end consumer applications.

-   **Foundation**: Founded in January 2013 by Xie Xinfa, a former ZTE engineer, the company was born from the insight that queuing is the most effective scenario to connect restaurants (B-end) with consumers (C-end).
-   **Growth**: Within five years, it covered over 200 cities and partnered with more than 100,000 restaurants, serving nearly 80 million diners monthly.

### Core Features

The platform focuses on improving restaurant efficiency and the diner's experience through several key functions:

-   **Multi-channel Queuing**: Supports remote ticket collection via the App, WeChat official accounts, and third-party platforms, allowing guests to join a line from home or the office.
-   **Real-time Status Tracking**: Diners can scan a QR code on their ticket to see their exact position in the queue and estimated wait times.
-   **Pre-ordering Food**: Allows customers to select dishes while waiting, which is then synchronized with the kitchen to increase table turnover and reduce walk-out rates.
-   **Queue Incentives**: Restaurants can add "waiting discounts" or coupons to the queuing interface to retain customers.

### Underlying Technologies

| Technology | Purpose |
|----|----|
| **SaaS (Software as a Service)** | Cloud-based architecture allows for rapid deployment and iterative updates across thousands of locations without high hardware costs. |
| **Big Data Analytics** | Used for precise customer profiling (dining habits, preferences) and scientific site selection for new restaurant branches. |
| **Internet of Things (IoT)** | Integrates smart terminals (POS, printers, audio systems) to ensure seamless data flow between the front desk and the kitchen. |
| **Cloud Computing** | Facilitates real-time synchronization of queuing data across different mobile and web interfaces. |

### Operation Impact

| Metric | Traditional Manual Queue | Using MWBYD System |
|----|----|----|
| **Wait Time Experience** | Customers must stay near the door, which may be perceived as stressful. | Remote Queuing greatly reduces anxiety while waiting. |
| **Labor Efficiency** | Staff must manually record names and call numbers. | All procedures are automated, reducing staff burnout. |
| **Customer Retention** | High walk-out rate if the queue is not transparent. | Transparent queue status and pre-order function increases customer loyalty. |

------------------------------------------------------------------------

## Citations & Links

-   At Your Service on the Table: Impact of Tabletop Technology on Restaurant Performance: <https://faculty.wharton.upenn.edu/wp-content/uploads/2017/09/2017.9.10_Tabletop_For_Submission_WithNames.pdf>
-   Table sharing - Wikipedia: <https://en.wikipedia.org/wiki/Table_sharing>
-   Beyond Private Dining: Exploring the Communal Table as Public Space Infrastructure: <https://www.archdaily.com/1034907/beyond-private-dining-exploring-the-communal-table-as-public-space-infrastructure>
-   Community Table: Designing Restaurant Seating That Encourages Connection and Belonging: <https://americanspcc.org/community-table-designing-restaurant-seating-that-encourages-connection-and-belonging/>
-   Mastering the Table Turnover Rate: Boost Your Restaurant’s Efficiency: <https://www.getknowapp.com/blog/table-turnover-rate/>
-   Bistro Table vs Pub Table: The Ultimate Guide for Your Business: <https://www.homebaa.com/blogs/commerical/bistro-table-vs-pub-table>
-   Restaurant Queue Management System: How to Reduce Wait Times: <https://www.wavetec.com/blog/queue-management/restaurant-queue-management/>
-   MWBYD Official Website: <https://mwee.cn/>
-   MWBYD Apple Store Page: <https://apps.apple.com/cn/app/%E7%BE%8E%E5%91%B3%E4%B8%8D%E7%94%A8%E7%AD%89-%E8%AE%A9%E7%BE%8E%E5%91%B3%E4%B8%8D%E7%94%A8%E7%AD%89/id979857479>
-   MWBYD Baidu Baike Page: <https://baike.baidu.com/item/%E7%BE%8E%E5%91%B3%E4%B8%8D%E7%94%A8%E7%AD%89/14580321>

------------------------------------------------------------------------
