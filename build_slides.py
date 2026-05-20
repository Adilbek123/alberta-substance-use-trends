"""Build a 7-slide deck as a policy briefing arc with sentence-style titles.
Black and white, formal bullet structure, no jargon in bodies.

Slide titles read as a storyline:
  1. (Cover)
  2. COVID-19 hit Alberta in March 2020, and many other things shifted at the same time
  3. Did Alberta opioid mortality jump at the COVID onset, and is it real or noise?
  4. An interrupted time series compares the pre-COVID and post-COVID periods statistically
  5. The death rate roughly doubled at 2020 Q2, sharp, large, and robust
  6. The pandemic as a whole shifted opioid mortality, not the virus alone
  7. Post-COVID baseline is higher than pre-COVID, and recovery is already underway
"""
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

BLACK = RGBColor(0x00, 0x00, 0x00)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x55, 0x55, 0x55)
LIGHT = RGBColor(0x99, 0x99, 0x99)

FONT = "Calibri"


def title(slide, text):
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.name = FONT
    r.font.color.rgb = BLACK


def hline(slide, y=1.45):
    line = slide.shapes.add_connector(1, Inches(0.6), Inches(y), Inches(12.7), Inches(y))
    line.line.color.rgb = BLACK
    line.line.width = Pt(0.75)


def bullets(slide, left, top, width, height, items, size=15, sub_size=12):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if isinstance(item, tuple):
            main, subs = item
        else:
            main, subs = item, []
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.level = 0
        r = p.add_run()
        r.text = "•  " + main
        r.font.size = Pt(size)
        r.font.name = FONT
        r.font.color.rgb = DARK
        for sub in subs:
            p = tf.add_paragraph()
            p.level = 1
            r = p.add_run()
            r.text = "–  " + sub
            r.font.size = Pt(sub_size)
            r.font.name = FONT
            r.font.color.rgb = GREY
    return tf


def page_num(slide, n):
    tb = slide.shapes.add_textbox(Inches(12.6), Inches(7.05), Inches(0.6), Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    r = p.add_run()
    r.text = str(n)
    r.font.size = Pt(10)
    r.font.name = FONT
    r.font.color.rgb = LIGHT


def footer_left(slide, text):
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(7.05), Inches(11), Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.size = Pt(9)
    r.font.name = FONT
    r.font.color.rgb = LIGHT


blank = prs.slide_layouts[6]
FOOTER = "Alberta opioid mortality around COVID-19  |  independent project"

# ===========================================================================
# Slide 1 - Cover
# ===========================================================================
s = prs.slides.add_slide(blank)

tb = s.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(11.7), Inches(1.2))
tf = tb.text_frame
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Alberta opioid mortality around the COVID-19 onset"
r.font.size = Pt(34)
r.font.bold = True
r.font.name = FONT
r.font.color.rgb = BLACK

tb = s.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11.7), Inches(0.5))
tf = tb.text_frame
p = tf.paragraphs[0]
r = p.add_run()
r.text = "An interrupted time series analysis using federal data"
r.font.size = Pt(18)
r.font.name = FONT
r.font.color.rgb = GREY

tb = s.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.6))
tf = tb.text_frame
for line, size, color in [
    ("Adilbek Sultanov", 14, BLACK),
    ("Independent project, May 2026", 12, GREY),
    ("github.com/Adilbek123/alberta-substance-use-trends", 11, GREY),
]:
    if tf.text == "":
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    r = p.add_run()
    r.text = line
    r.font.size = Pt(size)
    r.font.name = FONT
    r.font.color.rgb = color

page_num(s, 1)

# ===========================================================================
# Slide 2 - Background
#   "COVID-19 hit Alberta in March 2020, and many other things shifted at the same time"
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "COVID-19 hit Alberta in March 2020, and many other things shifted at the same time")
hline(s)

bullets(s, 0.7, 1.7, 12, 5.0, [
    ("COVID-19 was declared a pandemic by the WHO on 11 March 2020",
     ["Alberta declared a public health emergency on 17 March 2020",
      "Roughly 60,000 Canadians have died from COVID-19 directly between 2020 and 2023"]),
    ("Beyond the virus itself, the pandemic disrupted multiple systems at once",
     ["Drug supply chains for the unregulated drug market",
      "Harm reduction services (e.g., supervised consumption sites operating at reduced capacity)",
      "Mental health and addiction services (in-person care disruption, telehealth ramp-up lag)",
      "Employment, housing, and social connection"]),
    ("Other provinces reported a surge in opioid deaths from 2020 onward",
     ["British Columbia, Ontario, and others saw sharp increases at roughly the same time",
      "Alberta's pattern has not been quantified at this granularity in public analysis"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 2)

# ===========================================================================
# Slide 3 - The Question
#   "Did Alberta opioid mortality jump at the COVID onset, and is it real or noise?"
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Did Alberta opioid mortality jump at the COVID onset, and is it real or noise?")
hline(s)

bullets(s, 0.7, 1.7, 12, 5.0, [
    ("Pre-COVID context",
     ["Alberta opioid death rate sat around 4 per 100,000 residents per quarter, 2016 through early 2020",
      "Flat trend across that period, no sustained rise or fall"]),
    ("If a jump occurred at COVID, two things matter for policy",
     ["How large was it? This sets the post-COVID baseline against which Recovery Model progress will be measured",
      "Is it real, or could random variation in a noisy series explain it? This determines whether the change calls for action"]),
    ("This analysis answers both questions",
     ["Whether the level shift exists at the cutoff, separately from the existing trend",
      "Whether the size of the shift is meaningfully larger than what random variation could produce"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 3)

# ===========================================================================
# Slide 4 - Approach
#   "An interrupted time series compares the pre-COVID and post-COVID periods statistically"
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "An interrupted time series compares the pre-COVID and post-COVID periods statistically")
hline(s)

bullets(s, 0.7, 1.7, 12, 5.0, [
    ("Method: interrupted time series (also called segmented regression)",
     ["Fits one trend to the pre-COVID years, another to the post-COVID years",
      "Measures the gap between them at the cutoff (2020 Q2, first full quarter under the emergency)",
      "Tests whether that gap is meaningfully larger than the natural noise in the data"]),
    ("Data",
     ["Opioid deaths: Public Health Agency of Canada Health Infobase, Alberta quarterly, 2016 Q1 to 2025 Q3",
      "Population: Statistics Canada Table 17-10-0009-01, used to convert counts to a rate per 100,000",
      "No internal Government of Alberta data is used; all sources are public"]),
    ("Robustness checks confirm the result is not an artifact of method choices",
     ["Placebo cutoffs placed in the pre-period (should produce no jump if the design is credible)",
      "Drop the quarter that straddles the cutoff and refit",
      "Cross-check using a count model with a population offset"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 4)

# ===========================================================================
# Slide 5 - Findings (with chart)
#   "The death rate roughly doubled at 2020 Q2, sharp, large, and robust"
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "The death rate roughly doubled at 2020 Q2, sharp, large, and robust")
hline(s)

if os.path.exists(CHART):
    s.shapes.add_picture(CHART, Inches(0.5), Inches(1.65), width=Inches(8.4))

bullets(s, 9.2, 1.7, 4.0, 5.0, [
    ("Pre-COVID average",
     ["About 4 deaths per 100,000 per quarter"]),
    ("Post-COVID average",
     ["About 8 deaths per 100,000 per quarter"]),
    ("Level shift at the cutoff",
     ["About 5.5 per 100,000 per quarter",
      "Roughly a doubling",
      "Statistically very strong (p < 0.001)"]),
    ("Pre-COVID trend was flat",
     ["The jump is not part of an existing rise"]),
    ("All robustness checks hold",
     ["Placebos produce no jump",
      "Drop-quarter estimate moves <3%",
      "Cross-check confirms"]),
], size=12, sub_size=10)

footer_left(s, FOOTER)
page_num(s, 5)

# ===========================================================================
# Slide 6 - Interpretation
#   "The pandemic as a whole shifted opioid mortality, not the virus alone"
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "The pandemic as a whole shifted opioid mortality, not the virus alone")
hline(s)

bullets(s, 0.7, 1.7, 12, 5.0, [
    ("The total effect attributable to the pandemic, including its downstream consequences",
     ["Virus, public health measures, drug supply disruption, harm reduction capacity, mental health service disruption, isolation, economic shock",
      "These came together by construction, not by coincidence; a pandemic without them is not a counterfactual that exists in any data"]),
    ("The analysis cannot separate which channel did the most damage",
     ["Decomposing into supply vs. services vs. isolation vs. economic shock requires different data",
      "Drug-checking composition, service utilization series, and similar mechanism-level sources"]),
    ("Comparing Alberta to other provinces would not isolate a virus-only effect",
     ["Every Canadian province faced COVID and its policy response at essentially the same time",
      "A peer comparison would identify Alberta-specific deviation from the common pattern, not the virus channel alone"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 6)

# ===========================================================================
# Slide 7 - Implications
#   "Post-COVID baseline is higher than pre-COVID, and recovery is already underway"
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Post-COVID baseline is higher than pre-COVID, and recovery is already underway")
hline(s)

bullets(s, 0.7, 1.7, 12, 5.0, [
    ("For Recovery Model performance measurement, the baseline matters",
     ["The post-COVID baseline is roughly double the pre-COVID baseline",
      "Any 'return to baseline' framing needs to be explicit about which baseline"]),
    ("The trajectory is not flat: a real recovery is already visible",
     ["The post-COVID period peaked in 2021 Q4 and has been declining since 2024",
      "A single average over the post-period masks this dynamic"]),
    ("The next analytical work is decomposition, not better identification",
     ["Which channel drove most of the shift (supply, services, isolation, economic)",
      "Which age groups, geographic zones, and substance types concentrate the increase",
      "Modelling the rise-to-peak-and-decline shape directly, rather than a single level shift",
      "Cumulative excess deaths through end-of-sample as a policy-relevant total"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 7)

prs.save(OUT)
print(f"Saved: {OUT}")
