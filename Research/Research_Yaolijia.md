# Restaurant Queue Simulation - Concise Research Report

## 1: Strategic Research - VIP Queue Strategy 

### Concept & Evolution

The VIP priority queuing concept originated from the British term "VIP" (Very Important Person), first emerging around 1933 and gaining administrative significance during WWII for identifying senior military personnel and diplomats requiring priority transportation. Post-war civilian aviation adopted this concept, offering lounges and priority services to distinguished guests. In the F&B sector, the 1968 establishment of "VIP's" restaurant chain in Oregon, USA—serving Denny's-style coffee shops near freeways—marked the early integration of VIP branding into casual dining. The strategy evolved from informal host-discretion models to modern algorithmic, data-driven frameworks where time became a proxy for value alongside food quality and service.

### Scope: Best F&B Use Cases

VIP queuing is most effective in:

- **Fine-dining establishments**: Targeting "gourmet foodies" and influencers who contribute 20-50% of revenue and drive word-of-mouth promotion
- **High-demand urban venues**: Where demand significantly exceeds capacity, causing "balking" (customers refusing to join) or "reneging" (leaving queue)
- **High-turnover casual dining**: Japanese all-you-can-eat or hotpot restaurants managing dense crowds while ensuring regulars receive consistent experiences
- **Medium-sized restaurants**: Reducing on-site congestion and lowering customer churn by up to 30%

### Pros & Cons

| Dimension | Advantages | Disadvantages |
|-----------|------------|---------------|
| **Wait Time** | Stabilizes wait times for high-value VIP segments; reduces balking/reneging among profitable customers | May increase wait times for regular customers; risk of "starvation" when VIP arrival rate exceeds threshold |
| **Table Utilization** | Prioritizes seating for customers with higher lifetime value; optimizes revenue per table | Potential idle tables if VIP parties do not match available table sizes |
| **Fairness** | Virtual queues hide queue-jumping, reducing "unfairness perception" | Visible VIP jumps create negative utility proportional to wait time differential |
| **Revenue** | Generates direct revenue via paid priority fees; enhances loyalty program value; increases customer retention | Potential reputational damage if perceived as unfair; may alienate price-sensitive customers |

### Modeling Logic

**Priority System Types:**

- **Non-preemptive priority**: VIP can pass regular customers but cannot interrupt a meal in progress; must wait until current service cycle completes
- **Preemptive priority**: Higher-priority tasks interrupt lower-priority ones (applicable to kitchen operations, not physical seating)

**Ratio-Based Calling Logic:**

Many restaurants employ a **3:1 ratio** (three regular parties seated for every one VIP party) to maintain system stability. This heuristic is supported by weighted resource allocation models:
- If VIP queue weight = 10 and Regular queue weight = 1, VIP receives disproportionate but not absolute share of capacity

**Total Cost Function for VIP Threshold:**
```
C = c₁λ₁E(W₁) + c₂λ₂E(W₂)
```
Where:
- c₁, c₂ = waiting costs for VIP and regular customers
- λ₁, λ₂ = arrival rates
- E(W₁), E(W₂) = expected wait times

**Key Simulation Parameters:**
- VIP-to-Regular arrival ratio: approximately 1:9
- Customer patience decreases with queue position
- Informational transparency (real-time updates) increases patience threshold

---

## 2: App Research - THE GULU 

### Overview & History

THE GULU is a comprehensive mobile queuing ecosystem developed by Gorilla Group Limited, launched in Hong Kong in 2014 after R&D began in 2011. The platform targets "busy Hong Kong citizens" optimizing their time and "F&B merchants" digitizing floor management. It serves over 2,000 restaurant partners including Japanese all-you-can-eat establishments, hotpot chains, Chinese tea houses, and Western dining outlets. Major clients include Maxim's Group (400+ restaurants). A defining milestone was its COVID-19 pandemic pivot: peak 1.28 million simultaneous logins for mask queueing in early 2020, and supporting 40+ community testing centers in 2022.

### Core Features

- **Remote Digital Queuing**: Get tickets via mobile app before arriving; real-time position updates; push notifications when seat is ready
- **Multi-Category Table Queuing**:
  - Category A: 1-2 persons
  - Category B: 3-4 persons
  - Category C: 5-6 persons
  - Category D: 7+ persons
  - Queues processed in parallel; small tables can serve Category A tickets even if Category B has older tickets
- **Fast-Lane VIP Services**: Integration with merchant loyalty databases; priority user management; virtual fast-track inserting VIPs at specific offset from front

### Underlying Tech

| Technology | Purpose |
|------------|---------|
| **Tencent Cloud (TKE)** | Container orchestration; horizontal pod autoscaling for traffic spikes |
| **TencentDB for Redis** | In-memory database; 1M+ transactions/hour; millisecond latency |
| **WebSocket** | Persistent bidirectional TCP for real-time push updates |
| **Golang (goroutines)** | Lightweight concurrent connections for thousands of simultaneous sessions |

### Operational Impact

| Metric | Traditional Queue | THE GULU Digital |
|--------|-------------------|------------------|
| On-site congestion | High stress at door | 50% reduction |
| Order remake rate | ~12% (communication errors) | <3% (digital integration) |
| Table turnover | Prone to idle tables | 15% increase |
| Data visibility | Anecdotal/intuition | Real-time analytics |

Staff must manage "hybrid" queues (walk-ins via kiosk + remote app users) using handheld POS devices synced with centralized queue manager.

---

## Citations & Links

- VIP Hospitality History: https://www.xootle.com/en/blog/vips-hospitality.html
- Queueing Theory Guide: https://www.qminder.com/blog/queue-management/queuing-theory-guide/
- THE GULU Official Site: https://web.thegulu.com/
- THE GULU Business Solutions: https://biz.thegulu.com/en/post/helping-small-and-medium-sized-restaurants-go-digital-the-gulu-provides-smart-queueing-solutions-fo
- THE GULU App (iOS): https://apps.apple.com/hk/app/the-gulu/id739628906
- THE GULU Shop (Merchant App): https://apps.apple.com/hk/app/the-gulu-shop/id1547938860
- VIP Queue Academic Thesis: https://scholar.dsu.edu/cgi/viewcontent.cgi?article=1314&context=theses
- Haidilao Membership: https://www.haidilao-inc.com/us/member
- TableCheck VIP Blog: https://www.tablecheck.com/blog/vips-and-foodies/
- Priority Queue Theory (Medium): https://medium.com/@rutujagurav72/the-vip-lane-in-rabbitmq-a-deep-dive-into-priority-queues-0f2cda701f03
- Fairness Research: https://faculty.washington.edu/yongpin/fairness%20paper.pdf
- Queueing Theory Wikipedia: https://en.wikipedia.org/wiki/Queueing_theory

---

*Report generated for COMP1110 Restaurant Queue Simulation Project*
