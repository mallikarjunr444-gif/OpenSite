import os
from PIL import Image, ImageDraw
from build_video_part1 import (
    FRAMES_DIR, BG, PANEL, PANEL_HI, LINE, LIME, WHITE, MUTED, CARD, HOVER, TEXT_MUT, CYAN,
    F_TITLE, F_HERO, F_SUB, F_BODY, F_BOLD, F_TAG, F_NARR, F_CODE,
    header, teleprompter, card
)

def render_scenes_6_and_7():
    # Frame 14 (Scene 6: 3:45 - 4:05)
    img14 = Image.new("RGB", (1920, 1080), BG)
    d14 = ImageDraw.Draw(img14)
    header(d14, 6, "Long-term Intelligence", "3:45–4:05")
    d14.text((120, 110), "Long-term Growth Intelligence", fill=WHITE, font=F_TITLE)
    d14.text((120, 165), "Connecting historical interventions directly to ongoing organic performance.", fill=MUTED, font=F_SUB)
    card(d14, 120, 220, 1680, 680, t="THE OPENSITE GROWTH JOURNEY", sub="Durable historical timeline connecting actions to verified search visibility")
    timeline = [
        ("AUG 14, 2026", "Google August Core Update", "Impression drop on thin glossary. OpenSite deprecated 35 thin pages, merged into 4 deep-dives.", "DEFENSIVE ACTION"),
        ("SEP 02, 2026", "Exp #201: Pricing Toggle", "Default monthly billing with 20% annual savings callout. ARR jumped +31% with low friction.", "CRO WINNER"),
        ("SEP 20, 2026", "Exp #204: Code Snippets", "Added interactive Mermaid diagrams and code sandboxes. Rank jumped #18 -> #3 on Google US.", "RANKING SURGE"),
        ("OCT 08, 2026", "Exp #210: 1-Click CTA", "Dispelled CC friction on signup page. Conversion surged from 2.8% to 4.7% (+67.8% relative).", "CONVERSION WINNER"),
        ("OCT 25, 2026", "Google Helpful Content", "EEAT & schema markup drove +22% organic traffic surge while AI spam competitors crashed.", "EEAT REWARD"),
        ("NOV 01, 2026", "INP Latency Optimization", "Deferred heavy scripts. INP 290ms -> 48ms. Mobile impressions climbed 16% in 7 days.", "TECHNICAL SEO")
    ]
    tx = 160
    for i, (date, title, desc, tag) in enumerate(timeline):
        x = tx + (i % 3) * 545
        y = 320 + (i // 3) * 250
        card(d14, x, y, 520, 230, border=HOVER)
        d14.text((x + 20, y + 18), date, fill=LIME, font=F_TAG)
        d14.text((x + 130, y + 18), tag, fill=CYAN, font=F_TAG)
        d14.text((x + 20, y + 45), title, fill=WHITE, font=F_BOLD)
        words = desc.split(" ")
        cur, l_list = "", []
        for w in words:
            if len(cur + " " + w) < 38: cur += (" " if cur else "") + w
            else: l_list.append(cur); cur = w
        if cur: l_list.append(cur)
        dy = y + 80
        for l in l_list:
            d14.text((x + 20, dy), l, fill=TEXT_MUT, font=F_TAG)
            dy += 24
    teleprompter(d14, "With historical information and current website performance, OpenSite aims to help businesses make more informed growth decisions. For example, it can compare previous SEO recommendations with subsequent performance, review ranking changes, and identify areas needing attention.")
    img14.save(os.path.join(FRAMES_DIR, "frame_14.png"))

    # Frame 15 (Scene 6: 4:05 - 4:20)
    img15 = Image.new("RGB", (1920, 1080), BG)
    d15 = ImageDraw.Draw(img15)
    header(d15, 6, "Long-term Intelligence", "4:05–4:20")
    d15.text((120, 110), "The Vision: An Agent That Learns Your Site", fill=WHITE, font=F_TITLE)
    d15.text((120, 165), "Understanding a website's growth journey and continuously discovering new opportunities.", fill=MUTED, font=F_SUB)
    card(d15, 120, 220, 1680, 680, t="CLOSED-LOOP AI RECOMMENDATION ENGINE", sub="Continuous Synthesis of Search Changes, Content Performance, and Conversion Testing")
    d15.text((160, 310), "How the OpenSite Growth Agent Operates Continuously:", fill=WHITE, font=F_BOLD)
    loop_steps = [
        ("1. AUDIT & INGEST", "Continuously ingests Search Console metrics, analytics conversions, and crawls on-page technical health."),
        ("2. RECALL HISTORICAL WINS", "Before proposing an action, recalls what succeeded or failed in similar past experiments and algorithm updates."),
        ("3. FORMULATE HYPOTHESIS", "Generates high-conviction, evidence-backed recommendations with explicit predicted outcomes."),
        ("4. RETAIN OUTCOMES", "Once changes are deployed and telemetry is measured, retains the final outcome to compound the site's memory.")
    ]
    ly = 360
    for step, desc in loop_steps:
        d15.rounded_rectangle([(160, ly), (1760, ly + 95)], radius=10, fill=PANEL, outline=HOVER)
        d15.text((190, ly + 22), step, fill=LIME, font=F_BOLD)
        d15.text((190, ly + 55), desc, fill=TEXT_MUT, font=F_BODY)
        ly += 125
    teleprompter(d15, "The long-term vision is to create an agent that understands a website's growth journey and continuously helps users discover opportunities for improvement.")
    img15.save(os.path.join(FRAMES_DIR, "frame_15.png"))

    # Frame 16 (Scene 7: 4:20 - 4:35)
    img16 = Image.new("RGB", (1920, 1080), BG)
    d16 = ImageDraw.Draw(img16)
    header(d16, 7, "Conclusion", "4:20–4:35")
    card(d16, 260, 170, 1400, 710, border=(72, 93, 46), fill=(13, 14, 11))
    d16.line([(260, 170), (1660, 170)], fill=LIME, width=4)
    d16.text((340, 250), "OpenSite", fill=WHITE, font=F_HERO)
    d16.text((340, 350), "Understand. Optimize. Grow.", fill=LIME, font=F_TITLE)
    d16.text((340, 430), (
        "To conclude, OpenSite is our approach to making website optimization\n"
        "more intelligent, continuous, and data-driven.\n\n"
        "By combining SEO and conversion intelligence with persistent AI memory through Hindsight,\n"
        "we built an agent that doesn't simply analyze websites — but learns from their history."
    ), fill=WHITE, font=F_BODY)
    px = 340
    for p_title, p_desc in [
        ("INTELLIGENT", "Combines SEO, CRO, technical audits & queries."),
        ("CONTINUOUS", "Tracks performance across time and updates."),
        ("STATEFUL", "Powered by Hindsight persistent memory.")
    ]:
        card(d16, px, 630, 380, 190, border=HOVER)
        d16.text((px + 24, 660), p_title, fill=LIME, font=F_BOLD)
        d16.text((px + 24, 705), p_desc, fill=TEXT_MUT, font=F_BODY)
        px += 420
    teleprompter(d16, "To conclude, OpenSite is our approach to making website optimization more intelligent, continuous and data-driven. By combining SEO and conversion intelligence with persistent AI memory through Hindsight, we aim to build an agent that doesn't simply analyze websites but also learns from their history.")
    img16.save(os.path.join(FRAMES_DIR, "frame_16.png"))

    # Frame 17 (Scene 7: 4:35 - 4:45)
    img17 = Image.new("RGB", (1920, 1080), BG)
    d17 = ImageDraw.Draw(img17)
    header(d17, 7, "Conclusion", "4:35–4:45")
    card(d17, 360, 190, 1200, 670, border=(72, 93, 46), fill=(13, 14, 11))
    d17.line([(360, 190), (1560, 190)], fill=LIME, width=4)
    d17.text((440, 270), "Thank You for Watching!", fill=WHITE, font=F_HERO)
    d17.text((440, 360), "OpenSite — SEO & Conversion Intelligence Agent", fill=LIME, font=F_SUB)
    d17.text((440, 430), "Presenter: Mallikarjun", fill=WHITE, font=F_BOLD)
    d17.text((440, 470), "Technology: Hindsight AI Memory (Retain / Recall / Reflect)", fill=TEXT_MUT, font=F_BODY)
    d17.text((440, 510), "Core Engine: Streamlit, Python, Search Console, GA4 & CrUX Connectors", fill=TEXT_MUT, font=F_BODY)
    d17.rounded_rectangle([(440, 590), (1050, 660)], radius=10, fill=PANEL, outline=HOVER)
    d17.text((470, 615), "OpenSite: Understand. Optimize. Grow.", fill=LIME, font=F_CODE)
    d17.text((440, 720), "Project Showcase: Hindsight Hackathon Submission", fill=MUTED, font=F_BOLD)
    teleprompter(d17, "Thank you for watching. This is OpenSite. Understand. Optimize. Grow.")
    img17.save(os.path.join(FRAMES_DIR, "frame_17.png"))
    print("Rendered Scenes 6 and 7 (frames 14 to 17).")

if __name__ == "__main__":
    render_scenes_6_and_7()
