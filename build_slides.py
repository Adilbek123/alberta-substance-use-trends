"""Build a 4-slide deck summarising the analysis."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides.pptx")
CHART = os.path.join(HERE, "output", "rdit_opioid_deaths.png")

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

DARK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x55, 0x55, 0x55)
LIGHT = RGBColor(0x88, 0x88, 0x88)
BLUE = RGBColor(0x1F, 0x6F, 0xB4)
RED = RGBColor(0xC0, 0x39, 0x2B)
BG = RGBColor(0xFF, 0xFF, 0xFF)


def add_text(slide, left, top, width, height, text, size=14, bold=False, color=DARK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Helvetica Neue"
    return tf


def add_para(tf, text, size=14, bold=False, color=DARK):
    p = tf.add_paragraph()
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Helvetica Neue"
    return p


def add_footer(slide, n_total, n):
    add_text(slide, 0.4, 7.1, 4, 0.3,
             "Alberta opioid mortality and COVID-19  |  personal learning project",
             size=9, color=LIGHT)
    add_text(slide, 12.7, 7.1, 0.5, 0.3, f"{n} / {n_total}", size=9, color=LIGHT, align=PP_ALIGN.RIGHT)


blank = prs.slide_layouts[6]

# ===========================================================================
# Slide 1 — Title
# ===========================================================================
s = prs.slides.add_slide(blank)
add_text(s, 0.8, 2.2, 12, 1.2,
         "Alberta opioid deaths around COVID-19",
         size=40, bold=True, color=DARK)
add_text(s, 0.8, 3.4, 12, 0.7,
         "An interrupted time series with placebo and NB cross-checks",
         size=20, color=GREY)
add_text(s, 0.8, 4.6, 12, 0.5,
         "Adilbek Sultanov  ·  personal learning project  ·  May 2026",
         size=14, color=GREY)
add_text(s, 0.8, 5.3, 12, 0.5,
         "github.com/Adilbek123/alberta-substance-use-trends",
         size=12, color=BLUE)
add_footer(s, 4, 1)

# ===========================================================================
# Slide 2 — Question + method
# ===========================================================================
s = prs.slides.add_slide(blank)
add_text(s, 0.6, 0.4, 12, 0.6,
         "What I asked, and how I tried to answer it",
         size=26, bold=True, color=DARK)

tf = add_text(s, 0.6, 1.4, 12, 0.4, "Question", size=15, bold=True, color=BLUE)
add_para(tf, "Did Alberta's opioid death rate shift at a level higher than the pre-COVID trend can explain, "
              "starting from 2020 Q2 (first full quarter under the public health emergency)?",
         size=14, color=DARK)

tf = add_text(s, 0.6, 3.0, 12, 0.4, "Data", size=15, bold=True, color=BLUE)
add_para(tf, "PHAC Health Infobase substance-related harms data + StatCan Table 17-10-0009-01. "
              "39 quarters of Alberta opioid deaths, 2016 Q1 to 2025 Q3, normalised to deaths per 100k residents.",
         size=14, color=DARK)

tf = add_text(s, 0.6, 4.6, 12, 0.4, "Method", size=15, bold=True, color=BLUE)
add_para(tf, "Interrupted time series with a level and slope change around 2020 Q2. "
              "Quarter fixed effects for seasonality. Newey-West HAC SE with small-sample correction.",
         size=14, color=DARK)
add_para(tf, "Robustness: HAC lag sensitivity, donut (drop 2020 Q1), seven placebo cutoffs in the pre-period, "
              "negative binomial cross-check with log-population offset.",
         size=14, color=DARK)
add_footer(s, 4, 2)

# ===========================================================================
# Slide 3 — Findings (chart + table)
# ===========================================================================
s = prs.slides.add_slide(blank)
add_text(s, 0.6, 0.4, 12, 0.6,
         "Sharp, large, robust break at 2020 Q2",
         size=26, bold=True, color=DARK)

if os.path.exists(CHART):
    s.shapes.add_picture(CHART, Inches(0.5), Inches(1.3), width=Inches(8.2))

# Findings sidebar
tf = add_text(s, 8.9, 1.4, 4.2, 0.4, "Main spec", size=14, bold=True, color=BLUE)
add_para(tf, "Level shift at 2020 Q2:", size=12, color=GREY)
add_para(tf, "+5.50 per 100k per quarter", size=14, bold=True, color=DARK)
add_para(tf, "(95% CI +3.60, +7.39, p < 0.001)", size=11, color=GREY)
add_para(tf, "At mean AB pop: ~+246 deaths/quarter", size=11, color=GREY)

tf = add_text(s, 8.9, 3.4, 4.2, 0.4, "Robustness", size=14, bold=True, color=BLUE)
add_para(tf, "HAC L=1..6:  +5.50 (SE 0.79–0.98)", size=11, color=DARK)
add_para(tf, "Donut (drop 2020 Q1):  +5.34", size=11, color=DARK)
add_para(tf, "NB rate ratio:  2.43 (1.80, 3.26)", size=11, color=DARK)

tf = add_text(s, 8.9, 4.8, 4.2, 0.4, "Placebo cutoffs", size=14, bold=True, color=BLUE)
add_para(tf, "Seven fake cutoffs in pre-period:", size=11, color=GREY)
add_para(tf, "All point opposite direction.", size=11, color=DARK)
add_para(tf, "Largest |placebo|: 1.86", size=11, color=DARK)
add_para(tf, "Real jump (+5.50) is ~3× larger.", size=11, color=DARK)

add_footer(s, 4, 3)

# ===========================================================================
# Slide 4 — What this is and isn't
# ===========================================================================
s = prs.slides.add_slide(blank)
add_text(s, 0.6, 0.4, 12, 0.6,
         "What this identifies — and what it doesn't",
         size=26, bold=True, color=DARK)

tf = add_text(s, 0.6, 1.4, 12, 0.4, "What we can claim", size=15, bold=True, color=BLUE)
add_para(tf, "A sharp, large, robust break in Alberta opioid mortality at 2020 Q2.",
         size=14, color=DARK)
add_para(tf, "Pre-trend flat, placebos null, donut and NB cross-check consistent. "
              "This is a real shift in the data, not an artefact of specification choices.",
         size=13, color=GREY)

tf = add_text(s, 0.6, 3.1, 12, 0.4, "What we cannot claim", size=15, bold=True, color=RED)
add_para(tf, "That COVID-19 itself caused the jump.",
         size=14, color=DARK)
add_para(tf, "Many things moved at the same cutoff: the virus, public health emergency response, "
              "supply chain for the unregulated drug supply, harm reduction service capacity, mental health services, "
              "social isolation, and economic shock. ITS with a single cutoff cannot separate them.",
         size=13, color=GREY)

tf = add_text(s, 0.6, 5.0, 12, 0.4, "Next steps to sharpen identification", size=15, bold=True, color=BLUE)
add_para(tf, "1. Difference-in-discontinuities using other provinces with different pandemic-response timing", size=13, color=DARK)
add_para(tf, "2. Synthetic control to build a counterfactual Alberta without COVID", size=13, color=DARK)
add_para(tf, "3. Stratification by age, sex, zone, and substance type to localise where the shift concentrated", size=13, color=DARK)

add_footer(s, 4, 4)

prs.save(OUT)
print(f"Saved: {OUT}")
