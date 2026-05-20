"""Build a GoA-style briefing deck.

Format mirrors a Cabinet/MDM deck (section labels, not sentence headlines):
  1. Cover
  2. Issue
  3. Purpose
  4. Background
  5. Approach
  6. Findings
  7. What This Means
  8. Limitations and Next Steps

Black and white, bullet structure, no jargon in bodies. Every external fact
that is verifiable has been verified; claims that could not be verified have
been removed or softened.
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
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.7))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.size = Pt(26)
    r.font.bold = True
    r.font.name = FONT
    r.font.color.rgb = BLACK


def hline(slide, y=1.05):
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
r.text = "Alberta Opioid Mortality Around the COVID-19 Onset"
r.font.size = Pt(34)
r.font.bold = True
r.font.name = FONT
r.font.color.rgb = BLACK

tb = s.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11.7), Inches(0.5))
tf = tb.text_frame
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Interrupted Time Series Analysis Using Federal Data"
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
# Slide 2 - Issue
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Issue")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Opioid mortality in Alberta has risen sharply since the start of the COVID-19 pandemic, but the size and timing of the shift have not been quantified for this analysis at quarterly resolution.",
     []),
    ("Without a defensible measurement of the post-COVID baseline, performance under the Alberta Recovery Model cannot be evaluated against a meaningful counterfactual.",
     []),
    ("This analysis quantifies the level shift at the COVID onset using publicly available federal data, and tests whether the shift is statistically meaningful or could be explained by random variation in a noisy series.",
     []),
], size=16, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 2)

# ===========================================================================
# Slide 3 - Purpose
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Purpose")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Establish whether Alberta's opioid death rate shifted at the COVID-19 onset",
     ["Identify the size of the shift, if any",
      "Test whether the shift is meaningfully larger than the natural noise in the data"]),
    ("Inform the post-COVID baseline used for Recovery Model performance measurement",
     ["The baseline before the pandemic is materially different from the baseline after",
      "Any performance framing needs to be explicit about which baseline it compares to"]),
    ("Demonstrate an analytical approach the Ministry's Business Intelligence team could apply to other indicators",
     ["The same method applies to hospitalization, emergency department, and EMS data",
      "Same data source, same code structure, different outcome variable"]),
], size=15, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 3)

# ===========================================================================
# Slide 4 - Background
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Background")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("COVID-19 pandemic context",
     ["WHO characterized COVID-19 as a pandemic on 11 March 2020",
      "Alberta declared a provincial public health emergency on 17 March 2020",
      "Approximately 60,000 Canadians have died from the virus directly through 2024"]),
    ("Beyond the virus itself, the pandemic disrupted several systems at once",
     ["Drug supply chains for the unregulated drug market",
      "Harm reduction service delivery (in-person service capacity, hours, access)",
      "Mental health and addiction service delivery (in-person care disruption)",
      "Employment, housing, and social connection"]),
    ("Other provinces reported a substantial increase in opioid mortality starting 2020 Q2",
     ["British Columbia: quarterly opioid deaths roughly doubled (2019 average vs 2020 Q2 to 2021 Q1)",
      "Ontario: quarterly opioid deaths rose by roughly 75 per cent over the same comparison",
      "Federal data (PHAC) confirms a Canada-wide pattern at the same cutoff"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 4)

# ===========================================================================
# Slide 5 - Approach
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Approach")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Method: interrupted time series (segmented regression)",
     ["Fits one trend to the pre-COVID years, another to the post-COVID years",
      "Measures the gap between them at the cutoff (2020 Q2, first full quarter under the emergency)",
      "Tests whether that gap is meaningfully larger than the natural noise in the data"]),
    ("Data",
     ["Opioid deaths: Public Health Agency of Canada, Health Infobase, Alberta quarterly, 2016 Q1 to 2025 Q3",
      "Population: Statistics Canada Table 17-10-0009-01, used to convert counts to a rate per 100,000",
      "No internal Government of Alberta data is used; all sources are public"]),
    ("Robustness checks confirm the result is not an artefact of method choices",
     ["Placebo cutoffs placed in the pre-period (should produce no jump if the design is credible)",
      "Drop the quarter that straddles the cutoff and refit",
      "Cross-check using a count model with a population offset"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 5)

# ===========================================================================
# Slide 6 - Findings
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Findings")
hline(s)

if os.path.exists(CHART):
    s.shapes.add_picture(CHART, Inches(0.5), Inches(1.25), width=Inches(8.4))

bullets(s, 9.2, 1.4, 4.0, 5.5, [
    ("Pre-COVID average",
     ["About 4 deaths per 100,000 per quarter"]),
    ("Post-COVID average",
     ["About 8 deaths per 100,000 per quarter"]),
    ("Level shift at the cutoff",
     ["About 5.5 per 100,000 per quarter",
      "Roughly a doubling of the rate",
      "Statistically very strong (p < 0.001)"]),
    ("Pre-COVID trend was flat",
     ["The jump is not part of an existing rise"]),
    ("All robustness checks hold",
     ["Placebos produce no jump",
      "Drop-quarter estimate moves <3%",
      "Cross-check confirms"]),
], size=12, sub_size=10)

footer_left(s, FOOTER)
page_num(s, 6)

# ===========================================================================
# Slide 7 - What This Means
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "What This Means")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("The analysis identifies the total effect of the COVID-19 pandemic on Alberta opioid mortality",
     ["This includes the virus, the public health response, drug supply chain disruption, harm reduction service impacts, mental health service impacts, isolation, and the economic shock",
      "These are downstream consequences of the pandemic, not independent causes"]),
    ("The analysis does NOT separate the virus from everything else the pandemic brought together",
     ["What share came from supply versus services versus isolation versus economic shock is a separate, mechanism-level question",
      "Comparing Alberta to other provinces would not solve this, because all provinces faced COVID and its policy response at the same time"]),
    ("For Recovery Model performance measurement, the baseline matters",
     ["The post-COVID baseline is roughly double the pre-COVID baseline",
      "Any 'return to baseline' framing needs to be explicit about which baseline",
      "The post-COVID trajectory is already declining since 2024, suggesting a real recovery is underway"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 7)

# ===========================================================================
# Slide 8 - Limitations and Next Steps
# ===========================================================================
s = prs.slides.add_slide(blank)
title(s, "Limitations and Next Steps")
hline(s)

bullets(s, 0.7, 1.5, 12, 5.0, [
    ("Limitations",
     ["Single province, single outcome (opioid deaths) - no decomposition by substance type, age, sex, or zone",
      "Quarterly data is small for inference (39 observations); reliance on robustness checks rather than asymptotic theory alone",
      "Reporting lag and revisions: the most recent quarters may move as data is updated"]),
    ("Realistic next analytical work",
     ["Mechanism decomposition: bring in supply-side, service-capacity, and outcome data to attribute share to each channel",
      "Heterogeneity: by age, sex, zone, and substance type (fentanyl, carfentanil, other)",
      "Post-period dynamics: model the rise-to-peak-and-decline shape directly",
      "Cumulative excess deaths through end-of-sample as a policy-relevant total"]),
    ("Code, data, and full documentation",
     ["github.com/Adilbek123/alberta-substance-use-trends"]),
], size=14, sub_size=12)

footer_left(s, FOOTER)
page_num(s, 8)

prs.save(OUT)
print(f"Saved: {OUT}")
