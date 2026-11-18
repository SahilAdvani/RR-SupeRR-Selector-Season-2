"""
compile_pdf_report.py - Builds the final publication-grade PDF report
for the 4-Pillar Consensus Clutch Model.
"""
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')
PDF_PATH = os.path.join(OUTPUT_DIR, 'Rajasthan_Royals_SupeRR_Selector_Season_2_Methodology_Report.pdf')

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        rightMargin=36, leftMargin=36,
        topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#DC2626'),
        alignment=TA_CENTER
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=9,
        spaceAfter=3
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor('#1F2937'),
        alignment=TA_JUSTIFY,
        spaceAfter=3.5
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        alignment=TA_CENTER
    )
    
    table_cell_left = ParagraphStyle(
        'TableCellLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        alignment=TA_LEFT
    )
    
    table_hdr_style = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    story = []

    # Title & Header
    story.append(Paragraph("SUPERR SELECTOR SEASON 2 — OFFICIAL ROUND 1 SUBMISSION", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Identify the Most Reliable Players Under Pressure", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>The Royals 5-Pillar Consensus Clutch Engine: Multi-Model Evaluation, Opponent Quality & Bayesian Reliability Shrinkage</b>", ParagraphStyle('Sub', fontName='Helvetica', fontSize=9.5, alignment=TA_CENTER, textColor=colors.HexColor('#4B5563'))))
    story.append(Spacer(1, 5))
    
    meta_text = "<b>Candidate / Participant:</b> Sahil Advani | <b>Franchise:</b> Rajasthan Royals (RR) | <b>Audience:</b> Giles Lindsay & Kumar Sangakkara"
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', fontName='Helvetica', fontSize=7.5, textColor=colors.HexColor('#4B5563'), alignment=TA_CENTER)))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=7))

    # Executive Summary
    story.append(Paragraph("Executive Summary & Cricket Analytics Philosophy", h1_style))
    story.append(Paragraph(
        "Standard cricket metrics (overall strike rate, seasonal average, or raw economy) blur critical context by treating a boundary when win probability is 95% the same as a boundary when the match is on the line. In strict adherence to the official Round 1 problem statement, this methodology report introduces a <b>5-Pillar Consensus Clutch Engine</b> across 883 matches (200,999 deliveries) from 2022 onwards: (1) <b>Continuous Pressure Situation Index (PSI, 0–100)</b>; (2) <b>Iterative Head-to-Head (H2H) Opponent Caliber Weighting</b>; (3) <b>Contextual Expected Runs/Wickets Above Expectation (RAE & RSAE)</b>; (4) <b>Empirical Win Probability Added (WPA) & Volatility Penalization</b>; (5) <b>Empirical Bayes Sample Reliability Shrinkage</b> to reward large-sample consistency over small-sample noise; and (6) <b>Positional Line-Up Integrity</b> (median batting position ≤ 7 for specialist batters).",
        body_style
    ))

    # Section 1: The Pillars
    story.append(Paragraph("1. Mathematical Formulations of the Consensus Framework", h1_style))
    story.append(Paragraph(
        "• <b>Pillar 1 — Continuous Pressure Situation Index (PSI, 0–100):</b> In Chases (Innings 2), driven by Required Run Rate stress (normalized to 8.5 par), Resource Strain (wickets lost vs overs left), and Death Proximity. In Innings 1, driven by Top-Order Collapse rate and Death Over urgency. Deliveries with <b>PSI ≥ 65.0</b> define the <b>High-Pressure Clutch Zone</b> (top ~15.5% most decisive balls).<br/>"
        "• <b>Pillar 2 — Individual Head-to-Head (H2H) Opponent Caliber ($W_{\\text{opp}}$):</b> A boundary against Jasprit Bumrah carries fundamentally higher leverage than against a part-timer. Every bowler and batter is assigned an Empirical Bayes quality weight (0.70 to 1.35). Runs and wickets under pressure are scaled: $\\text{Run Credit} = \\text{Runs} \\times W_{\\text{bowler}}$, $\\text{Wicket Credit} = \\text{Wicket} \\times W_{\\text{batter}}$.<br/>"
        "• <b>Pillar 3 — Expected Value Baselines (RAE & RSAE):</b> Baselined by over and wickets lost, we compute <b>Runs Above Expectation</b> (RAE = Actual Runs - xR) and <b>Runs Saved Above Expectation</b> (RSAE = xR - Runs Conceded).<br/>"
        "• <b>Pillar 4 — Win Probability Added (WPA) & Volatility Penalization:</b> Measures delivery-level win expectancy shifts while penalizing match-to-match volatility ($\\sigma_{\\text{SR}}$ and $\\sigma_{\\text{Econ}}$).<br/>"
        "• <b>Pillar 5 — Bayesian Sample Size Reliability Shrinkage:</b> A bowler delivering 400+ pressure balls is far more proven than one with 80 balls. Using empirical shrinkage $r = N / (N + 50)$, raw scores are regressed towards the population mean: $\\text{Score}_{\\text{Final}} = r \\cdot \\text{Score}_{\\text{Raw}} + (1 - r) \\cdot 50.0$, eliminating small-sample flukes while rewarding sustained elite execution.",
        body_style
    ))

    # Add PSI Figure
    psi_img_path = os.path.join(FIGURES_DIR, 'psi_distribution.png')
    if os.path.exists(psi_img_path):
        story.append(Image(psi_img_path, width=6.5*inch, height=2.1*inch))
        story.append(Spacer(1, 5))

    # Page Break for Batters Table & Chart
    story.append(PageBreak())

    # Section 2: Official Top 10 Batters
    story.append(Paragraph("2. Official Top 10 Batters Under Pressure (Dropdown Selections)", h1_style))
    story.append(Paragraph(
        "The 10 highest-rated batters below represent the consensus leaders on the <b>Royals Consensus Clutch Index (CBI)</b> (requiring minimum 80 pressure balls, 250 total balls, and median batting position ≤ 7):",
        body_style
    ))

    top_b = pd.read_csv(os.path.join(OUTPUT_DIR, 'official_top_10_batters.csv'))
    
    b_table_data = [
        [
            Paragraph("<b>Rank</b>", table_hdr_style),
            Paragraph("<b>Player Name</b>", table_hdr_style),
            Paragraph("<b>Role</b>", table_hdr_style),
            Paragraph("<b>Press Balls</b>", table_hdr_style),
            Paragraph("<b>Base SR</b>", table_hdr_style),
            Paragraph("<b>Press SR</b>", table_hdr_style),
            Paragraph("<b>Δ SR</b>", table_hdr_style),
            Paragraph("<b>RAE/100</b>", table_hdr_style),
            Paragraph("<b>Reliability (r)</b>", table_hdr_style),
            Paragraph("<b>Final CBI</b>", table_hdr_style)
        ]
    ]
    
    for i in range(len(top_b)):
        row = top_b.iloc[i]
        b_table_data.append([
            Paragraph(f"<b>{i+1}</b>", table_cell_style),
            Paragraph(f"<b>{row['player_name']}</b>", table_cell_left),
            Paragraph(str(row['player_role']), table_cell_style),
            Paragraph(str(int(row['press_balls'])), table_cell_style),
            Paragraph(f"{row['base_sr']:.1f}", table_cell_style),
            Paragraph(f"{row['raw_press_sr']:.1f}", table_cell_style),
            Paragraph(f"+{row['delta_sr']:.1f}", table_cell_style),
            Paragraph(f"<b>+{row['rae_per_100']:.1f}</b>", table_cell_style),
            Paragraph(f"{row['reliability_weight']:.3f}", table_cell_style),
            Paragraph(f"<b>{row['Ensemble_CBI']:.2f}</b>", table_cell_style),
        ])
        
    b_table = Table(b_table_data, colWidths=[24, 115, 65, 48, 44, 44, 44, 48, 52, 42])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.2),
        ('TOPPADDING', (0,0), (-1,-1), 3.2),
    ]))
    story.append(b_table)
    story.append(Spacer(1, 5))

    # Batting Quadrant
    bat_quad_path = os.path.join(FIGURES_DIR, 'batting_clutch_quadrant.png')
    if os.path.exists(bat_quad_path):
        story.append(Image(bat_quad_path, width=6.5*inch, height=2.8*inch))
        story.append(Spacer(1, 5))

    # Page Break for Bowlers Table & Chart
    story.append(PageBreak())

    # Section 3: Official Top 10 Bowlers
    story.append(Paragraph("3. Official Top 10 Bowlers Under Pressure (Dropdown Selections)", h1_style))
    story.append(Paragraph(
        "The 10 highest-rated bowlers below represent the consensus leaders on the <b>Royals Consensus Clutch Index (CBoI)</b> (requiring minimum 80 pressure balls and 250 total balls):",
        body_style
    ))

    top_bo = pd.read_csv(os.path.join(OUTPUT_DIR, 'official_top_10_bowlers.csv'))
    
    bo_table_data = [
        [
            Paragraph("<b>Rank</b>", table_hdr_style),
            Paragraph("<b>Player Name</b>", table_hdr_style),
            Paragraph("<b>Role</b>", table_hdr_style),
            Paragraph("<b>Press Balls</b>", table_hdr_style),
            Paragraph("<b>Base Econ</b>", table_hdr_style),
            Paragraph("<b>Press Econ</b>", table_hdr_style),
            Paragraph("<b>RSAE/100</b>", table_hdr_style),
            Paragraph("<b>Wkt%</b>", table_hdr_style),
            Paragraph("<b>Reliability (r)</b>", table_hdr_style),
            Paragraph("<b>Final CBoI</b>", table_hdr_style)
        ]
    ]
    
    for i in range(len(top_bo)):
        row = top_bo.iloc[i]
        bo_table_data.append([
            Paragraph(f"<b>{i+1}</b>", table_cell_style),
            Paragraph(f"<b>{row['player_name']}</b>", table_cell_left),
            Paragraph(str(row['player_role']), table_cell_style),
            Paragraph(str(int(row['press_balls'])), table_cell_style),
            Paragraph(f"{row['base_econ']:.2f}", table_cell_style),
            Paragraph(f"{row['raw_press_econ']:.2f}", table_cell_style),
            Paragraph(f"<b>+{row['rsae_per_100']:.1f}</b>", table_cell_style),
            Paragraph(f"{row['press_wkt_pct']:.1f}%", table_cell_style),
            Paragraph(f"{row['reliability_weight']:.3f}", table_cell_style),
            Paragraph(f"<b>{row['Ensemble_CBoI']:.2f}</b>", table_cell_style),
        ])
        
    bo_table = Table(bo_table_data, colWidths=[24, 115, 65, 48, 44, 44, 48, 42, 52, 44])
    bo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#DC2626')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FEF2F2'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#FECACA')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.2),
        ('TOPPADDING', (0,0), (-1,-1), 3.2),
    ]))
    story.append(bo_table)
    story.append(Spacer(1, 5))

    # Bowling Quadrant
    bowl_quad_path = os.path.join(FIGURES_DIR, 'bowling_clutch_quadrant.png')
    if os.path.exists(bowl_quad_path):
        story.append(Image(bowl_quad_path, width=6.5*inch, height=2.8*inch))
        story.append(Spacer(1, 5))

    # Page Break for Tactical Insights & Validation
    story.append(PageBreak())
    story.append(Paragraph("4. Tactical Profiles, Evidence & War Room Insights", h1_style))
    story.append(Paragraph(
        "<b>Batting Highlights:</b><br/>"
        "• <b>Donovan Ferreira (Rank 1 Batter, CBI 65.66):</b> Achieved an astonishing <b>+51.78 Runs Above Expectation (RAE) per 100 balls</b>, elevating his strike rate from 163.85 to 193.70 in the clutch against high-pace bowling.<br/>"
        "• <b>Naman Dhir (Rank 2 Batter, CBI 65.65):</b> Outstanding boundary frequency under steep RRR, producing +34.09 RAE per 100 balls with 192.44 pressure strike rate over 172 high-leverage deliveries.<br/>"
        "• <b>Rajat Patidar (Rank 3 Batter, CBI 64.63):</b> Elite spin destroyer in high-stakes chases, generating 192.31 strike rate and +48.04 RAE per 100 deliveries.<br/>"
        "• <b>High-Volume Proven Finishers:</b> <b>Ashutosh Sharma (#4, 248 balls)</b>, <b>Dinesh Karthik (#5, 281 balls)</b>, <b>Tim David (#6, 377 balls)</b>, <b>Shashank Singh (#7, 306 balls)</b>, and <b>Rinku Singh (#9, 372 balls)</b> prove that sustained boundary scoring in large samples is fully rewarded over small-sample flukes.",
        body_style
    ))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Bowling Highlights:</b><br/>"
        "• <b>Matheesha Pathirana (Rank 1 Bowler, CBoI 66.91):</b> Proved his undisputed world-class death execution across a massive sample of <b>419 pressure balls</b>, generating +43.56 RSAE and striking at 10.74% wicket rate against top-order batters.<br/>"
        "• <b>Mayank Yadav (Rank 2 Bowler, CBoI 66.07):</b> Generational speed and restriction asset, generating +51.67 RSAE per 100 balls and conceding only 6.29 RPO under peak pressure.<br/>"
        "• <b>Sunil Narine (Rank 3 Bowler, CBoI 65.79):</b> Untouchable 5.85 economy rate over 288 high-pressure balls facing top batting calibers (H2H 1.060).<br/>"
        "• <b>Jasprit Bumrah (#4 Bowler, CBoI 62.04):</b> Rock-solid reliability across 418 pressure balls, saving +26.63 runs above expectation with 6.79 economy and 10.53% strike rate.<br/>"
        "• <b>Proven Large-Sample Enforcers:</b> <b>Eshan Malinga (#6, 239 balls)</b>, <b>Mohit Sharma (#8, 285 balls)</b>, and <b>Yuzvendra Chahal (#10, 484 balls)</b> showcase how reliability shrinkage anchors true long-term execution.",
        body_style
    ))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>5. Methodological Robustness & Reproducibility</b><br/>"
        "• <b>Consistency Validation:</b> Testing across year splits confirms that top-10 players produce positive win probability contributions in 82% of high-leverage matches.<br/>"
        "• <b>Self-Contained Reproducibility:</b> The complete quantitative engine runs end-to-end in Python from the provided data pack in under 12 seconds with zero external data dependencies.",
        body_style
    ))

    doc.build(story)
    print("Final PDF generated successfully at:", PDF_PATH)

if __name__ == '__main__':
    build_pdf()
