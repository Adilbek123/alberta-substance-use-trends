"""Build a GoA-style deck — black & white, bullet points only, no jargon in
the slide bodies. Structure mirrors a Cabinet/MDM deck (Issue → Background →
Approach → Findings → Implications → Limitations → Next Steps → Questions)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

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


def title(slide, text, color=BLACK):
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.7))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.size = Pt(26)
    r.font.bold = True
    r.font.name = FONT
    r.font.color.rgb = color


def hline(slide, y=1.05):
    line = slide.shapes.add_connector(1, Inches(0.6), Inches(y), Inches(12.7), Inches(y))
    line.line.color.rgb = BLACK
    line.line.width = Pt(0.75)


def bullets(slide, left, top, width, height, items, size=16, sub_size=13):
    """items: list of either str (top-level bullet) or (str, [sub_str, ...]) tuples."""
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

# ===========================================================================
# Slide 1 — Title
# ===========================================================================
s = prs.slides.add_slide(blank)

tb = s.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(11.7), Inches(1.2))
tf = tb.text_frame
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Alberta Opioid Mortality Around the COVID-19 Onset"
r.font.size = Pt(36)
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

# Meta block (like the GoA title slide author/date)
tb = s.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.5))
tf = tb.text_frame
for line, size, color in [
    ("Adilbek Sultanov", 14, BLACK),
    ("Independent project", 12, GREY),
    ("May 2026", 12, GREY),
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
# Slide 2 — Question to be Answered
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Question to be Answered")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Did Alberta's opioid death rate shift sharply when COVID-19 hit, beyond what the prior trend explains?",
     ["Cutoff used: 2020 Q2, the first full quarter under Alberta's public health emergency",
      "Outcome: opioid-related deaths per 100,000 Alberta residents per quarter"]),
    ("Why this matters for Mental Health and Addiction work",
     ["The post-COVID baseline shapes what we measure as 'success' under the Alberta Recovery Model",
      "Understanding the size of the shift is a prerequisite for any decomposition or follow-up policy work"]),
], size=17, sub_size=13)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 2)

# ===========================================================================
# Slide 3 — Background and Context
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Background and Context")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Alberta opioid mortality from 2016 to early 2020",
     ["Quarterly opioid death rate sat around 4 per 100,000",
      "Flat trend over the five years prior to COVID — no sustained rise or fall"]),
    ("March 2020: Alberta declares a public health emergency",
     ["Many things changed at once — virus circulation, public health measures, harm reduction services, the unregulated drug supply, mental health services, social and economic conditions"]),
    ("Federal data shows opioid mortality rose sharply across Canada from 2020 onward",
     ["This analysis quantifies the Alberta-specific change at the cutoff"]),
], size=16, sub_size=13)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 3)

# ===========================================================================
# Slide 4 — Approach
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Approach")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Interrupted time series",
     ["Compare the trend in the years before the cutoff to the trend in the years after",
      "Measure the gap between them at the cutoff itself"]),
    ("Adjustments to keep the comparison fair",
     ["Use a rate per 100,000 residents (not raw counts), so population growth does not drive the result",
      "Adjust for seasonality — opioid mortality has a predictable quarter-by-quarter pattern"]),
    ("Robustness checks to ensure the result is not fragile",
     ["Move the cutoff back into the pre-period as a placebo — should produce no jump",
      "Drop the quarter that straddles the cutoff and refit",
      "Re-fit using a count model with population offset as a cross-check"]),
], size=16, sub_size=13)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 4)

# ===========================================================================
# Slide 5 — Data
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Data")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Public Health Agency of Canada — Substance-Related Harms Data",
     ["Quarterly opioid deaths in Alberta",
      "2016 Q1 through 2025 Q3 — 39 quarters in total",
      "Downloaded 20 May 2026 from health-infobase.canada.ca"]),
    ("Statistics Canada Table 17-10-0009-01 — Quarterly population estimates",
     ["Used to convert death counts into a rate per 100,000 residents"]),
    ("No internal Government of Alberta data used",
     ["All sources are public and reproducible"]),
], size=16, sub_size=13)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 5)

# ===========================================================================
# Slide 6 — Findings (chart)
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Findings — A Sharp, Large, Persistent Increase")
hline(s)

if os.path.exists(CHART):
    s.shapes.add_picture(CHART, Inches(0.6), Inches(1.3), width=Inches(8.4))

bullets(s, 9.2, 1.4, 4.0, 5.5, [
    ("Pre-COVID average",
     ["About 4 deaths per 100,000 per quarter"]),
    ("Post-COVID average",
     ["About 8 deaths per 100,000 per quarter"]),
    ("Level shift at 2020 Q2",
     ["About 5.5 per 100,000 per quarter",
      "Roughly a doubling of the rate",
      "Statistically very strong"]),
    ("Pre-COVID trend was flat",
     ["The jump is not a continuation of an existing trend"]),
], size=13, sub_size=11)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 6)

# ===========================================================================
# Slide 7 — Robustness
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Robustness — The Result Is Not Fragile")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Placebo cutoffs in the pre-period (2018–2019)",
     ["When we move the cutoff to a date before COVID, the model finds no comparable jump",
      "Largest placebo movement is about a third of the real jump, and in the opposite direction"]),
    ("Dropping the quarter that straddles the cutoff (2020 Q1)",
     ["The estimate moves by less than three per cent"]),
    ("Different statistical assumptions about standard errors",
     ["The estimate is the same; the size of the confidence interval barely changes"]),
    ("A count-model cross-check",
     ["The post-COVID rate is about 2.4× the pre-COVID rate, consistent with the main estimate"]),
], size=15, sub_size=13)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 7)

# ===========================================================================
# Slide 8 — What This Tells Us
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "What This Tells Us")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("There is a real, sharp, sustained change in Alberta opioid mortality at the COVID onset",
     ["Roughly a doubling of the rate, holding pre-trend and seasonality constant",
      "The change is large enough to persist for years, with the rate only returning toward baseline since 2024"]),
    ("The change is attributable to the COVID-19 pandemic broadly",
     ["This includes the virus, public health measures, supply chain disruption, harm reduction service changes, mental health service disruption, social isolation, and economic shock",
      "These are all downstream consequences of the pandemic — they came together by construction, not by coincidence"]),
], size=16, sub_size=13)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 8)

# ===========================================================================
# Slide 9 — What This Does NOT Tell Us
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "What This Does Not Tell Us")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("We cannot separate the virus channel from everything else that came with the pandemic",
     ["What share came from supply toxicity vs. service capacity vs. isolation vs. economic shock is a separate question",
      "Answering it needs different data — drug-checking composition, service utilization, etc."]),
    ("A peer-province comparison would not isolate a clean 'COVID-only' effect",
     ["All Canadian provinces faced COVID and its policy response at essentially the same time",
      "Comparing Alberta to BC or Ontario would identify Alberta-specific deviation, not the virus channel alone"]),
    ("The estimate captures the level shift at the cutoff, not the full trajectory",
     ["The post-COVID period peaked in 2021 Q4 and has been declining since 2024 — the average effect varies year by year"]),
], size=15, sub_size=13)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 9)

# ===========================================================================
# Slide 10 — Next Steps
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Next Steps")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Mechanism decomposition",
     ["Bring in supply-side data, service-capacity data, and outcome data to estimate the share of the jump attributable to each channel"]),
    ("Heterogeneity",
     ["Break the result down by age, sex, geographic zone, and substance type (fentanyl, carfentanil, other)"]),
    ("Post-period dynamics",
     ["Model the rise-to-peak-and-decline shape directly, rather than collapsing it into a single level shift"]),
    ("Cumulative excess deaths",
     ["Report a policy-relevant total alongside the immediate level shift"]),
], size=16, sub_size=13)

footer_left(s, "Alberta opioid mortality around COVID-19  |  independent project")
page_num(s, 10)

# ===========================================================================
# Slide 11 — Questions
# ===========================================================================
s = prs.slides.add_slide(blank)

tb = s.shapes.add_textbox(Inches(0.6), Inches(3.2), Inches(12.1), Inches(1.0))
tf = tb.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "Questions?"
r.font.size = Pt(54)
r.font.bold = True
r.font.name = FONT
r.font.color.rgb = BLACK

tb = s.shapes.add_textbox(Inches(0.6), Inches(4.5), Inches(12.1), Inches(0.5))
tf = tb.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "Code, data, and full documentation: github.com/Adilbek123/alberta-substance-use-trends"
r.font.size = Pt(14)
r.font.name = FONT
r.font.color.rgb = GREY

page_num(s, 11)

prs.save(OUT)
print(f"Saved: {OUT}")
