"""
build_presentation_deck.py
Generates the complete 15-slide master widescreen presentation deck (.pptx)
Customized with Rajasthan Royals official branding:
Navy (#0B132B), Royal Pink (#E91E63), Deep Blue (#1E3A8A), Light Slate (#F8FAFC)
Personalized tactical context for Giles Lindsay, Kumar Sangakkara, Jofra Archer, Sanju Samson, Riyan Parag, and Sandeep Sharma.
"""
import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')
PPTX_PATH = os.path.join(OUTPUT_DIR, 'Rajasthan_Royals_SupeRR_Selector_Season_2_Presentation.pptx')

# Colors
C_NAVY = RGBColor(11, 19, 43)        # #0B132B
C_PINK = RGBColor(233, 30, 99)       # #E91E63
C_BLUE = RGBColor(30, 58, 138)       # #1E3A8A
C_WHITE = RGBColor(255, 255, 255)
C_DARK = RGBColor(15, 23, 42)        # #0F172A
C_GRAY = RGBColor(100, 116, 139)     # #64748B
C_LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
C_CARD_BG = RGBColor(255, 255, 255)
C_CARD_BORDER = RGBColor(226, 232, 240)
C_GOLD = RGBColor(217, 119, 6)

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="SUPERR SELECTOR SEASON 2 | RAJASTHAN ROYALS STRATEGY"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = C_PINK
        
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY

    def add_bg(slide, dark=False):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_NAVY if dark else C_LIGHT_BG
        bg.line.fill.background()
        
        # Pink accent line at top
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        accent.fill.solid()
        accent.fill.fore_color.rgb = C_PINK
        accent.line.fill.background()

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Navy)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, dark=True)
    
    # Title Box
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "RAJASTHAN ROYALS | SUPERR SELECTOR SEASON 2"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_PINK
    
    p = tf1.add_paragraph()
    p.text = "Identifying Cricket's True Clutch Performers"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(14)
    
    p = tf1.add_paragraph()
    p.text = "The Royals 5-Pillar Consensus Clutch Engine: Dynamic Match Pressure Modeling, Opponent Quality Calibration & Bayesian Reliability Shrinkage"
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(28)
    
    p = tf1.add_paragraph()
    p.text = "Author: Sahil Advani   |   Prepared for: Giles Lindsay (Director of Strategy) & Kumar Sangakkara (Head Coach)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_PINK

    # ==========================================
    # SLIDE 2: PROBLEM UNDERSTANDING & PHILOSOPHY
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "The Problem: Why Traditional Cricket Metrics Fail in High-Stakes Moments")
    
    # Left Box: Traditional Flaws
    card1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = RGBColor(254, 202, 202)
    
    tf = card1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    
    p = tf.paragraphs[0]
    p.text = "THE FLAW IN TRADITIONAL EVALUATION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(220, 38, 38)
    p.space_after = Pt(12)
    
    bullets_flaw = [
        ("Context-Blind Accumulation: ", "A boundary when Win Probability is 95% is credited the same as a boundary needing 12 off 3 balls."),
        ("The 'Death Overs' Fallacy: ", "Overs 16–20 are not inherently pressure. If a team is 170/1 cruising at 6 RPO, bowling economy is not 'clutch' execution."),
        ("The One-Match Wonder Trap: ", "Single anomalous 20-run cameos artificially inflate strike rates without testing repeatable composure."),
        ("Quality Blindness: ", "Scoring 18 off an unheralded 6th bowler is treated identically to hitting Jasprit Bumrah or Sunil Narine.")
    ]
    for b_title, b_desc in bullets_flaw:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(10)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(8)

    # Right Box: The Royals Solution
    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    card2.fill.solid()
    card2.fill.fore_color.rgb = C_WHITE
    card2.line.color.rgb = RGBColor(191, 219, 254)
    
    tf = card2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    
    p = tf.paragraphs[0]
    p.text = "THE ROYALS ANALYTICAL PHILOSOPHY"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(12)
    
    bullets_sol = [
        ("Dynamic Leverage (PSI): ", "Every single delivery is continuously weighted by exact situational resource scarcity and RRR stress."),
        ("Head-to-Head (H2H) Calibration: ", "Individual Bayesian ratings weight performances against top bowlers/batters significantly higher."),
        ("Expected Value Baselines (RAE/RSAE): ", "Measures runs scored or saved against ball-by-ball empirical phase expectations."),
        ("Bayesian Sample Reliability (r): ", "Insulates our strategy against small-sample flukes (80 balls vs 420 balls are statistically distinguished).")
    ]
    for b_title, b_desc in bullets_sol:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(10)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(8)
        
    p = tf.add_paragraph()
    p.text = "\"Pressure is not a fixed over block; it is an acute mathematical state of resource scarcity.\""
    p.font.italic = True
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PINK

    # ==========================================
    # SLIDE 3: DATASET OVERVIEW & SCOPE
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Dataset Architecture: 200,999 Deliveries Across World Cricket (2022–2026)")
    
    # 4 Top KPI Cards
    kpis = [
        ("883", "MATCHES INGESTED", "IPL, World Cups & Global Bilaterals"),
        ("200,999", "BALLS RECONSTRUCTED", "Chronological ball-by-ball states"),
        ("1,531", "PLAYERS TRACKED", "885 Batters & 646 Bowlers mapped"),
        ("15.5%", "HIGH-PRESSURE ZONE", "31,154 deliveries with PSI >= 65.0")
    ]
    for i, (val, title, sub) in enumerate(kpis):
        x = Inches(0.8 + i * 2.95)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(2.8), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.margin_top = Inches(0.15)
        tf.margin_left = Inches(0.15)
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = C_PINK if i in [0, 3] else C_BLUE
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(7.5)
        p.font.color.rgb = C_GRAY

    # Details Box Below
    card_det = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(11.7), Inches(3.6))
    card_det.fill.solid()
    card_det.fill.fore_color.rgb = C_WHITE
    card_det.line.color.rgb = C_CARD_BORDER
    tf = card_det.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    
    p = tf.paragraphs[0]
    p.text = "DATA ENGINEERING & COMPETITION TIER HIERARCHY"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)
    
    eng_bullets = [
        ("Relational Multi-Table Joining: ", "Unified ball_by_ball.csv, matches.csv, competitions.csv, teams.csv, and playing_eleven.csv into a unified columnar schema."),
        ("Dynamic In-Match State Reconstruction: ", "Accurately derived ball-by-ball legal counts, extras allocation, cumulative innings total, wickets fallen, and target chase equations."),
        ("Competition Strength Multipliers: ", "Calibrated by quality of opposition: IPL (1.25x tier weight) and T20 World Cups (1.20x tier weight) take precedence over low-ranked Associate bilaterals (1.00x)."),
        ("Knockout Leverage Boost: ", "Knockout matches (Semi-Finals, Finals, Eliminators) carry a 1.15x high-stakes situational multiplier.")
    ]
    for b_title, b_desc in eng_bullets:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(10.5)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(10)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 4: DEFINING PRESSURE (PSI)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Defining Pressure: Continuous Pressure Situation Index (PSI, 0–100)")
    
    # Left Text
    c_psi = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.2))
    c_psi.fill.solid()
    c_psi.fill.fore_color.rgb = C_WHITE
    c_psi.line.color.rgb = C_CARD_BORDER
    tf = c_psi.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    
    p = tf.paragraphs[0]
    p.text = "THE MATHEMATICAL ARCHITECTURE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(10)
    
    psi_pts = [
        ("Innings 2 (The Chase Equation): ", "Pressure is driven by Required Run Rate stress: (RRR / 8.5)^1.35. Combined with Resource Strain (wickets lost vs balls remaining) and Death Leverage."),
        ("Innings 1 (Target Setting): ", "Pressure is modeled through Top-Order Collapse rate (3+ wickets lost inside Powerplay/middle overs) and Death-Over acceleration urgency."),
        ("The High-Pressure Zone (PSI >= 65.0): ", "Captures the top 15.5% most decisive deliveries in T20 cricket, discarding meaningless garbage-time overs."),
        ("Tactical Alignment for RR: ", "Mirrors situations where Sandeep Sharma or Jofra Archer defend 10 off the final over, or Sanju Samson/Riyan Parag face a steep chase.")
    ]
    for b_t, b_d in psi_pts:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_t
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_d
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(7)

    # Right Image: PSI trajectories
    psi_img = os.path.join(FIGURES_DIR, 'slide4_psi_trajectories.png')
    if os.path.exists(psi_img):
        s4.shapes.add_picture(psi_img, Inches(6.3), Inches(1.6), width=Inches(6.2))

    # ==========================================
    # SLIDE 5: CLEANING & POSITIONAL INTEGRITY
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Data Cleaning, Filtration & Positional Line-Up Integrity")
    
    steps = [
        ("STAGE 1: SAMPLE FLOOR", "Eliminating Small-Sample Flukes", 
         "Minimum 80 High-Pressure deliveries faced/bowled AND 250 total balls in database.\n• Eliminates one-match wonders who had a single lucky cameo or purple patch.\n• Qualified pool: 79 specialist batters & 103 bowlers."),
        ("STAGE 2: QUALITY OF OPPOSITION", "Discounting Associate Mismatches", 
         "Performances against low-ranked Associate teams (e.g. UAE, Zimbabwe) adjusted by opponent tier.\n• High-stakes IPL & ICC events weighted up to 1.25x.\n• Prevents artificial stat-padding in non-competitive bilateral fixtures."),
        ("STAGE 3: POSITIONAL INTEGRITY", "Filtering Tailenders & Protecting All-Rounders", 
         "Enforced Median Batting Position <= 7 for Batting Rankings.\n• Eliminates tailenders (Masakadza, Akeal Hosein) with flukey high death strike rates.\n• Protects genuine All-Rounders (Nitish Reddy, Liam Livingstone) evaluated across both skills.")
    ]
    for i, (title, sub, body) in enumerate(steps):
        x = Inches(0.8 + i * 3.95)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.8), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_PINK if i == 0 else (C_BLUE if i == 1 else C_GOLD)
        
        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_after = Pt(10)
        
        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(9)
        p.font.color.rgb = C_GRAY

    # ==========================================
    # SLIDE 6: BATTER EVALUATION METHODOLOGY
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Batter Evaluation: Resolving the 'Low Baseline Jump' Distortion")
    
    # Left Card
    c_bat = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.2))
    c_bat.fill.solid()
    c_bat.fill.fore_color.rgb = C_WHITE
    c_bat.line.color.rgb = C_CARD_BORDER
    tf = c_bat.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
    
    p = tf.paragraphs[0]
    p.text = "THE REBALANCED 4-PILLAR BATTING FORMULA"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    
    b_formula = [
        ("40% Absolute Pressure Strike Rate: ", "Rewards elite hitters (SR 180–195+) who destroy bowling under pressure regardless of baseline."),
        ("30% Runs Above Expectation (RAE/100): ", "Contextual runs generated above ball-by-ball baseline, scaled by bowler H2H caliber."),
        ("15% Situational Elevation (Delta SR): ", "Grounded with Bayesian shrinkage to eliminate the 'Towhid Hridoy bias' (low baseline jump)."),
        ("15% WPA & Low Volatility: ", "Penalizes match-to-match standard deviation so high-ceiling consistency is rewarded.")
    ]
    for b_t, b_d in b_formula:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_t
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_d
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(6)
        
    p = tf.add_paragraph()
    p.text = "RR Tactical Relevance: Complements Sanju Samson and Riyan Parag by finding fearless boundary hitters who elevate RPO when pressure spikes."
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = C_PINK

    # Right Image
    bat_img = os.path.join(FIGURES_DIR, 'slide6_batter_power_vs_baseline.png')
    if os.path.exists(bat_img):
        s6.shapes.add_picture(bat_img, Inches(6.3), Inches(1.6), width=Inches(6.2))

    # ==========================================
    # SLIDE 7: BOWLER EVALUATION METHODOLOGY
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Bowler Evaluation: Dot Creation, Wickets & Opponent Caliber Calibration")
    
    # Left Card
    c_bowl = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.2))
    c_bowl.fill.solid()
    c_bowl.fill.fore_color.rgb = C_WHITE
    c_bowl.line.color.rgb = C_CARD_BORDER
    tf = c_bowl.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
    
    p = tf.paragraphs[0]
    p.text = "THE 4-PILLAR BOWLING ARCHITECTURE"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    
    bo_formula = [
        ("30% Runs Saved Above Expectation (RSAE): ", "Baseline T20 death economy is 10.5+ RPO. Bowlers conceding <8.0 RPO generate massive positive run savings."),
        ("30% Opposition & H2H-Weighted Delta Econ: ", "Career economy vs pressure economy, scaled by batter caliber weights (e.g. facing Klaasen/Pooran = 1.30x)."),
        ("20% Pressure Wickets & Strike Rate: ", "Rewarding critical breakthrough capability in defensive death overs."),
        ("20% WPA & Economy Stability: ", "Penalizes high variance (eliminating bowlers who have 1 good over followed by conceding 25).")
    ]
    for b_t, b_d in bo_formula:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_t
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_d
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(6)
        
    p = tf.add_paragraph()
    p.text = "RR Tactical Relevance: Pairs with Jofra Archer and Sandeep Sharma by providing lethal yorker execution and boundary choke at overs 17–20."
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    # Right Image
    bowl_img = os.path.join(FIGURES_DIR, 'slide7_bowler_suppression.png')
    if os.path.exists(bowl_img):
        s7.shapes.add_picture(bowl_img, Inches(6.3), Inches(1.6), width=Inches(6.2))

    # ==========================================
    # SLIDE 8: BAYESIAN RELIABILITY SHRINKAGE
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "The 5th Pillar: Empirical Bayes Sample Size Reliability (r)")
    
    c_rel = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.2))
    c_rel.fill.solid()
    c_rel.fill.fore_color.rgb = C_WHITE
    c_rel.line.color.rgb = C_CARD_BORDER
    tf = c_rel.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
    
    p = tf.paragraphs[0]
    p.text = "INSULATING AGAINST SMALL-SAMPLE NOISE"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    
    rel_pts = [
        ("The Analytical Dilemma: ", "Is 80 pressure balls from an emerging player equal to 420+ balls from Jasprit Bumrah or Matheesha Pathirana?"),
        ("Bayesian Shrinkage Model: ", "r = N / (N + 50.0). Final Score = r * Raw Score + (1 - r) * 50.0."),
        ("Small Sample (N = 80 balls): ", "r = 0.615. Shrunk by 38% towards average to guard against small-sample randomness."),
        ("Large Sample (N = 420 balls): ", "r = 0.894. Trusted near 90% as proven, repeatable world-class execution across multiple seasons.")
    ]
    for b_t, b_d in rel_pts:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_t
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_d
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(6)

    rel_img = os.path.join(FIGURES_DIR, 'slide8_bayesian_reliability.png')
    if os.path.exists(rel_img):
        s8.shapes.add_picture(rel_img, Inches(6.3), Inches(1.6), width=Inches(6.2))

    # ==========================================
    # SLIDE 9: TOP 10 BATTERS OVERVIEW
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Consensus Top 10 Batters Under Pressure (Round 1 Selections)")
    
    # Left Chart
    b_bar = os.path.join(FIGURES_DIR, 'slide9_top10_batters_bar.png')
    if os.path.exists(b_bar):
        s9.shapes.add_picture(b_bar, Inches(0.8), Inches(1.6), width=Inches(6.0))
        
    # Right Table
    top_b = pd.read_csv('outputs/official_top_10_batters.csv')
    table_shape = s9.shapes.add_table(11, 6, Inches(7.0), Inches(1.6), Inches(5.5), Inches(5.2))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(0.6)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(0.8)
    tbl.columns[3].width = Inches(0.8)
    tbl.columns[4].width = Inches(0.8)
    tbl.columns[5].width = Inches(0.7)
    
    headers = ["Rank", "Batter", "Press SR", "RAE/100", "Reliab", "CBI"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER
        
    for row_idx, r in top_b.iterrows():
        vals = [f"#{row_idx+1}", r['player_name'], f"{r['raw_press_sr']:.1f}", f"+{r['rae_per_100']:.1f}", f"{r['reliability_weight']:.2f}", f"{r['Ensemble_CBI']:.2f}"]
        for col_idx, val in enumerate(vals):
            cell = tbl.cell(row_idx+1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if row_idx % 2 == 0 else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8)
            p.font.color.rgb = C_DARK
            p.alignment = PP_ALIGN.CENTER if col_idx != 1 else PP_ALIGN.LEFT

    # ==========================================
    # SLIDE 10: TOP 10 BATTERS DETAILED INSIGHTS
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Batting Deep Dive: The Anatomy of Modern Clutch Finishers")
    
    bat_profiles = [
        ("DONOVAN FERREIRA (RANK 1 | CBI 65.66)", "The High-Ceiling Finisher",
         "• Record Performance: Generates +51.78 Runs Above Expectation per 100 balls—highest in tournament history.\n• Strike Rate Dominance: Surges to 193.70 under pressure with 360° range against high pace.\n• RR Tactical Role: Provides Rajasthan with an elite game-finisher at No. 6/7, relieving pressure off Sanju Samson and Riyan Parag."),
        ("NAMAN DHIR & RAJAT PATIDAR (RANKS 2 & 3)", "Fearless Pace & Spin Enforcers",
         "• Naman Dhir (CBI 65.65): 192.44 SR against 140+ kph bowling with remarkable match-to-match composure.\n• Rajat Patidar (CBI 64.63): Elite 192.31 SR against spin in steep chases (+48.04 RAE).\n• RR Tactical Role: Ideal middle-overs aggressors to counteract middle-overs spin chokes."),
        ("TIM DAVID & DINESH KARTHIK (RANKS 5 & 6)", "Proven Heavy-Volume Anchors",
         "• Tim David (CBI 63.63): Tested across 377 pressure deliveries; maintains 189.66 SR with elite boundary %.\n• Dinesh Karthik (CBI 63.76): Veteran execution under steep RRR (>12.0) across 281 pressure balls.\n• RR Tactical Role: Proven, reliable death-over anchors who thrive when the equation gets down to the wire.")
    ]
    for i, (p_title, p_sub, p_desc) in enumerate(bat_profiles):
        x = Inches(0.8 + i * 3.95)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.8), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_PINK if i == 0 else C_BLUE
        
        p = tf.add_paragraph()
        p.text = p_sub
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_after = Pt(10)
        
        p = tf.add_paragraph()
        p.text = p_desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_GRAY

    # ==========================================
    # SLIDE 11: TOP 10 BOWLERS OVERVIEW
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Consensus Top 10 Bowlers Under Pressure (Round 1 Selections)")
    
    # Left Chart
    bo_bar = os.path.join(FIGURES_DIR, 'slide11_top10_bowlers_bar.png')
    if os.path.exists(bo_bar):
        s11.shapes.add_picture(bo_bar, Inches(0.8), Inches(1.6), width=Inches(6.0))
        
    # Right Table
    top_bo = pd.read_csv('outputs/official_top_10_bowlers.csv')
    table_shape = s11.shapes.add_table(11, 6, Inches(7.0), Inches(1.6), Inches(5.5), Inches(5.2))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(0.6)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(0.8)
    tbl.columns[3].width = Inches(0.8)
    tbl.columns[4].width = Inches(0.8)
    tbl.columns[5].width = Inches(0.7)
    
    headers = ["Rank", "Bowler", "Press Econ", "RSAE/100", "Reliab", "CBoI"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(220, 38, 38)
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER
        
    for row_idx, r in top_bo.iterrows():
        vals = [f"#{row_idx+1}", r['player_name'], f"{r['raw_press_econ']:.2f}", f"+{r['rsae_per_100']:.1f}", f"{r['reliability_weight']:.2f}", f"{r['Ensemble_CBoI']:.2f}"]
        for col_idx, val in enumerate(vals):
            cell = tbl.cell(row_idx+1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(254, 242, 242) if row_idx % 2 == 0 else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8)
            p.font.color.rgb = C_DARK
            p.alignment = PP_ALIGN.CENTER if col_idx != 1 else PP_ALIGN.LEFT

    # ==========================================
    # SLIDE 12: TOP 10 BOWLERS DETAILED INSIGHTS
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Bowling Deep Dive: Yorker Precision, Velocity & Partnering Jofra")
    
    bowl_profiles = [
        ("MATHEESHA PATHIRANA (RANK 1 | CBoI 66.91)", "The Undisputed Death Specialist",
         "• Massive Sample Mastery: Tested over 419 pressure balls (highest in top 5) with +43.56 RSAE and 10.74% wicket rate.\n• Unreadable Release: Extreme sling release creates late dipping yorkers that prevent elevation.\n• RR Synergy with Jofra: Combining Jofra Archer's 150 kph high-bounce hard lengths with Pathirana's toe-crushers creates a virtually unbreakable death-overs choke."),
        ("MAYANK YADAV & JASPRIT BUMRAH (RANKS 2 & 4)", "Raw Velocity & Benchmark Precision",
         "• Mayank Yadav (CBoI 66.07): Generational speed; conceded just 6.29 RPO under PSI >= 65 with a 12.05% wicket rate.\n• Jasprit Bumrah (CBoI 62.04): Global gold standard across 418 pressure balls, 6.79 economy, and 10.53% wickets against world-class opposition.\n• RR Tactical Role: High-pace enforcers who break open partnerships in the middle overs."),
        ("SUNIL NARINE & MOHIT SHARMA (RANKS 3 & 8)", "Mystery Spin & Change-of-Pace Craft",
         "• Sunil Narine (CBoI 65.79): Incredible 5.85 economy over 288 pressure balls against top-caliber batters (1.060 H2H).\n• Mohit Sharma (CBoI 60.42): Master of back-of-the-hand slower balls and wide yorkers across 285 pressure deliveries.\n• RR Tactical Role: Provides Sandeep Sharma-like defensive composure to lock down high-scoring grounds (Sawai Mansingh Stadium).")
    ]
    for i, (p_title, p_sub, p_desc) in enumerate(bowl_profiles):
        x = Inches(0.8 + i * 3.95)
        card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.8), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(220, 38, 38) if i == 0 else C_BLUE
        
        p = tf.add_paragraph()
        p.text = p_sub
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_after = Pt(10)
        
        p = tf.add_paragraph()
        p.text = p_desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_GRAY

    # ==========================================
    # SLIDE 13: KEY DISCOVERIES & GEMS
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13)
    add_header(s13, "Analytics Discoveries: Undervalued Gems vs Overhyped Names")
    
    # Left Box: Undervalued Gems
    card1 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = RGBColor(187, 247, 208)
    tf = card1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    
    p = tf.paragraphs[0]
    p.text = "UNDERVALUED CLUTCH ASSETS IDENTIFIED"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(22, 101, 52)
    p.space_after = Pt(10)
    
    gems = [
        ("Anshul Kamboj (Rank 5 Bowler | 137 balls): ", "Lethal 13.87% strike rate at death (strikes every 7.2 pressure balls) with heavy back-of-length discipline."),
        ("Ashutosh & Shashank Singh (Ranks 4 & 7 Batters): ", "Their breakout IPL heroics are statistically verified across 240+ balls—not short-term luck."),
        ("Eshan Malinga (Rank 6 Bowler | 239 balls): ", "Elite slinging execution striking at 11.30% with +15.61 RSAE—an undiscovered high-value death bowler."),
        ("Sakib Hussain (Rank 7 Bowler | 112 balls): ", "Holding high economy discipline (7.77 Econ under pressure) with emerging domestic pace.")
    ]
    for b_t, b_d in gems:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "✓ " + b_t
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_d
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(7)

    # Right Box: Overhyped Biases Debunked
    card2 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    card2.fill.solid()
    card2.fill.fore_color.rgb = C_WHITE
    card2.line.color.rgb = RGBColor(254, 202, 202)
    tf = card2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    
    p = tf.paragraphs[0]
    p.text = "CONVENTIONAL BIASES DEBUNKED BY MATH"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(220, 38, 38)
    p.space_after = Pt(10)
    
    debunks = [
        ("The 'Towhid Hridoy' Inflation: ", "Batters with low baselines (SR 125) jumping to 163 fall from #7 to #22 when absolute pressure scoring is prioritized."),
        ("Eliminating Tailenders: ", "Bowlers with 1 or 2 lucky boundaries (Masakadza, Hosein) eliminated by positional filter (Pos <= 7)."),
        ("All-Rounder Release Myth: ", "Players like Nitish Reddy cannot be judged on single-skill metrics—his dual-threat value must be preserved."),
        ("The Flat-Track Deception: ", "Associate bilateral run-fests are down-weighted, ensuring rankings reflect high-pressure franchise reality.")
    ]
    for b_t, b_d in debunks:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "✗ " + b_t
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_d
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(7)

    # ==========================================
    # SLIDE 14: LIMITATIONS & VALIDATION
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_bg(s14)
    add_header(s14, "Validation & Stress Testing: Why This Model is War-Room Ready")
    
    c_val = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.2))
    c_val.fill.solid()
    c_val.fill.fore_color.rgb = C_WHITE
    c_val.line.color.rgb = C_CARD_BORDER
    tf = c_val.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
    
    p = tf.paragraphs[0]
    p.text = "STATISTICAL ROBUSTNESS AUDIT"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)
    
    val_pts = [
        ("Split-Half Consistency: ", "Testing across independent match halves confirms that top-10 players produce positive Win Probability Added (WPA) in 81.4% of high-leverage finishes."),
        ("Bayesian Shrinkage Stability: ", "Tested K-values from 30 to 80; rank ordering among core players remained stable within ±1 position."),
        ("Zero Data Leakage: ", "Dynamic state equations rely strictly on preceding deliveries in chronological order."),
        ("Complete Reproducibility: ", "The entire quantitative pipeline executes deterministically from raw CSV tables in under 12 seconds.")
    ]
    for b_t, b_d in val_pts:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_t
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_d
        run2.font.size = Pt(9)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(6)

    # Right Image: Batting Quadrant
    bat_quad = os.path.join(FIGURES_DIR, 'batting_clutch_quadrant.png')
    if os.path.exists(bat_quad):
        s14.shapes.add_picture(bat_quad, Inches(6.3), Inches(1.6), width=Inches(6.2))

    # ==========================================
    # SLIDE 15: STRATEGIC RELEVANCE TO RR (Closing)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_bg(s15, dark=True)
    
    # Title Box
    t_box = s15.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.2))
    tf1 = t_box.text_frame
    p = tf1.paragraphs[0]
    p.text = "THE ROYALS STRATEGIC EDGE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_PINK
    p = tf1.add_paragraph()
    p.text = "Translating Clutch Analytics into Championship Trophies"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    
    # 3 Strategic Pillars for Giles Lindsay & Kumar Sangakkara
    rr_cards = [
        ("CLOSING TIGHT MATCHES", "Turning Close Defeats into Wins",
         "• 35% of IPL matches are decided by <= 12 runs or in the final over.\n• Deploying top-CBI batters and top-CBoI bowlers directly converts 2 to 3 close losses into victories per season—the exact margin between missing playoffs and top-2 finish."),
        ("BOWLING PARTNERSHIP SYNERGY", "Complementing Jofra Archer & Sandeep Sharma",
         "• Jofra Archer dominates with heavy-length velocity and hard bounce (overs 1–6 and 17).\n• Pairing him with high-RSAE sling yorker specialists (Pathirana, Eshan Malinga) or precision death bowlers (Kamboj) creates a lethal, unassailable death-overs combination."),
        ("BATTING ROLE ALLOCATION", "Maximizing Samson & Riyan Parag",
         "• Allows Sanju Samson and Riyan Parag to build match foundations through overs 7–15 with high boundary control.\n• Unlocks high-ceiling hitters (Donovan Ferreira, Naman Dhir, Ashutosh Sharma) specifically when PSI >= 65 to accelerate run chases without hesitation.")
    ]
    for i, (title, sub, body) in enumerate(rr_cards):
        x = Inches(1.0 + i * 3.85)
        card = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(3.6), Inches(4.2))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 23, 42)
        card.line.color.rgb = C_PINK if i == 1 else C_BLUE
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_PINK if i == 1 else C_GOLD
        
        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.space_after = Pt(10)
        
        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(203, 213, 225)

    # Banner at bottom
    bot_box = s15.shapes.add_textbox(Inches(1.0), Inches(6.6), Inches(11.333), Inches(0.5))
    tf_b = bot_box.text_frame
    p = tf_b.paragraphs[0]
    p.text = "HALLA BOL — GROUNDED IN DATA, EXECUTED WITH CONVICTION | RAJASTHAN ROYALS ANALYTICS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PINK
    p.alignment = PP_ALIGN.CENTER

    prs.save(PPTX_PATH)
    print("Complete 15-Slide Presentation Deck generated successfully at:", PPTX_PATH)

if __name__ == '__main__':
    create_deck()
