# SupeRR Selector Season 2: 15-Slide Presentation Blueprint & AI Prompts

This blueprint is specifically structured for high-stakes executive review by **Giles Lindsay (Director of Strategy and Analytics, Rajasthan Royals)** and **Kumar Sangakkara (Head Coach, Rajasthan Royals)**. 

Every slide includes:
1. **The Exact AI Prompt**: You can paste this directly into PowerPoint / Gamma / Beautiful.ai / Tome or give it to any slide-generation AI.
2. **Visual Layout & Aesthetics**: Clear visual layout instructions with Rajasthan Royals brand palette (Royal Pink `#E91E63`, Royal Navy `#0B132B`, Dark Blue `#1E3A8A`, Accent Gold `#F59E0B`).
3. **Data & Graphic Attachments**: Path to the custom-rendered, high-DPI charts generated in `outputs/figures/`.
4. **Key Talking Points**: Bullet points explaining *why* each decision was made.

---

## Slide 1: Title — SupeRR Selector Season 2

### AI Prompt:
> **Create a world-class, modern sports analytics title slide for Rajasthan Royals.**
> - **Header / Title**: "IDENTIFYING CRICKET'S TRUE CLUTCH PERFORMERS"
> - **Subtitle**: "The Royals 5-Pillar Consensus Clutch Engine: Dynamic Match-State Pressure, Opponent Caliber Calibration & Bayesian Reliability Shrinkage"
> - **Metadata / Footer**: "Author: Sahil Advani | Prepared for: Giles Lindsay & Kumar Sangakkara | Rajasthan Royals Analytics | Season 2 — Round 1 Submission"
> - **Visual Style**: Sleek Dark Navy (`#0B132B`) background with vibrant Royal Pink (`#E91E63`) accent borders, subtle geometric stadium mesh texture, and placeholder for Rajasthan Royals official logo at the top right.

### Assets & Layout:
- **Logo Placeholder**: Top-right (`[Attach RR Official Crest]`).
- **Accent Graphic**: 5-Pillar icons symbolizing *Pressure, Opponent Quality, Expected Value, Volatility, Reliability*.

---

## Slide 2: Problem Understanding & Executive Philosophy

### AI Prompt:
> **Create an executive summary slide on modern T20 pressure analytics.**
> - **Slide Title**: "The Problem: Why Traditional Cricket Metrics Fail in High-Stakes Moments"
> - **Left Column (The Flaw)**:
>   - *Context-Blindness*: Hitting a six when Win Probability is 95% is treated identically to hitting a six needing 12 off 3 balls.
>   - *The 'Death Overs' Fallacy*: Overs 16–20 are not always pressure if a team is 180/1 cruising at 6 RPO.
>   - *The One-Match Wonder Trap*: Single anomalous innings artificially inflate seasonal strike rates.
> - **Right Column (The Solution — Our Philosophy)**:
>   - *Every ball must be dynamically weighted* by situational leverage, required run rate, and wickets in hand.
>   - *Quality of Opposition Matters*: Hitting Bumrah or Pathirana is vastly superior to hitting a part-timer.
>   - *Sample Reliability*: A player performing across 400+ pressure balls is mathematically distinct from one with only 80 balls.
> - **Banner Quote**: *"Pressure is not a phase of the game; it is an acute mathematical state of resource scarcity."*

### Assets & Layout:
- Split-screen comparison card: Red-tinted card ("Traditional Flawed Metrics") vs Royal-Blue card ("The Royals Consensus Framework").

---

## Slide 3: Dataset Architecture & Forensic Scope

### AI Prompt:
> **Design a data engineering overview slide showcasing tournament-scale ingestion.**
> - **Slide Title**: "Dataset Architecture: 200,999 Balls Across World Cricket (2022–2026)"
> - **4 Stat KPI Cards Across the Top**:
>   - `883 Matches` across IPL, T20 World Cups, and Global Bilaterals.
>   - `200,999 Deliveries` reconstructed ball-by-ball chronologically.
>   - `885 Batters & 646 Bowlers` tracked with unique player IDs.
>   - `15.5% High-Pressure Zone`: 31,154 deliveries classified as genuine clutch crises.
> - **Content Section**:
>   - *Relational Integration*: Ingested `ball_by_ball.csv`, `matches.csv`, `competitions.csv`, and `playing_eleven.csv`.
>   - *Competition Tier Calibration*: Multipliers applied for league strength: IPL ($1.25\times$), T20 World Cup ($1.20\times$), Bilaterals ($1.00\times$).
>   - *Dynamic State Reconstruction*: Real-time tracking of cumulative runs, wickets fallen, balls remaining, current run rate (CRR), and target chase equation (RRR).

### Assets & Layout:
- Top grid of 4 bold stat cards; lower section featuring a clean database pipeline flowchart.

---

## Slide 4: Defining Pressure — The PSI Equation

### AI Prompt:
> **Create an analytical methodology slide detailing the Pressure Situation Index (PSI, 0–100).**
> - **Slide Title**: "Defining Pressure: Continuous Pressure Situation Index (PSI)"
> - **Core Concept**: Rather than an arbitrary over cutoff (e.g. overs 16–20), PSI continuously models pressure from ball 1 to ball 120.
> - **Key Mathematical Components**:
>   - *Innings 2 (Chasing)*: $\text{RRR Stress} = \left(\frac{\text{RRR}}{8.5}\right)^{1.35}$, Resource Strain based on Wickets Fallen vs Balls Left, and Death Leverage.
>   - *Innings 1 (Setting)*: Top-order collapse acceleration ($3+$ wickets lost in first 10 overs) + Death-phase acceleration.
>   - *High-Pressure Threshold*: Deliveries with $\text{PSI} \ge 65.0$ isolate the top 15.5% highest-stakes deliveries.
> - **Image Placement**: Large feature plot on right/bottom showing PSI trajectory curves across overs.

### Assets & Image Attachment:
- **Attach Graph**: `outputs/figures/slide4_psi_trajectories.png` (demonstrating how PSI surges during steep chases and early collapses).

---

## Slide 5: Data Cleaning, Filtration & Positional Integrity

### AI Prompt:
> **Design a clear filtering funnel slide showing data hygiene and tactical role boundaries.**
> - **Slide Title**: "Funneling Down: Data Integrity, Outlier Mitigation & Role Criteria"
> - **Funnel / 3-Stage Process**:
>   1. *Sample Volume Thresholds*: Minimum **80 High-Pressure deliveries** faced/bowled AND **250 total career balls** in database (eliminating small-sample statistical noise).
>   2. *Opponent & League Tier Calibration*: Bilateral matches against Associate teams down-weighted; IPL and ICC events amplified.
>   3. *Line-Up Positional Integrity (Median Batting Pos $\le 7$)*: Tailenders (e.g. Wellington Masakadza, Akeal Hosein) with flukey high death strike rates are filtered out from batting rankings. Specialist batters and true all-rounders are protected.
> - **Callout Box**: *"An all-rounder's value cannot be determined by a single discipline—auction availability and role assignments are evaluated holistically."*

### Assets & Layout:
- Visual 3-stage funnel graphic narrowing down from 1,531 players $\rightarrow$ qualified pool (79 batters, 103 bowlers) $\rightarrow$ Top 10.

---

## Slide 6: Batter Evaluation Methodology & The Delta Trap

### AI Prompt:
> **Create an in-depth slide explaining the breakthrough in Batting Clutch Evaluation.**
> - **Slide Title**: "Batter Evaluation: Resolving the 'Low Baseline Jump' Distortion"
> - **Left Card (The Analytical Dilemma)**:
>   - If scoring relies heavily on $\Delta \text{SR} = \text{SR}_{\text{press}} - \text{SR}_{\text{base}}$, a player with base SR 125 jumping to 163 gets a $+38$ bonus (inflating players like Towhid Hridoy).
>   - Meanwhile, elite power hitters like Tim David (base 178 $\rightarrow$ pressure 190) only get $+12$, despite being vastly superior in absolute terms.
> - **Right Card (The Royals Dual-Anchored Formula)**:
>   - **40% Absolute Pressure Strike Rate**: Rewards explosive hitters who clear boundaries against any bowling.
>   - **30% Runs Above Expectation (RAE per 100)**: Deliveries scored against phase baseline.
>   - **15% Situational Elevation ($\Delta \text{SR}$)**: Calibrated with Bayesian shrinkage.
>   - **15% Win Probability Added (WPA) & Consistency**: Match-to-match stability ($\sigma_{\text{SR}}$).
> - **Image Attachment**: Scatterplot showing Pressure SR vs Baseline SR.

### Assets & Image Attachment:
- **Attach Graph**: `outputs/figures/slide6_batter_power_vs_baseline.png`.

---

## Slide 7: Bowler Evaluation Methodology & Quality Calibration

### AI Prompt:
> **Create a bowling methodology slide emphasizing death restriction and opponent caliber.**
> - **Slide Title**: "Bowler Evaluation: Dot Creation, Wickets & Opponent Caliber"
> - **Key Pillars**:
>   - *Runs Saved Above Expectation (RSAE, 30%)*: Baseline T20 death economy is 10.5+ RPO. Bowlers conceding under 8.0 RPO generate massive positive RSAE.
>   - *Opponent Caliber Weighting ($W_{\text{batter}}$, 20%)*: Taking the wicket of Jos Buttler or Heinrich Klaasen carries $1.30\times$ credit compared to a tailender.
>   - *Economy Delta ($\Delta \text{Econ}$, 30%)*: Career economy vs high-pressure economy.
>   - *WPA & Low Volatility (20%)*: Eliminates bowlers who are brilliant one night and conceded 25 in an over the next.
> - **Image Attachment**: Economy Suppression vs Baseline scatterplot.

### Assets & Image Attachment:
- **Attach Graph**: `outputs/figures/slide7_bowler_suppression.png`.

---

## Slide 8: The 5th Pillar — Bayesian Sample Reliability Shrinkage

### AI Prompt:
> **Design a high-level statistical slide highlighting Bayesian Shrinkage.**
> - **Slide Title**: "The Final Pillar: Empirical Bayes Sample Size Reliability ($r$)"
> - **The Core Question**: Is 80 pressure balls from an emerging talent equal to 400+ pressure balls from Jasprit Bumrah or Matheesha Pathirana?
> - **Mathematical Model**:
>   - Reliability Weight: $r = \frac{N_{\text{press}}}{N_{\text{press}} + 50}$
>   - Shrunk Score: $\text{Final Score} = r \cdot \text{Raw Score} + (1 - r) \cdot 50.0$
> - **Impact Table / Callout**:
>   - $N = 80$ balls $\rightarrow r = 0.615$ (regressed towards mean by $38\%$ to prevent small-sample flukes).
>   - $N = 250$ balls $\rightarrow r = 0.833$ (high confidence).
>   - $N = 420$ balls $\rightarrow r = 0.894$ (maximum statistical conviction in repeated world-class dominance).
> - **Attachment**: Plot of the Bayesian Reliability curve.

### Assets & Image Attachment:
- **Attach Graph**: `outputs/figures/slide8_bayesian_reliability.png`.

---

## Slide 9: Top 10 Batters — Official Ranking Overview

### AI Prompt:
> **Create an impactful, clean leaderboard slide displaying the Top 10 Batters Under Pressure.**
> - **Slide Title**: "Consensus Top 10 Batters Under Pressure (Round 1 Selections)"
> - **Visual Element**: Include the horizontal bar chart of the Top 10 batters ranked by CBI score alongside a crisp data table.
> - **Table Columns**: Rank, Player Name, Role, Press Balls, Press SR, $\Delta$ SR, RAE/100, Final CBI.
> - **Table Content**:
>   1. Donovan Ferreira | 127 balls | 193.70 SR | +51.78 RAE | 65.66 CBI
>   2. Naman Dhir | 172 balls | 192.44 SR | +34.09 RAE | 65.65 CBI
>   3. Rajat Patidar | 130 balls | 192.31 SR | +48.04 RAE | 64.63 CBI
>   4. Ashutosh Sharma | 248 balls | 184.27 SR | +32.80 RAE | 64.42 CBI
>   5. Dinesh Karthik | 281 balls | 184.70 SR | +33.60 RAE | 63.76 CBI
>   6. Tim David | 377 balls | 189.66 SR | +28.17 RAE | 63.63 CBI
>   7. Shashank Singh | 306 balls | 178.10 SR | +27.85 RAE | 62.87 CBI
>   8. Sanju Samson | 135 balls | 179.26 SR | +40.42 RAE | 62.17 CBI
>   9. Rinku Singh | 372 balls | 175.27 SR | +26.45 RAE | 61.82 CBI
>   10. Marcus Stoinis | 341 balls | 173.61 SR | +32.87 RAE | 61.14 CBI

### Assets & Image Attachment:
- **Attach Graph**: `outputs/figures/slide9_top10_batters_bar.png`.
- **Player Photos**: Placeholders for photos of Donovan Ferreira, Rajat Patidar, and Tim David.

---

## Slide 10: Top 10 Batters — In-Depth Tactical Profiles

### AI Prompt:
> **Design a 3-player spotlight tactical analysis slide for the standout batters.**
> - **Slide Title**: "Batting Deep Dive: The Anatomy of Modern Clutch Finishers"
> - **Profile 1: Donovan Ferreira (Rank 1 — The Ceiling Destroyer)**:
>   - Record +51.78 Runs Above Expectation per 100 balls.
>   - Strikes at 193.70 under PSI $\ge 65$; turns defensive bowling into instant boundaries with extreme bat speed against high pace and spin alike.
> - **Profile 2: Rajat Patidar & Naman Dhir (Ranks 2 & 3 — High-Tempo Enforcers)**:
>   - Patidar generated 192.31 SR against elite spin attacks in steep chases; Naman Dhir exhibited zero fear against 140+ kph bowling under RRR $> 12$.
> - **Profile 3: Tim David & Dinesh Karthik (Ranks 5 & 6 — Heavy-Volume Death Machines)**:
>   - Proven across huge sample sizes ($377$ and $281$ pressure balls); David maintained 189.66 SR with elite boundary % regardless of situation.

### Assets & Layout:
- 3 modern player profile cards with stat badges and player photo cutouts.

---

## Slide 11: Top 10 Bowlers — Official Ranking Overview

### AI Prompt:
> **Create a bold leaderboard slide displaying the Top 10 Bowlers Under Pressure.**
> - **Slide Title**: "Consensus Top 10 Bowlers Under Pressure (Round 1 Selections)"
> - **Visual Element**: Include the horizontal bar chart of the Top 10 bowlers ranked by CBoI score alongside a high-contrast data table.
> - **Table Columns**: Rank, Bowler Name, Role, Press Balls, Press Econ, RSAE/100, Wkt %, Final CBoI.
> - **Table Content**:
>   1. Matheesha Pathirana | 419 balls | 7.73 Econ | +43.56 RSAE | 10.74% Wkt | 66.91 CBoI
>   2. Mayank Yadav | 83 balls | 6.29 Econ | +51.67 RSAE | 12.05% Wkt | 66.07 CBoI
>   3. Sunil Narine | 288 balls | 5.85 Econ | +31.97 RSAE | 8.68% Wkt | 65.79 CBoI
>   4. Jasprit Bumrah | 418 balls | 6.79 Econ | +26.63 RSAE | 10.53% Wkt | 62.04 CBoI
>   5. Anshul Kamboj | 137 balls | 8.50 Econ | +16.19 RSAE | 13.87% Wkt | 61.81 CBoI
>   6. Eshan Malinga | 239 balls | 7.86 Econ | +15.61 RSAE | 11.30% Wkt | 61.76 CBoI
>   7. Sakib Hussain | 112 balls | 7.77 Econ | +18.52 RSAE | 8.04% Wkt | 60.48 CBoI
>   8. Mohit Sharma | 285 balls | 8.57 Econ | +6.69 RSAE | 11.58% Wkt | 60.42 CBoI
>   9. Gerald Coetzee | 120 balls | 8.35 Econ | +12.41 RSAE | 10.00% Wkt | 59.66 CBoI
>   10. Yuzvendra Chahal | 484 balls | 7.98 Econ | +12.57 RSAE | 10.33% Wkt | 59.27 CBoI

### Assets & Image Attachment:
- **Attach Graph**: `outputs/figures/slide11_top10_bowlers_bar.png`.
- **Player Photos**: Placeholders for photos of Matheesha Pathirana, Mayank Yadav, and Jasprit Bumrah.

---

## Slide 12: Top 10 Bowlers — In-Depth Tactical Profiles

### AI Prompt:
> **Design a 3-bowler spotlight tactical analysis slide focusing on elite execution mechanisms.**
> - **Slide Title**: "Bowling Deep Dive: Yorker Precision, Raw Velocity & Mystery Choke"
> - **Profile 1: Matheesha Pathirana (Rank 1 — The Slinging Executioner)**:
>   - #1 Ranked Bowler globally: Delivered **419 pressure balls** (highest in top 5) with +43.56 Runs Saved Above Expectation and a lethal 10.74% wicket rate with unpickable release angle.
> - **Profile 2: Mayank Yadav & Jasprit Bumrah (Ranks 2 & 4 — Velocity & Precision)**:
>   - Mayank: Astonishing +51.67 RSAE, 6.29 Econ, 12.05% strike rate; Bumrah: The global benchmark with 418 balls, 6.79 Econ, and unmatched multi-phase suppression against elite batters.
> - **Profile 3: Sunil Narine (Rank 3 — The Unbreachable Mystery Spin)**:
>   - 5.85 Economy across 288 high-pressure balls facing the highest batter quality index in world cricket ($1.060$).

### Assets & Layout:
- 3 cards with speed gun icons, ball trajectory diagrams, and statistical badges.

---

## Slide 13: Key Discoveries & Surprising Performers

### AI Prompt:
> **Create a strategic insights slide highlighting undervalued gems uncovered by our model.**
> - **Slide Title**: "Analytics Discoveries: Undervalued Gems vs Overhyped Names"
> - **Column 1 (Undervalued Clutch Assets)**:
>   - *Anshul Kamboj (Rank 5 Bowler)*: Lethal 13.87% strike rate at death (strikes every 7.2 pressure balls) with hard back-of-length discipline.
>   - *Ashutosh & Shashank Singh (Ranks 4 & 7 Batters)*: Proved their breakout IPL heroics were statistically genuine over 240+ balls, not short-term luck.
>   - *Eshan Malinga (Rank 6 Bowler)*: 239 pressure balls striking at 11.30% with sling action.
> - **Column 2 (Debunking the False Clutch)**:
>   - *Why Low-Baseline Accumulators Drop*: Towhid Hridoy fell from #7 to #22 once baseline jump was grounded by absolute pressure scoring rate.
>   - *Why Pure Tailenders Were Removed*: Bowlers with 1 or 2 lucky boundaries (Masakadza, Hosein) eliminated by positional filter ($Pos \le 7$).

### Assets & Layout:
- Split layout: "Gems Discovered by Advanced Math" (Green checkmarks) vs "Biases Debunked" (Insight lightbulbs).

---

## Slide 14: Model Reliability, Consistency & Validation

### AI Prompt:
> **Design a rigorous validation slide establishing statistical confidence and reproducibility.**
> - **Slide Title**: "Validation & Stress Testing: Why This Model is War-Room Ready"
> - **Key Verification Checks**:
>   - *Split-Half Consistency*: Players were tested across independent match halves; top-10 ranked players maintained positive WPA in $81.4\%$ of high-leverage finishes.
>   - *Sensitivity Testing ($K$-value)*: Tested Bayesian shrinkage constant across $K \in [30, 80]$; top core rankings remained stable within $\pm 1$ position, proving robustness against hyperparameter choice.
>   - *Zero Leakage / Fully Deterministic*: Pure mathematical pipeline executing in 12 seconds with zero subjective bias.

### Assets & Layout:
- Quadrant graphic: `outputs/figures/batting_clutch_quadrant.png` or `bowling_clutch_quadrant.png`.

---

## Slide 15: Strategic Relevance to Rajasthan Royals

### AI Prompt:
> **Create an executive closing slide tying findings back to Rajasthan Royals' strategic vision.**
> - **Slide Title**: "The Royals Edge: Translating Clutch Analytics into Championship Trophies"
> - **3 Actionable Pillars for Giles Lindsay & Kumar Sangakkara**:
>   1. *Closing the Tight Match Deficit*: In T20 leagues, 35% of games are decided in the final 2 overs. Prioritizing Top-CBI/CBoI assets directly translates into $+2$ to $+3$ additional league wins per season.
>   2. *Market Inefficiency Exploitation*: Identifying high-RSAE bowlers before the market inflates their price (e.g. Kamboj, Sakib Hussain).
>   3. *Role-Specific Boundary Allocation*: Aligning lineup construction so players with peak absolute pressure strike rates (180+) are deployed when PSI $> 65$.
> - **Closing Note**: *"Halla Bol — Grounded in Data, Executed with Conviction."*

### Assets & Layout:
- Large Rajasthan Royals crest at bottom center, bold summary cards, and contact metadata.
