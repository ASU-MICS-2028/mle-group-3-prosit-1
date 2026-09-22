import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Colors
    c_navy = RGBColor(15, 32, 67)       # #0F2043 primary dark
    c_teal = RGBColor(0, 150, 136)      # #009688 accent teal
    c_blue = RGBColor(41, 128, 185)     # #2980B9 accent blue
    c_red = RGBColor(192, 57, 43)       # #C0392B alert red
    c_card_bg = RGBColor(245, 247, 250) # #F5F7FA light card
    c_border = RGBColor(220, 224, 230)
    c_white = RGBColor(255, 255, 255)
    c_dark = RGBColor(33, 33, 33)
    c_gray = RGBColor(100, 110, 120)

    def add_header(slide, title_text, category_text=""):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.9))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        if category_text:
            p0.text = category_text.upper()
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = c_teal
            p1 = tf.add_paragraph()
        else:
            p1 = p0
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = c_navy

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "DATA-DRIVEN RESOURCE ALLOCATION OF ITNs IN GHANA"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = c_white

    p2 = tf1.add_paragraph()
    p2.text = "An Uncertainty-Aware Decision Framework for Allocating 50,000 Nets Across 50 Northern Districts"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(178, 223, 219)
    p2.space_before = Pt(15)

    p3 = tf1.add_paragraph()
    p3.text = "Advisory Presentation to the National Malaria Elimination Programme (NMEP), Ghana Health Service\nICS553 Machine Learning Essentials · Group 3 · Ashesi University"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(200, 215, 230)
    p3.space_before = Pt(40)

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement & Decision Framing
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Decision Context: Allocating 50,000 Indivisible Nets", "Executive Summary")
    
    # Left Card: Operational Parameters
    card1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3))
    card1.fill.solid()
    card1.fill.fore_color.rgb = c_card_bg
    card1.line.color.rgb = c_border
    
    tb_c1 = s2.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(5.0), Inches(4.8))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "Operational Parameters & Constraints"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy
    
    bullets1 = [
        ("Resource Ceiling:", " Exactly 50,000 long-lasting ITNs available for northern Ghana."),
        ("Target Unit:", " 50 administrative districts across Northern, Upper East, and Upper West regions."),
        ("Indivisibility:", " Integer allocations required (no fractional nets; Hamilton apportionment)."),
        ("Asymmetric Loss:", " Under-allocating to an epidemic zone costs human lives; over-allocating only incurs marginal warehousing costs.")
    ]
    for b_title, b_desc in bullets1:
        p = tf_c1.add_paragraph()
        p.space_before = Pt(12)
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = c_navy
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = c_dark

    # Right Card: The Naive Allocation Traps
    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.3))
    card2.fill.solid()
    card2.fill.fore_color.rgb = c_card_bg
    card2.line.color.rgb = c_border
    
    tb_c2 = s2.shapes.add_textbox(Inches(7.2), Inches(1.7), Inches(5.0), Inches(4.8))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "Why The Naive Heuristic Fails Catastrophically"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_red

    bullets2 = [
        ("The Clinic Access Bias:", " Raw cases measure clinic attendance, not infection. Rural areas with no clinics report 0 cases!"),
        ("The Referral Hospital Trap:", " Regional hospitals (Bolgatanga, Wa) log thousands of cases from patients travelling from outside districts."),
        ("Satiation & Existing Coverage:", " Upper East already has 79.6% net coverage. Dumping nets there gives zero marginal benefit."),
        ("Ignoring Over-dispersion:", " High localized spikes are treated as ordinary noise, leaving high-risk zones under-protected.")
    ]
    for b_title, b_desc in bullets2:
        p = tf_c2.add_paragraph()
        p.space_before = Pt(12)
        run1 = p.add_run()
        run1.text = "⚠ " + b_title
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = c_red
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = c_dark

    # -------------------------------------------------------------
    # SLIDE 3: Map Highlights: National Data Availability & Division
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Geospatial Surveillance & Survey Data Divide", "Theme B1 Geospatial EDA")
    
    # Left Map: Cluster Availability
    p_map1 = Path("figures/b1_data_availability.png")
    if p_map1.exists():
        s3.shapes.add_picture(str(p_map1), Inches(0.8), Inches(1.5), width=Inches(4.4))
    
    # Right Map: District Surveillance Case Rate
    p_map2 = Path("figures/b1_district_case_rate.png")
    if p_map2.exists():
        s3.shapes.add_picture(str(p_map2), Inches(5.5), Inches(1.5), width=Inches(4.4))

    # Right Card: Insights
    card3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.1), Inches(1.5), Inches(2.5), Inches(5.4))
    card3.fill.solid()
    card3.fill.fore_color.rgb = c_card_bg
    card3.line.color.rgb = c_border
    
    tb_c3 = s3.shapes.add_textbox(Inches(10.2), Inches(1.7), Inches(2.3), Inches(5.0))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "Key Cartographic Findings"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_navy
    
    insights = [
        "1. Severe Surveillance Divide: 50 northern districts have DHIMS-2 records; 210 southern districts have zero routine data.",
        "2. Survey Density: DHS 2022 sampled 618 clusters nationwide, but Northern Region rural clusters carry wide sampling errors.",
        "3. Survey Weighting Effect: Unweighted net ownership (70.96%) overstates true weighted ownership (66.77%) by 4.19 percentage points."
    ]
    for ins in insights:
        p = tf_c3.add_paragraph()
        p.space_before = Pt(10)
        p.text = ins
        p.font.size = Pt(10)
        p.font.color.rgb = c_dark

    # -------------------------------------------------------------
    # SLIDE 4: Theme A: Why Poisson Failed (Over-dispersion)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Over-Dispersion: Why Poisson Regression Crashed", "Theme A Statistical Modeling")

    # Left: Explanation Card
    card4 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.3))
    card4.fill.solid()
    card4.fill.fore_color.rgb = c_card_bg
    card4.line.color.rgb = c_border
    
    tb_c4 = s4.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.1), Inches(4.8))
    tf_c4 = tb_c4.text_frame
    tf_c4.word_wrap = True
    p = tf_c4.paragraphs[0]
    p.text = "The Mathematical Breakdown"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    points4 = [
        ("The Poisson Assumption:", " Assumes Variance = Mean. Expected variance/mean ratio is strictly 1.0."),
        ("Observed Reality:", " In northern Ghana, Variance / Mean = 77,183! Observed SD is 122,882 vs Poisson SD of 442 (278x narrower)."),
        ("Survives Population Offset:", " Pearson chi2/df = 54,147. Poisson fails catastrophically even after adjusting for district population."),
        ("Negative Binomial (NB2):", " Adds dispersion knob (alpha = 0.2677), allowing Var = mu + alpha*mu^2. Outperforms Poisson by 2,393,669 AIC points!")
    ]
    for t, d in points4:
        p = tf_c4.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = t
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = c_navy
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = c_dark

    # Right: Embedded Figure a3
    p_fig_a3 = Path("figures/a3_poisson_vs_nb.png")
    if p_fig_a3.exists():
        s4.shapes.add_picture(str(p_fig_a3), Inches(6.6), Inches(1.5), width=Inches(5.9))

    # -------------------------------------------------------------
    # SLIDE 5: Theme A: Survey Uncertainty & Two-Stage Cluster Bootstrap
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Honest Uncertainty: The Two-Stage Cluster Bootstrap", "Theme A Sampling Theory")

    # Left: Explanation
    card5 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.3))
    card5.fill.solid()
    card5.fill.fore_color.rgb = c_card_bg
    card5.line.color.rgb = c_border
    
    tb_c5 = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.1), Inches(4.8))
    tf_c5 = tb_c5.text_frame
    tf_c5.word_wrap = True
    p = tf_c5.paragraphs[0]
    p.text = "Cluster Autocorrelation vs. Naive Sampling"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    points5 = [
        ("The DHS Sampling Design:", " 2-stage cluster sampling: clusters (villages) chosen first, then 25-30 households per cluster."),
        ("Intra-Cluster Correlation:", " Families in the same village share the same swamp and risk. They are NOT independent."),
        ("The Naive Bootstrap Danger:", " Resampling households ignores village clustering, giving a confidence interval of 7.17 pp (false precision!)."),
        ("The Honest Cluster Bootstrap:", " Resampling clusters first yields a 15.20 pp interval — 2.12x wider (DEFF = 4.50)!"),
        ("Validation Benchmark:", " Survey-weighted net ownership reproduces published 2022 DHS report to 0.09 pp (67.69% vs 67.60%).")
    ]
    for t, d in points5:
        p = tf_c5.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = t
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = c_navy
        r2 = p.add_run()
        r2.text = d
        r2.font.size = Pt(11)
        r2.font.color.rgb = c_dark

    # Right: Embedded Figure a4
    p_fig_a4 = Path("figures/a4_bootstrap_ci_comparison.png")
    if p_fig_a4.exists():
        s5.shapes.add_picture(str(p_fig_a4), Inches(6.6), Inches(2.0), width=Inches(5.9))

    # -------------------------------------------------------------
    # SLIDE 6: Theme B: Pipeline Rigour & The Leakage Audit
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Pipeline Discipline & Leakage Audit", "Theme B Pipeline Engineering")

    # 3 Summary Boxes across width
    box_w = Inches(3.7)
    box_h = Inches(5.1)
    
    # Leak 1
    b1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), box_w, box_h)
    b1.fill.solid()
    b1.fill.fore_color.rgb = c_card_bg
    b1.line.color.rgb = c_border
    tb_b1 = s6.shapes.add_textbox(Inches(0.9), Inches(1.8), Inches(3.5), Inches(4.7))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True
    p = tf_b1.paragraphs[0]
    p.text = "1. Preprocessing Leak"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy
    t1 = tf_b1.add_paragraph()
    t1.space_before = Pt(10)
    t1.text = "• Scaling/imputing before split leaks test distribution into training.\n• Deflates test RMSE by 212 cases (87,144 vs honest 87,356).\n• Prevention: Strict Pipeline and ColumnTransformer encapsulation."
    t1.font.size = Pt(11)

    # Leak 2
    b2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.6), box_w, box_h)
    b2.fill.solid()
    b2.fill.fore_color.rgb = c_card_bg
    b2.line.color.rgb = c_border
    tb_b2 = s6.shapes.add_textbox(Inches(4.9), Inches(1.8), Inches(3.5), Inches(4.7))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True
    p = tf_b2.paragraphs[0]
    p.text = "2. Target Encoding Catastrophe"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_red
    t2 = tf_b2.add_paragraph()
    t2.space_before = Pt(10)
    t2.text = "• Encoding district by target mean without out-of-fold regularization.\n• Model memorizes training targets, faking R² = 1.0000 (honest 0.4905).\n• Prevention: Target encoding rejected entirely."
    t2.font.size = Pt(11)

    # Leak 3
    b3 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.6), box_w, box_h)
    b3.fill.solid()
    b3.fill.fore_color.rgb = c_card_bg
    b3.line.color.rgb = c_border
    tb_b3 = s6.shapes.add_textbox(Inches(8.9), Inches(1.8), Inches(3.5), Inches(4.7))
    tf_b3 = tb_b3.text_frame
    tf_b3.word_wrap = True
    p = tf_b3.paragraphs[0]
    p.text = "3. Spatial Autocorrelation"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy
    t3 = tf_b3.add_paragraph()
    t3.space_before = Pt(10)
    t3.text = "• Random 80/20 train/test splits place neighboring districts on both sides.\n• Model 'peeks' at geographic twin; test error drops by 45.5% (47,646 vs 87,356).\n• Prevention: Region-stratified holdout split."
    t3.font.size = Pt(11)

    # -------------------------------------------------------------
    # SLIDE 7: Theme C: The Proposed Equitable Allocation Formula
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "The Equitable Need-Weighted Allocation Policy", "Theme C Resource Optimization")

    tb7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.text = "Three Pillars of the Proposed Allocation Model"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = c_navy

    items7 = [
        ("1. Upper-Bound Epidemic Risk (mu_upper):", " We extract the upper bound of the 95% prediction interval from the Negative Binomial model. This implements an asymmetric minimax hedge, ensuring districts are protected against worst-case epidemic spikes."),
        ("2. The Unmet Coverage Gap (1 - Coverage):", " Bed nets produce herd immunity. Districts with ~80% coverage experience diminishing marginal returns. Weighting by (1 - coverage/100) directs nets where baseline household ownership is lowest."),
        ("3. Hamilton Integer Apportionment:", " Guarantees that exactly 50,000 integer nets are allocated (no fractional nets, no budget drops) by awarding floor quotas and distributing remainders to largest fractional deficits.")
    ]
    for h, b in items7:
        p = tf7.add_paragraph()
        p.space_before = Pt(14)
        r1 = p.add_run()
        r1.text = h + "\n"
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = c_teal
        r2 = p.add_run()
        r2.text = b
        r2.font.size = Pt(12)
        r2.font.color.rgb = c_dark

    # Formula Box
    fbox = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.1))
    fbox.fill.solid()
    fbox.fill.fore_color.rgb = c_navy
    tf_fb = fbox.text_frame
    tf_fb.word_wrap = True
    p_fb = tf_fb.paragraphs[0]
    p_fb.text = "Weight_i = mu_upper_i  x  (1 - net_coverage_pct_i / 100)        =>        Allocation_i = Hamilton(Weight_i, Total = 50,000)"
    p_fb.font.size = Pt(15)
    p_fb.font.bold = True
    p_fb.font.color.rgb = c_white
    p_fb.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 8: Map Highlight: Equitable Allocation Map
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Map Highlight: 50,000 Net Distribution Across Northern Ghana", "Theme C Geospatial Allocation")

    p_map_alloc = Path("figures/c2_allocation_map.png")
    if p_map_alloc.exists():
        s8.shapes.add_picture(str(p_map_alloc), Inches(0.8), Inches(1.5), width=Inches(5.0))

    # Right Card: Regional Allocation Summary
    card8 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.2), Inches(1.5), Inches(6.3), Inches(5.3))
    card8.fill.solid()
    card8.fill.fore_color.rgb = c_card_bg
    card8.line.color.rgb = c_border
    
    tb_c8 = s8.shapes.add_textbox(Inches(6.4), Inches(1.7), Inches(5.9), Inches(4.9))
    tf_c8 = tb_c8.text_frame
    tf_c8.word_wrap = True
    p = tf_c8.paragraphs[0]
    p.text = "Regional Consignment Shares"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    reg_allocs = [
        ("Northern Region Depot (Tamale):", " 24,980 nets (49.96%) across 26 districts.\nReflects lower baseline net coverage (67.7%) and largest population at risk."),
        ("Upper East Depot (Bolgatanga):", " 17,547 nets (35.09%) across 13 districts.\nHigh historical caseload, but high baseline coverage (79.6%) dampens allocation."),
        ("Upper West Depot (Wa):", " 7,473 nets (14.95%) across 11 districts.\nCorrected for hospital referral inflation; nets distributed to rural catchments.")
    ]
    for rh, rd in reg_allocs:
        p = tf_c8.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = rh + "\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = c_navy
        r2 = p.add_run()
        r2.text = rd
        r2.font.size = Pt(11)
        r2.font.color.rgb = c_dark

    # -------------------------------------------------------------
    # SLIDE 9: Map Highlight: Policy Shift (Gainers vs. Losers)
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Map Highlight: Net Shifts (Equitable vs. Naive)", "Theme C Policy Impact")

    p_map_shift = Path("figures/c3_policy_shift_map.png")
    if p_map_shift.exists():
        s9.shapes.add_picture(str(p_map_shift), Inches(0.8), Inches(1.5), width=Inches(6.0))

    p_fig_bar = Path("figures/c1_allocation_comparison.png")
    if p_fig_bar.exists():
        s9.shapes.add_picture(str(p_fig_bar), Inches(7.1), Inches(1.5), width=Inches(5.4))

    # -------------------------------------------------------------
    # SLIDE 10: Deep Dive: The Referral Hospital Trap
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Deep Dive: The Referral Hospital Trap Explained", "Theme C Policy Defense")

    # Card 1: Bolga & Wa
    c10_1 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3))
    c10_1.fill.solid()
    c10_1.fill.fore_color.rgb = c_card_bg
    c10_1.line.color.rgb = c_border
    tb_10_1 = s10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.9))
    tf_10_1 = tb_10_1.text_frame
    tf_10_1.word_wrap = True
    p = tf_10_1.paragraphs[0]
    p.text = "Why Wa (-1,516) & Bolgatanga (-665) Lose Nets"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_red
    
    b_loss = [
        "1. Hospital Catchment Distortion: Wa and Bolgatanga host the two regional referral hospitals. Cases are logged at the clinic address, not patient residence!",
        "2. Saturated Baseline Ownership: Upper East has 79.6% net coverage; Upper West has 69.8%. Bolga already has nets in almost every home.",
        "3. Eliminating Waste: Naive allocation gives Bolga 3,015 nets and Wa 2,610 nets. Our model scales them down to honest local community levels."
    ]
    for b in b_loss:
        p = tf_10_1.add_paragraph()
        p.space_before = Pt(12)
        p.text = b
        p.font.size = Pt(11)
        p.font.color.rgb = c_dark

    # Card 2: Tamale & Sagnarigu
    c10_2 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.3))
    c10_2.fill.solid()
    c10_2.fill.fore_color.rgb = c_card_bg
    c10_2.line.color.rgb = c_border
    tb_10_2 = s10.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(4.9))
    tf_10_2 = tb_10_2.text_frame
    tf_10_2.word_wrap = True
    p = tf_10_2.paragraphs[0]
    p.text = "Why Tamale (+1,692) & Sagnarigu (+1,012) Gain Nets"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_teal

    b_gain = [
        "1. Massive Population at Risk: Tamale has ~255,000 residents; Sagnarigu has ~168,000 residents (the largest urban agglomeration in the north).",
        "2. Critical Unmet Need Gap: Northern Region has only 67.7% baseline coverage. The absolute number of unprotected people is highest here.",
        "3. Correcting Naive Under-allocation: Naive policy awarded Tamale only 483 nets (0.97% of supply)! Equitable allocation restores 2,175 nets."
    ]
    for b in b_gain:
        p = tf_10_2.add_paragraph()
        p.space_before = Pt(12)
        p.text = b
        p.font.size = Pt(11)
        p.font.color.rgb = c_dark

    # -------------------------------------------------------------
    # SLIDE 11: NMEP Implementation Roadmap
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Implementation Roadmap for NMEP Rollout", "Theme D Operational Strategy")

    tb11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    tf11 = tb11.text_frame
    tf11.word_wrap = True

    steps = [
        ("Phase 1: Regional Warehousing & Staging (Weeks 1-2)", "Consignments dispatched to Tamale (24,980), Bolgatanga (17,547), and Wa (7,473) central medical stores."),
        ("Phase 2: Last-Mile Delivery via CHPS Compounds (Weeks 3-4)", "Bypassing regional hospital gates to distribute directly through Community-Based Health Planning and Services (CHPS), prioritizing pregnant women and children under 5."),
        ("Phase 3: Digital Tracking & Traceability (Weeks 4-6)", "Barcode scanning of bale deliveries at district health directorates to eliminate supply leakage and diversion."),
        ("Phase 4: 6-Month Post-Distribution Audit (Month 6)", "Conduct rapid two-stage cluster surveys in recipient communities to evaluate net hanging rates, physical integrity, and local parasitaemia decline.")
    ]
    p = tf11.paragraphs[0]
    p.text = "Four-Phase Rollout Schedule"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = c_navy

    for sh, sd in steps:
        p = tf11.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = sh + "\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = c_teal
        r2 = p.add_run()
        r2.text = sd
        r2.font.size = Pt(11)
        r2.font.color.rgb = c_dark

    # -------------------------------------------------------------
    # SLIDE 12: Viva Exam Defense FAQ Cheat Sheet
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Viva Oral Defense: Examiner Grill-Me Cheat Sheet", "Academic Defense Bank")

    tb12 = s12.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    faqs = [
        ("Examiner: 'Why not use Poisson regression?'",
         "Answer: In northern Ghana, Variance/Mean is 77,183. Poisson assumes 1.0, underestimating outbreak spread by 278x. Negative Binomial (alpha = 0.2677) accommodates this heavy tail and beats Poisson by 2.39M AIC."),
        ("Examiner: 'Why did naive bootstrap fail?'",
         "Answer: DHS data is clustered by village. Naive bootstrap pretends households are independent, shrinking the CI to 7.17 pp. Two-stage cluster bootstrap gives an honest 15.20 pp interval (DEFF = 4.50)."),
        ("Examiner: 'Why cut nets from Bolgatanga when it has the highest case count?'",
         "Answer: Bolgatanga Regional Hospital logs cases from surrounding rural districts. Furthermore, Upper East already has 79.6% net coverage. Handing thousands more nets to Bolga causes waste; our model targets true community unmet need."),
        ("Examiner: 'What if your budget is cut by 50% to 25,000 nets?'",
         "Answer: The priority ranking is invariant. Because Hamilton apportionment scales linearly with relative need weights, the district priority hierarchy remains identical.")
    ]
    p = tf12.paragraphs[0]
    p.text = "High-Stakes Panel Q&A Scripts"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy

    for q, a in faqs:
        p = tf12.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = q + "  "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = c_navy
        r2 = p.add_run()
        r2.text = a
        r2.font.size = Pt(10)
        r2.font.color.rgb = c_dark

    # Save
    out_dir = Path("reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ITN_Allocation_Presentation.pptx"
    prs.save(str(out_path))
    print(f"Presentation deck successfully created at: {out_path}")

if __name__ == "__main__":
    create_deck()
