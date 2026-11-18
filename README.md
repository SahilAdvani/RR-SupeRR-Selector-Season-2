# SupeRR Selector Season 2: Identifying Cricket's True Clutch Performers
## Rajasthan Royals Analytics Case Study & Submission Repository

**Author / Participant:** Sahil Advani (`sahiladvani`)  
**Target Organization:** Rajasthan Royals (RR) Analytics Department  
**Evaluation Panel:** Giles Lindsay (Director of Strategy and Analytics) & Kumar Sangakkara (Head Coach)  
**Round:** Round 1 — Identifying the Most Reliable Players Under Pressure  

---

## 📌 Executive Summary
In high-stakes T20 cricket, aggregate statistical metrics (overall strike rate, seasonal average, or raw economy) blur critical context by treating a boundary when win probability is 95% the same as a boundary when the match is on the line. 

This repository houses the end-to-end, reproducible quantitative code, models, datasets, visual quadrants, and reports for the **Royals 5-Pillar Consensus Clutch Engine** evaluated across 883 matches (200,999 deliveries) from 2022 to 2026.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE ROYALS 5-PILLAR CONSENSUS ARCHITECTURE                      │
├────────────────────────────────┬───────────────────────────────────────────────────────┤
│ Pillar 1: Dynamic Pressure     │ Continuous Pressure Situation Index (PSI, 0–100)      │
│ Situation Index (PSI)          │ tracking RRR stress, resource strain & phase urgency. │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ Pillar 2: Head-to-Head (H2H)   │ Individual Empirical Bayes ratings (0.70x to 1.35x)   │
│ Opponent Caliber Weights       │ scaling credits for facing Bumrah vs a part-timer.    │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ Pillar 3: Expected Value       │ Runs Above Expectation (RAE) for batters and Runs     │
│ (RAE & RSAE per 100 balls)     │ Saved Above Expectation (RSAE) for bowlers.           │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ Pillar 4: Win Probability      │ Delivery-level equity shifts with penalization for    │
│ Added (WPA) & Consistency      │ match-to-match volatility (sigma).                    │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ Pillar 5: Bayesian Sample      │ Shrinkage factor r = N / (N + 50) regressing small     │
│ Reliability Shrinkage          │ samples (80 balls) vs sustained mastery (400+ balls). │
└────────────────────────────────┴───────────────────────────────────────────────────────┘
```

---

## 🏆 Official Consensus Top 10 Leaderboards

### 🏏 Top 10 Batters Under Pressure (Consensus CBI)
| Rank | Player Name | Tactical Role | Press Balls | Base SR | Press SR | Δ SR | RAE / 100 Balls | Reliability ($r$) | Final CBI | Primary Tactical Profile |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Donovan Ferreira** | Batter | 127 | 163.85 | **193.70** | +29.85 | **+51.78** | 0.718 | **65.66** | Explosive Middle-Order/Death Finisher & Spin Slogger |
| **2** | **Naman Dhir** | All-Rounder | 172 | 168.42 | **192.44** | +24.02 | **+34.09** | 0.775 | **65.65** | Dynamic High-Tempo Enforcer against High-Pace Bowling |
| **3** | **Rajat Patidar** | Batter | 130 | 167.86 | **192.31** | +24.44 | **+48.04** | 0.722 | **64.63** | Elite No. 3/4 Spin Punisher in High-Stakes Chases |
| **4** | **Ashutosh Sharma** | Batter | 248 | 166.28 | **184.27** | +17.99 | **+32.80** | **0.832** | **64.42** | Fearless Death-Over Executioner with 360° Range |
| **5** | **Dinesh Karthik** | Batter | 281 | 167.29 | **184.70** | +17.40 | **+33.60** | **0.849** | **63.76** | Veteran Death Over Specialist under Steep Required Rates |
| **6** | **Tim David** | Batter | 377 | 177.65 | **189.66** | +12.00 | **+28.17** | **0.883** | **63.63** | Elite High-Baseline Power Hitter & Boundary Machine |
| **7** | **Shashank Singh** | Batter | 306 | 161.61 | **178.10** | +16.50 | **+27.85** | **0.860** | **62.87** | Calm, High-Impact Middle-Order Chase Finisher |
| **8** | **Sanju Samson** | Batter | 135 | 154.61 | **179.26** | +24.64 | **+40.42** | 0.730 | **62.17** | Powerplay & Middle-Overs Aggressor in Pressure Chases |
| **9** | **Rinku Singh** | Batter | 372 | 152.68 | **175.27** | +22.58 | **+26.45** | **0.882** | **61.82** | Elite Last-Over Boundary Striker & Game Closer |
| **10** | **Marcus Stoinis** | All-Rounder | 341 | 153.57 | **173.61** | +20.04 | **+32.87** | **0.872** | **61.14** | High-Impact Pace-Muscling Finisher with Heavy Sample |

---

### 🎯 Top 10 Bowlers Under Pressure (Consensus CBoI)
| Rank | Player Name | Tactical Role | Press Balls | Base Econ | Press Econ | RSAE / 100 Balls | Press Wkt% | Reliability ($r$) | Final CBoI | Primary Tactical Profile |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Matheesha Pathirana** | Bowler | 419 | 8.83 | **7.73** | **+43.56** | **10.74%** | **0.893** | **66.91** | Unplayable Sling-Action Death Yorker Specialist |
| **2** | **Mayank Yadav** | Bowler | 83 | 9.38 | **6.29** | **+51.67** | **12.05%** | 0.624 | **66.07** | 150+ kph Express Pace Enforcer (Extreme Dot Creation) |
| **3** | **Sunil Narine** | All-Rounder | 288 | 6.86 | **5.85** | **+31.97** | 8.68% | **0.852** | **65.79** | Undisputed Mystery Spin Master (Supreme Run Choke) |
| **4** | **Jasprit Bumrah** | Bowler | 418 | 7.26 | **6.79** | **+26.63** | **10.53%** | **0.893** | **62.04** | The Gold Standard Multi-Phase Executioner in World Cricket |
| **5** | **Anshul Kamboj** | Bowler | 137 | 9.97 | 8.50 | **+16.19** | **13.87%** | 0.733 | **61.81** | Hard-Length Seamer Striking Reliably at the Death |
| **6** | **Eshan Malinga** | Bowler | 239 | 9.06 | **7.86** | **+15.61** | **11.30%** | **0.827** | **61.76** | Slinging Yorker Specialist Striking Every 8.8 Deliveries |
| **7** | **Sakib Hussain** | Bowler | 112 | 9.42 | **7.77** | **+18.52** | 8.04% | 0.691 | **60.48** | Emerging Indian Pacer Holding High Economy Discipline |
| **8** | **Mohit Sharma** | Bowler | 285 | 9.61 | 8.57 | **+6.69** | **11.58%** | **0.851** | **60.42** | Veteran Back-of-the-Hand Slower Ball & Wide Yorker Enforcer |
| **9** | **Gerald Coetzee** | Bowler | 120 | 9.62 | 8.35 | **+12.41** | **10.00%** | 0.706 | **59.66** | Express Pace Middle/Death Enforcer with Heavy Bouncer |
| **10** | **Yuzvendra Chahal** | Bowler | 484 | 8.62 | **7.98** | **+12.57** | **10.33%** | **0.906** | **59.27** | Wicket-Taking Leg-Spinner with Maximum Pressure Exposure |

---

## 📂 Repository Structure
```bash
├── src/
│   ├── data_loader.py                  # Ingestion, competition tiering (IPL 1.25x, World Cup 1.20x)
│   ├── match_state.py                  # Chronological match reconstruction (runs, wickets, RRR)
│   ├── pressure_model.py               # Continuous Pressure Situation Index (PSI, 0-100)
│   ├── advanced_clutch_engine.py       # H2H weights, RAE/RSAE, WPA, and Bayesian reliability
│   ├── generate_visualizations.py      # Publication quadrant & PSI curve generation
│   ├── generate_slide_visualizations.py# 16:9 widescreen chart renderings
│   ├── compile_pdf_report.py           # ReportLab 4-page formal submission PDF
│   └── build_presentation_deck.py      # python-pptx presentation deck generator
├── outputs/
│   ├── official_top_10_batters.csv     # Ranked top 10 batters under pressure
│   ├── official_top_10_bowlers.csv     # Ranked top 10 bowlers under pressure
│   ├── all_qualified_batters.csv       # Complete qualified batter metrics
│   ├── all_qualified_bowlers.csv       # Complete qualified bowler metrics
│   ├── figures/                        # High-resolution scatterplots and PSI curves
│   ├── Rajasthan_Royals_SupeRR_Selector_Season_2_Methodology_Report.pdf # Formal PDF Report
│   └── Rajasthan_Royals_SupeRR_Selector_Season_2_Presentation.pptx      # 16-Slide Deck
├── README.md                           # Master documentation
└── requirements.txt                    # Python environment specifications
```

---

## ⚡ Reproducibility (Run in 12 Seconds)
To execute the complete analytics pipeline from raw CSV data:
```bash
# Clone the repository
git clone https://github.com/sahiladvani/RR-SupeRR-Selector-Season-2.git
cd RR-SupeRR-Selector-Season-2

# Install dependencies
pip install -r requirements.txt

# Run advanced clutch consensus engine
python src/advanced_clutch_engine.py

# Generate visualizations & official PDF report
python src/generate_visualizations.py
python src/compile_pdf_report.py
```

---

## 📜 Official Round 1 Submission Details
- **Participant:** Sahil Advani
- **Franchise Focus:** Rajasthan Royals (RR)
- **Problem Statement:** Identify Top 10 Batters and Top 10 Bowlers performing best under pressure.
- **Halla Bol!**
