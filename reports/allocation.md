# ITN Resource Allocation Brief: Northern Ghana (50,000 Nets)

**Prepared for:** National Malaria Elimination Programme (NMEP), Ghana Health Service  
**Advisory Group:** Group 3 Consultancy (Eric Elikplim Sunu, Lead)  
**Academic Context:** Ashesi University · ICS553 Machine Learning Essentials · Prosit 1  
**Deliverable:** 50-District Allocation Schedule, Sensitivity Analysis, and Policy Defense

---

## 1. Executive Summary

This advisory brief presents a scientifically defensible allocation schedule for **50,000 long-lasting insecticide-treated nets (ITNs)** across the 50 administrative districts of northern Ghana (Northern, Upper East, and Upper West regions).

Traditional allocation policies allocate commodities proportionally to routine clinic case counts. We demonstrate that this naive policy suffers from severe **referral hospital bias**, over-allocating nets to urban tertiary hubs where coverage already exceeds 79% while starving vulnerable rural catchment populations. 

By modeling district transmission using a **Negative Binomial regression with log-population offset** and scaling by the **unmet coverage gap** ($1 - \text{coverage}$), our proposed equitable policy:
1. Reallocates nets to high-population, low-coverage centers (**Tamale receives $+1,692$ additional nets**, **Sagnarigu $+1,012$**, **East Gonja $+878$**).
2. Dampens over-allocation to hospital referral centers (**Wa loses $-1,516$ nets**, **Bolgatanga loses $-665$ nets**), where baseline coverage is already high and recorded cases reflect external catchment patients.
3. Guarantees exact integer compliance ($\sum_{i=1}^{50} A_i = 50,000$) via **Hamilton's largest remainder apportionment**.

---

## 2. Methodology & Allocation Formula

### Mathematical Formulation
1. **Transmission Risk Estimation:**
   $$\log(\mu_i) = \beta_0 + \beta_1 \cdot \text{net\_coverage\_pct}_i + \log(\text{population}_i)$$
   where counts follow $\text{NB2}(\mu_i, \alpha)$, with estimated dispersion $\alpha = 0.2677$.
2. **Uncertainty-Aware Epidemic Risk:**
   We compute the upper bound of the 95% prediction interval $\hat{\mu}_{i,\text{upper}}$ to protect against epidemic surges.
3. **Unmet Need Weight:**
   $$W_i = \hat{\mu}_{i,\text{upper}} \times \left(1 - \frac{\text{net\_coverage\_pct}_i}{100}\right)$$
4. **Apportionment (Hamilton's Method):**
   $$q_i = 50,000 \times \frac{W_i}{\sum_{j=1}^{50} W_j}, \quad A_i = \lfloor q_i \rfloor + r_i$$
   where $r_i \in \{0, 1\}$ assigned to the largest fractional remainders until $\sum A_i = 50,000$.

---

## 3. Full 50-District Allocation Schedule

| Rank | District | Region | Population | Baseline Net Coverage | Positive Cases | Naive Allocation | Equitable Allocation | Net Shift ($\Delta$) |
|---|---|---|---|---|---|---|---|---|
| 1 | Bolgatanga | Upper East Region | 146,648 | 79.6% | 589,849 | 3,015 | **2,350** | -665 |
| 2 | Garu-Tempane | Upper East Region | 144,084 | 79.6% | 537,743 | 2,749 | **2,309** | -440 |
| 3 | Tamale | Northern Region | 255,650 | 67.7% | 94,577 | 483 | **2,175** | +1,692 |
| 4 | Kasena-Nankana | Upper East Region | 121,967 | 79.6% | 279,555 | 1,429 | **1,954** | +525 |
| 5 | Bawku | Upper East Region | 109,220 | 79.6% | 375,349 | 1,918 | **1,750** | -168 |
| 6 | Bawku West | Upper East Region | 104,486 | 79.6% | 330,111 | 1,687 | **1,674** | -13 |
| 7 | Bongo | Upper East Region | 94,019 | 79.6% | 332,006 | 1,697 | **1,507** | -190 |
| 8 | Talensi | Upper East Region | 90,474 | 79.6% | 257,164 | 1,314 | **1,450** | +136 |
| 9 | Sagnarigu | Northern Region | 168,145 | 67.7% | 82,041 | 419 | **1,431** | +1,012 |
| 10 | Nanumba North | Northern Region | 161,943 | 67.7% | 142,368 | 728 | **1,378** | +650 |
| 11 | Savelugu-Nanton | Northern Region | 159,170 | 67.7% | 145,932 | 746 | **1,355** | +609 |
| 12 | East Gonja | Northern Region | 155,946 | 67.7% | 87,768 | 449 | **1,327** | +878 |
| 13 | Kasena-Nankana West | Upper East Region | 78,847 | 79.6% | 331,779 | 1,696 | **1,263** | -433 |
| 14 | Bunkpurugu-Yunyoo | Northern Region | 139,484 | 67.7% | 173,167 | 885 | **1,187** | +302 |
| 15 | East Mamprusi | Northern Region | 139,026 | 67.7% | 146,684 | 750 | **1,183** | +433 |
| 16 | West Mamprusi | Northern Region | 139,060 | 67.7% | 76,698 | 392 | **1,183** | +791 |
| 17 | Yendi | Northern Region | 136,110 | 67.7% | 149,880 | 766 | **1,158** | +392 |
| 18 | Binduri | Upper East Region | 68,483 | 79.6% | 195,412 | 999 | **1,097** | +98 |
| 19 | Wa | Upper West Region | 119,409 | 69.8% | 510,536 | 2,610 | **1,094** | -1,516 |
| 20 | Gushiegu | Northern Region | 127,710 | 67.7% | 77,631 | 397 | **1,087** | +690 |
| 21 | Kpandai | Northern Region | 124,884 | 67.7% | 135,944 | 695 | **1,063** | +368 |
| 22 | Pusiga | Upper East Region | 63,913 | 79.6% | 324,040 | 1,656 | **1,024** | -632 |
| 23 | Builsa North | Upper East Region | 62,704 | 79.6% | 198,952 | 1,017 | **1,005** | -12 |
| 24 | Sawla-Tuna-Kalba | Northern Region | 113,808 | 67.7% | 225,306 | 1,152 | **968** | -184 |
| 25 | Nanumba South | Northern Region | 107,670 | 67.7% | 105,606 | 540 | **916** | +376 |
| 26 | Jirapa | Upper West Region | 98,366 | 69.8% | 295,356 | 1,510 | **902** | -608 |
| 27 | Central Gonja | Northern Region | 99,732 | 67.7% | 158,686 | 811 | **849** | +38 |
| 28 | Wa West | Upper West Region | 90,556 | 69.8% | 242,905 | 1,242 | **830** | -412 |
| 29 | Mion | Northern Region | 93,547 | 67.7% | 95,125 | 486 | **796** | +310 |
| 30 | Karaga | Northern Region | 88,292 | 67.7% | 66,957 | 342 | **751** | +409 |
| 31 | Wa East | Upper West Region | 80,358 | 69.8% | 200,006 | 1,022 | **737** | -285 |
| 32 | Tolon | Northern Region | 82,827 | 67.7% | 154,301 | 789 | **705** | -84 |
| 33 | Builsa South | Upper East Region | 40,623 | 79.6% | 158,164 | 808 | **651** | -157 |
| 34 | Saboba | Northern Region | 76,402 | 67.7% | 138,672 | 709 | **650** | -59 |
| 35 | Nadowli-Kaleo | Upper West Region | 68,717 | 69.8% | 231,888 | 1,185 | **630** | -555 |
| 36 | Zabzugu | Northern Region | 73,848 | 67.7% | 84,689 | 433 | **628** | +195 |
| 37 | Bole | Northern Region | 70,912 | 67.7% | 191,586 | 979 | **603** | -376 |
| 38 | Nabdam | Upper East Region | 37,256 | 79.6% | 265,768 | 1,358 | **597** | -761 |
| 39 | Tatale-Sangule | Northern Region | 69,286 | 67.7% | 109,774 | 561 | **590** | +29 |
| 40 | Sissala East | Upper West Region | 63,151 | 69.8% | 237,265 | 1,213 | **579** | -634 |
| 41 | Lawra | Upper West Region | 61,143 | 69.8% | 196,648 | 1,005 | **560** | -445 |
| 42 | Lambussie-Karni | Upper West Region | 57,703 | 69.8% | 241,844 | 1,236 | **529** | -707 |
| 43 | Chereponi | Northern Region | 62,151 | 67.7% | 93,652 | 479 | **529** | +50 |
| 44 | Sissala West | Upper West Region | 55,365 | 69.8% | 173,575 | 887 | **507** | -380 |
| 45 | Nandom | Upper West Region | 51,248 | 69.8% | 148,102 | 757 | **470** | -287 |
| 46 | Mamprugu-Moagduri | Northern Region | 53,901 | 67.7% | 41,612 | 213 | **459** | +246 |
| 47 | North Gonja | Northern Region | 50,814 | 67.7% | 46,343 | 237 | **432** | +195 |
| 48 | West Gonja | Northern Region | 47,944 | 67.7% | 96,371 | 493 | **408** | -85 |
| 49 | Kumbungu | Northern Region | 45,220 | 67.7% | 51,640 | 264 | **385** | +121 |
| 50 | Daffiama-Bussie-Issa | Upper West Region | 36,585 | 69.8% | 154,954 | 792 | **335** | -457 |
| **Total** | **All 50 Districts** | — | **5,263,334** | — | **9,781,209** | **50,000** | **50,000** | **0** |

---

## 4. Deep-Dive on Major Policy Reallocations

```
        ┌─────────────────────────────────────────────────────────────┐
        │       Top Gainers (Equitable Allocation > Naive)            │
        ├─────────────────────────────────────────────────────────────┤
        │ Tamale          │ +1,692 nets (High population, low cov gap)│
        │ Sagnarigu       │ +1,012 nets (Peri-urban expansion zone)   │
        │ East Gonja      │ +878 nets   (Rural underserved basin)     │
        │ West Mamprusi   │ +791 nets   (High transmission ecology)   │
        │ Gushiegu        │ +690 nets   (Clinic-deprived rural zone)  │
        ├─────────────────────────────────────────────────────────────┤
        │        Top Losers (Equitable Allocation < Naive)            │
        ├─────────────────────────────────────────────────────────────┤
        │ Wa              │ -1,516 nets (Referral hospital distortion)│
        │ Nabdam          │ -761 nets   (Low pop, high existing cov)  │
        │ Lambussie-Karni │ -707 nets   (Saturated net ownership)     │
        │ Bolgatanga      │ -665 nets   (Regional hospital hub, ~80%) │
        │ Sissala East    │ -634 nets   (Low unmet net deficit)       │
        └─────────────────────────────────────────────────────────────┘
```

### Why Do Tamale and Sagnarigu Gain Over 2,700 Nets Combined?
1. **Under-Credited by Naive Case Count:** Tamale has over 255,000 residents (by far the largest population in the dataset), yet reported only 94,577 positive cases over the 4-year surveillance period. Under naive allocation, it was awarded a meager 483 nets ($0.97\%$ of the shipment).
2. **Unmet Coverage Need:** Northern Region’s baseline net coverage is $67.7\%$, compared to $79.6\%$ in Upper East. The absolute number of unprotected citizens in Tamale is the largest in northern Ghana. Allocating 2,175 nets closes a critical urban/peri-urban protection deficit.

### Why Do Wa and Bolgatanga Lose Significant Nets?
1. **The Referral Hub Effect:** Wa (510,536 cases) and Bolgatanga (589,849 cases) recorded massive case totals not because local residents are infected at $5\times$ higher rates, but because they host the two primary regional tertiary hospitals in northern Ghana. Patients from small surrounding districts (e.g., Nabdam, Bongo, Wa East, Wa West) seek clinical care at these central facilities.
2. **Diminishing Marginal Utility:** Upper East already has $79.6\%$ net coverage, and Upper West has $69.8\%$. Both municipal centers are saturated with nets from prior NGO campaigns. Awarding Bolgatanga 3,015 nets under naive rules would result in nets sitting unused in storerooms, while nearby rural districts lack basic bed coverage.

---

## 5. Sensitivity & Robustness Analysis

1. **Shipment Size Sensitivity ($N = 25,000$ to $100,000$):**
   Because Hamilton's apportionment scales linearly with the unmet need index $W_i$, relative shares remain strictly invariant. District priority order does not flip under budget expansions or cuts.
2. **Coverage Measurement Uncertainty:**
   If Northern Region's true net coverage is lower than the DHS point estimate ($67.7\%$), as suggested by our cluster bootstrap interval (which extends down to $60.1\%$), the true unmet need gap is even wider. Under extreme rural under-coverage scenarios, the allocation shift toward Northern Region is even more justified.

---

## 6. Implementation Roadmap for NMEP

1. **Logistics & Warehousing:** Route bulk shipments to three central regional depots:
   - Tamale Central Depot: 24,980 nets (Northern Region)
   - Bolgatanga Depot: 17,547 nets (Upper East Region)
   - Wa Central Depot: 7,473 nets (Upper West Region)
2. **Last-Mile Distribution:** District health directorates must distribute directly through Community-Based Health Planning and Services (CHPS) compounds, prioritizing pregnant women attending antenatal care (ANC) and children receiving measles immunizations.
3. **Post-Distribution Audit:** Rapid cluster surveys must be conducted at 6 months post-distribution to assess net retention, hanging rates, and physical integrity.
