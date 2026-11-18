# Implementation Plan: SupeRR Selector Season 2 (Round 1)

## Overview & Phased Workflow

| Phase | Milestone | Expected Deliverable | Status |
|---|---|---|---|
| **Phase 1** | Groundwork & Data Exploration | EDA summary, clean schema mappings | In Progress |
| **Phase 2** | Match-State Engine & Pressure Modeling | Cumulative match state, Win Expectancy / PSI formula | Pending Review |
| **Phase 3** | Player Performance Engine | Batter & Bowler baseline vs pressure metrics, Delta scores | Pending Review |
| **Phase 4** | Ranking & Robustness Testing | Top 10 Batters, Top 10 Bowlers, Empirical Bayes shrinkage, sensitivity tests | Pending Review |
| **Phase 5** | Visualizations & Report Generation | Publication-grade charts, tables, and complete Methodology Report PDF | Pending Review |
| **Phase 6** | Final Review & Unstop Submission Alignment | Verifying dropdown IDs, final checks against brief | Pending Review |

---

## Phase 1: Data Exploration & Feature Preparation
- **Task 1.1**: Inspect data distributions across `matches.csv` (883 matches), `ball_by_ball.csv`, `competitions.csv`.
- **Task 1.2**: Verify consistency of player names vs IDs between `competition_team_player_mapping.csv`, `playing_eleven.csv`, and `ball_by_ball.csv`.
- **Task 1.3**: Validate extra runs, boundary flags, and wicket event types (exclude run-outs for bowler wickets).

---

## Phase 2: Match-State & Pressure Situation Index (PSI) Engine
- **Task 2.1: State Tracking**
  - Compute ball-by-ball cumulative runs, balls elapsed, legal balls remaining.
  - Track wickets fallen per innings dynamically.
  - Calculate targets for 2nd innings (merging revised target from `matches.csv` when DLS or rain affected).
- **Task 2.2: Formulation of PSI**
  - *2nd Innings (Chases)*:
    - Required Run Rate ($\text{RRR} = \frac{\text{Runs Needed}}{\text{Balls Remaining} / 6}$).
    - Resource Ratio ($\frac{\text{Wickets in Hand}}{\text{Overs Remaining}}$).
    - Leverage Index: Rate of change of win probability per ball.
  - *1st Innings (Setting Target)*:
    - Collapse leverage: Wickets fallen in first 6 overs / top order collapse.
    - Death overs leverage (Overs 16-20 with high impact on final competitive total).
  - *Tournament Leverage*:
    - Knockout matches vs Group stage weight.
- **Task 2.3: Validation of PSI**
  - Check whether known iconic clutch situations (e.g., World Cup games, IPL finals, tight final overs) receive top PSI scores.

---

## Phase 3: Player Metric Construction (Baseline vs Pressure)
- **Task 3.1: Batting Metrics**
  - **Baseline**: Overall T20 SR, Dot%, Boundary%, Dismissal Rate.
  - **High Pressure**: SR under high PSI, Boundary%, Dot% reduction, Scoring Efficiency.
  - **Clutch Delta ($\Delta \text{Bat}$)**: Quantifying over-performance or stability under severe pressure.
- **Task 3.2: Bowling Metrics**
  - **Baseline**: Overall T20 Economy, Wkt%, Dot%.
  - **High Pressure**: Economy under high PSI, Wicket strike rate, Dot Ball suppression.
  - **Clutch Delta ($\Delta \text{Bowl}$)**: Ability to restrict boundaries and take decisive wickets when the game is on the line.
- **Task 3.3: Competition Weighting**
  - Calibrate weights: IPL matches & T20 World Cup matches vs bilateral series to reflect bowling/batting depth.

---

## Phase 4: Regularization, Eligibility & Top 10 Selection
- **Task 4.1: Volume / Eligibility Filters**
  - Establish statistically robust sample size floors (e.g., minimum 100-150 balls faced in high-pressure situations for batters, minimum 100-120 balls bowled for bowlers).
- **Task 4.2: Bayesian Shrinkage**
  - Apply Empirical Bayes shrinkage to dampen extreme variance from small samples.
- **Task 4.3: Ranking Generation**
  - Generate Top 10 Batters and Top 10 Bowlers.
  - Map every ranked player to their exact name and player ID in the data pack for exact matching with Unstop dropdowns.

---

## Phase 5: Visualizations & Methodology Report Compilation
- **Task 5.1: High-Impact Visualizations**
  - Scatter plots: Baseline Performance vs Pressure Performance (highlighting the "Clutch Quadrant").
  - Distribution curves: PSI across match phases.
  - Player radar/spider charts comparing Top 3 batters and bowlers against cohort averages.
- **Task 5.2: Report Drafting (PDF)**
  - Section 1: Executive Summary & Cricket Philosophy.
  - Section 2: Mathematical Definition of Pressure (Formulas, Diagrams).
  - Section 3: Performance Metrics & Clutch Score Formulation.
  - Section 4: Sample Size Handling & Bayesian Regularization.
  - Section 5: The Top 10 Batters & Bowlers (Tables, Stats, Profiles, Tactical Justification).
  - Section 6: Sensitivity, Stability & Limitations.
  - Section 7: Strategic Recommendations for Rajasthan Royals Auction Strategy.

---

## Phase 6: Review & Final Verification
- Verify that every player in the Top 10 list is present in the dataset and dropdown options.
- Confirm consistency between the Methodology Report, tables, and final recommended rankings.

