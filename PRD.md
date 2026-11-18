# Product Requirements Document (PRD)

## 1. Executive Summary & Objective
**Competition**: SupeRR Selector Season 2 — Rajasthan Royals IPL Auction Strategy Hackathon (Unstop).  
**Challenge**: Round 1 — *Identify the Most Reliable Players Under Pressure*.  
**Goal**: Build a rigorous, mathematically sound, and domain-informed cricket analytics system that:
1. Quantifies pressure for every ball in T20 cricket (IPL & T20I matches, 2022 onwards).
2. Measures how individual batters and bowlers perform in high-pressure situations compared to their baseline/ordinary levels.
3. Produces two defensible, high-conviction **Top 10 Player Rankings**:
   - **Top 10 Batters Under Pressure** (Rank 1 to 10)
   - **Top 10 Bowlers Under Pressure** (Rank 1 to 10)
4. Generates an elite **Methodology Report** (PDF format) covering mathematical formulations, pressure definitions, metric engineering, sample size thresholds, visualizations, validation tests, and franchise-level strategic insights.

---

## 2. Key Stakeholders & Audience
- **Rajasthan Royals Analytics & Strategy Team** (Director of Strategy & Analytics, Head Coach, Data Scientists).
- **Evaluation Criteria**:
  - Rigor & clarity of the pressure definition (must not be arbitrary; must capture the dynamic nature of T20 cricket).
  - Soundness of performance measurement (relative to player baseline, match context, role adjustment).
  - Fair comparisons (sample size handling, bayesian shrinkage / reliability filtering, balance between IPL and T20Is).
  - Reproducibility and transparency.
  - Actionable insights backed by data, not reputation or bias.

---

## 3. Scope & Deliverables

### Deliverable 1: Top 10 Player Selection (Unstop Dropdowns)
- **Top 10 Batters**: Ranked 1 through 10 (no duplicates, matching the methodology report).
- **Top 10 Bowlers**: Ranked 1 through 10 (no duplicates, matching the methodology report).

### Deliverable 2: Methodology Report (Document Upload)
Structured as required by the brief:
1. **Introduction & Strategic Context**: Why pressure performance drives auction premium and playoff wins in IPL.
2. **Pressure Definition Framework**:
   - Dynamic context factors: Required Run Rate (RRR) vs Current Run Rate (CRR), wickets fallen vs remaining resources, balls remaining, phase of the match (Powerplay, Middle, Death), knockout vs league match context.
   - Mathematical formulation: Win Probability Added (WPA) leverage / Leverage Index (LI) or Context-Weighted Pressure Index (PI).
3. **Performance Metrics & Rating System**:
   - **Batters**: Strike Rate under pressure ($\Delta \text{SR}$), Boundary %, Dot Ball Suppression, Dismissal Risk, Win Probability Contribution, Wickets In Hand context.
   - **Bowlers**: Economy Rate under pressure ($\Delta \text{Econ}$), Dot Ball %, Boundary Conceded %, Wicket Taking Rate (Wkts / balls), Death Over execution.
   - **Relative Delta Formulation**: Performance in Pressure vs. Performance in Normal / Baseline ($\Delta_{\text{Player}}$) to isolate true "clutch" ability from generic baseline quality.
4. **Sample Size & Fair Comparison Framework**:
   - Minimum volume filters (balls faced / balls bowled in pressure situations).
   - Bayesian shrinkage / Empirical Bayes weighting to avoid small-sample flukes.
   - Competition weighting (IPL vs T20I level of competition calibration).
5. **Empirical Findings & Evidence**:
   - Top 10 Batter table with complete statistical profiles and percentile ranks.
   - Top 10 Bowler table with complete statistical profiles and percentile ranks.
   - Radar charts / scatter plots showing Baseline vs. Clutch Delta.
6. **Reliability, Sensitivity & Limitations**:
   - Year-on-year stability test / bootstrap confidence intervals.
   - Known limitations (e.g., batting position shifts, pitch conditions).

---

## 4. Data Inputs & Architecture
The analysis is powered by the provided official dataset (`6af458274c1e8_data_pack.zip`):
- `ball_by_ball.csv`: 33 columns covering granular ball-by-ball actions, runs, wickets, extras, pace/spin, dismissals, timings.
- `matches.csv`: 883 matches, match dates, venues, knock_out flags, toss details, revised overs/targets.
- `competitions.csv`: 141 competitions (IPL 2022-2026, T20I series, World Cups).
- `playing_eleven.csv`: Player lineups, captaincy, wicket-keeping, impact player flags.
- `competition_team_player_mapping.csv` & `teams.csv`: Player and team registry.

---

## 5. Success Metrics
- **Mathematical Integrity**: Coherent formulas with zero data leakage.
- **Explainability**: Intuitive for a cricket analyst or coach while statistically robust for a quantitative analyst.
- **Reproducibility**: End-to-end automated pipeline executing without errors.
- **Report Aesthetic**: Polished, publication-ready styling meeting high corporate/sports analytics presentation standards.

