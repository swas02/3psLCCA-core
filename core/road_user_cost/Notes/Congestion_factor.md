# **Introduction:**
This document presents a step-by-step approach to adjust the Vehicle Operating Cost (VOC) for a small car over a 4-hour period based on hourly time- and distance-related congestion factors.

Note: Assume 1 day = 4 hours.

**Given Data:**

* Distance-related VOC per car: **A (₹/car)**
* Time-related VOC per car: **B (₹/car)**
* Hourly traffic volume (number of cars, Nₕ):

  * Hour 1: 200 cars
  * Hour 2: 400 cars
  * Hour 3: 300 cars
  * Hour 4: 200 cars
* Congestion factors (distance and time) per hour: to be assigned or calculated based on V/C ratio.

---

## **VOC Calculation Table:**

This table is only for one type of car say for small cars.

- ADT is 1100 PCU/Day

| Hour | Traffic (No. of Cars, Nₕ) | Distance CF (DCF) | Time CF (TCF) | VOC per car = A×DCF + B×TCF | Total VOC for hour = VOC per car × Nₕ |
| ---- | ------------------------- | ----------------- | ------------- | --------------------------- | ------------------------------------- |
| 1    | 200                       | a                 | α             | A·a + B·α                   | 200·(A·a + B·α)                       |
| 2    | 400                       | b                 | β             | A·b + B·β                   | 400·(A·b + B·β)                       |
| 3    | 300                       | c                 | γ             | A·c + B·γ                   | 300·(A·c + B·γ)                       |
| 4    | 200                       | d                 | δ             | A·d + B·δ                   | 200·(A·d + B·δ)                       |

**Total VOC for 4-hour period:**

[
VOC_{total} = 200(A·a + B·α) + 400(A·b + B·β) + 300(A·c + B·γ) + 200(A·d + B·δ)
]

---

**Explanation:**

1. **Distance-related VOC (A)** represents fuel, oil, tyre wear, and maintenance costs per car per unit distance.
2. **Time-related VOC (B)** represents driver wages, depreciation, and overheads per car per unit time.
3. **Distance Congestion Factor (a, b, c, d)** adjusts the distance VOC based on congestion; higher values indicate more congestion and higher fuel/tyre/wear costs. Refer table 10 of IRC SP 30-2019.
4. **Time Congestion Factor (α, β, γ, δ)** adjusts the time VOC; higher values indicate slower travel and increased time costs. Refer table 11 of IRC SP 30-2019.
5. Multiplying by **Nₕ** accounts for the number of vehicles using the road each hour.

---

**Conclusion:**
This table and formula provide a complete framework to calculate hourly and total VOC for a small car over multiple hours of operation. Once actual congestion factors are computed (using IRC SP:30 formulas), numerical VOC values can be derived for each hour and summed to get total cost.
