# ITN Resource Allocation Brief: Northern Ghana (50,000 Nets)

**Prepared for:** National Malaria Elimination Programme (NMEP), Ghana Health Service  
**Advisory Group:** Group 3 Consultancy (Eric Elikplim Sunu, Lead)  
**Academic Context:** Ashesi University · ICS553 Machine Learning Essentials · Prosit 1  
**Deliverable:** 50-District Allocation Schedule, Sensitivity Analysis, and Policy Defense

---

## 1. Executive Summary

This brief presents an allocation schedule for **50,000 long-lasting insecticide-treated nets (ITNs)** across the 50 districts of northern Ghana (Northern, Upper East and Upper West as they were in 2014-17).

We compare two rules. A **case-proportional comparator** gives nets in proportion to reported positive cases. It is not Ghana's practice, which allocates ITNs by population through mass campaigns at about one net per two people (PMI Ghana Malaria Operational Plan FY2017). Our **equitable rule** weights each district by the upper 95% confidence bound of its expected cases (negative binomial with a log-population offset) times its unmet coverage gap ($1 - \text{coverage}$). Against the comparator:
1. Nets move towards the most populous districts: **Tamale $+1,692$**, **Sagnarigu $+1,012$**, **East Gonja $+878$**.
2. Districts that report many cases per person give nets up: **Wa $-1,516$**, **Nabdam $-761$**, **Bolgatanga $-665$**.
3. Exactly 50,000 whole nets are allocated ($\sum_{i=1}^{50} A_i = 50,000$) by **Hamilton's largest-remainder method**.

Because coverage is known only by region, the rule allocates in proportion to population within each region (section 2). The split between regions depends on the model: a better-fitting region-effects model moves 7,720 nets (section 5). Sources: `04_allocation.ipynb`, cells alloc_cd07 to alloc_cd13.

---

## 2. Methodology & Allocation Formula

### Mathematical Formulation
1. **Transmission Risk Estimation:**
   $$\log(\mu_i) = \beta_0 + \beta_1 \cdot \text{net\_coverage\_pct}_i + \log(\text{population}_i)$$
   where counts follow $\text{NB2}(\mu_i, \alpha)$, with estimated dispersion $\alpha = 0.2677$.
2. **Upper confidence bound:**
   $\hat{\mu}_{i,\text{upper}}$ is the upper bound of the 95% confidence interval for $\mu_i$. It is a confidence interval for the mean, not a prediction interval for a district's count.
3. **Unmet Need Weight:**
   $$W_i = \hat{\mu}_{i,\text{upper}} \times \left(1 - \frac{\text{net\_coverage\_pct}_i}{100}\right)$$
4. **Apportionment (Hamilton's Method):**
   $$q_i = 50,000 \times \frac{W_i}{\sum_{j=1}^{50} W_j}, \quad A_i = \lfloor q_i \rfloor + r_i$$
   where $r_i \in \{0, 1\}$ assigned to the largest fractional remainders until $\sum A_i = 50,000$.

### What the rule does in practice (`04_allocation.ipynb`, alloc_cd11)
- `net_coverage_pct` takes one value per region, so $\mu_i$ is population times a regional rate. Within a region, nets follow population exactly: 8.5 nets per 1,000 people in Northern, 16.0 in Upper East and 9.2 in Upper West.
- The upper bound multiplies each region by a constant (1.198, 1.342 and 1.162), so it shifts nets between regions, not between districts within a region.
- The coverage coefficient is positive ($\beta_1 = +0.082$ per percentage point): regions with more nets had more malaria, because nets were sent where malaria was worst and the coverage (2022) post-dates the cases (2014-17). In the weight, this term outweighs the gap term, so higher-coverage regions receive more nets per person.

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
| **Total** | **All 50 Districts** | | **4,788,809** | | **9,781,981** | **50,000** | **50,000** | **0** |

---

## 4. Who Gains, Who Loses, and Why

| District | Region | Change vs comparator | Cases per person, 2014-17 | Rank in region (1 = most) |
|---|---|---|---|---|
| Tamale | Northern | +1,692 | 0.37 | 26 of 26 |
| Sagnarigu | Northern | +1,012 | 0.49 | 25 of 26 |
| Bole | Northern | -376 | 2.70 | 1 of 26 |
| Nabdam | Upper East | -761 | 7.13 | 1 of 13 |
| Bolgatanga | Upper East | -665 | 4.02 | 4 of 13 |
| Wa | Upper West | -1,516 | 4.28 | 1 of 11 |

Source: `04_allocation.ipynb`, cells alloc_cd09 and alloc_cd11.

### Why do Tamale and Sagnarigu gain?
They are the two most populous districts in the dataset, and within a region the rule allocates by population. They also report the fewest cases per person of all 50 districts (Tamale the fewest, Sagnarigu the second fewest), so the case-proportional comparator gives them little: Tamale would receive 483 nets. Our rule treats their residents as being at the same risk as the rest of Northern Region. That is a value judgement, and we make it openly: it protects districts whose low counts may reflect low testing, at the cost of districts whose high counts reflect real burden.

### Why do Wa and Bolgatanga lose?
The rule moves nets towards Northern Region overall, and both districts report many cases per person for their regions (Wa 1st of 11, Bolgatanga 4th of 13), which a population rule does not reward. Referral bias, where a regional hospital records patients from neighbouring districts, may add to their counts, but it is a hypothesis, not a finding. Against it: Nabdam, often named as a sending district, reports the most cases per person of all 50 districts, and Tamale, home to the north's only tertiary hospital (claims table, E-03), reports the fewest.

---

## 5. Sensitivity: What Would Change the Answer

One modelling choice changes at a time (`04_allocation.ipynb`, cell alloc_cd13):

| Scenario | Northern | Upper East | Upper West | Nets moved |
|---|---|---|---|---|
| As proposed | 24,196 | 18,631 | 7,173 | 0 |
| Point estimate instead of the upper bound | 25,095 | 17,240 | 7,665 | 1,391 |
| Region-effects model (AIC 1,253.8 vs 1,286.8) | 18,634 | 16,473 | 14,893 | 7,720 |
| Coverage corrected for the 11 districts now in Savannah or North East | 27,686 | 14,891 | 7,423 | 3,740 |
| Northern coverage at its lower cluster-bootstrap bound (61.4%) | 22,939 | 18,596 | 8,465 | 1,292 |
| Northern coverage at its upper cluster-bootstrap bound (74.0%) | 29,004 | 11,951 | 9,045 | 6,680 |

- Within a region, nets follow population in every scenario except the coverage correction, which gives the 11 reassigned districts their current regions' coverage (Savannah 79.1%, North East 62.8%).
- The regional split is the uncertain part. The region-effects model fits the data better and moves 7,720 nets, so regional totals should be read as a range, not a point.
- Lower Northern coverage does not earn Northern Region more nets under this model: because the coverage coefficient is positive, it gives fewer (22,939 at 61.4%).
- A larger or smaller budget does not change shares: Hamilton apportionment scales every district's share, up to rounding.

---

## 6. Implementation Roadmap for NMEP

1. **Logistics & Warehousing:** Route bulk shipments to three central regional depots:
   - Tamale Central Depot: 24,196 nets (Northern Region)
   - Bolgatanga Depot: 18,631 nets (Upper East Region)
   - Wa Central Depot: 7,173 nets (Upper West Region)

   (Regional totals from `04_allocation.ipynb`, cell alloc_cd07.)
2. **Last-Mile Distribution:** District health directorates must distribute directly through Community-Based Health Planning and Services (CHPS) compounds, prioritizing pregnant women attending antenatal care (ANC) and children receiving measles immunizations.
3. **Post-Distribution Audit:** Rapid cluster surveys must be conducted at 6 months post-distribution to assess net retention, hanging rates, and physical integrity.
