import os
from PIL import Image, ImageDraw
from build_video_part1 import (
    FRAMES_DIR, BG, PANEL, PANEL_HI, LINE, LIME, WHITE, MUTED, CARD, HOVER, TEXT_MUT, CYAN,
    F_TITLE, F_HERO, F_SUB, F_BODY, F_BOLD, F_METRIC, F_TAG, F_NARR, F_CODE,
    header, teleprompter, card
)

def render_scenes_1_to_3():
    # Frame 01 (Scene 1: 0:00 - 0:15)
    img = Image.new("RGB", (1920, 1080), BG)
    d = ImageDraw.Draw(img)
    header(d, 1, "Introduction", "0:00–0:15")
    card(d, 260, 150, 1400, 740, border=(72, 93, 46), fill=(14, 16, 12))
    d.line([(260, 150), (1660, 150)], fill=LIME, width=4)
    d.text((340, 220), "OpenSite", fill=WHITE, font=F_HERO)
    d.ellipse([(670, 245), (688, 263)], fill=LIME)
    d.text((705, 245), "AI GROWTH & CONVERSION AGENT", fill=LIME, font=F_SUB)
    d.text((340, 320), "Understand. Optimize. Grow.", fill=(220, 222, 212), font=F_SUB)
    d.text((340, 370), "A unified intelligence platform combining real-time SEO telemetry, CRO experiment tracking,\nand persistent agent memory powered by Hindsight.", fill=TEXT_MUT, font=F_BODY)
    bx = 340
    for tag, desc in [("● PERSISTENT AI MEMORY", "Retain & recall ranking signals"), ("● UNIFIED WORKSPACE", "Audit, keywords & experiments"), ("● CLOSED-LOOP ADVISOR", "Evidence-based growth strategies")]:
        card(d, bx, 510, 380, 180, border=HOVER)
        d.text((bx + 20, 535), tag, fill=LIME, font=F_TAG)
        d.text((bx + 20, 570), desc, fill=WHITE, font=F_BOLD)
        d.text((bx + 20, 615), "Active across 12 intelligence modules", fill=MUTED, font=F_TAG)
        bx += 420
    d.rounded_rectangle([(340, 750), (840, 810)], radius=30, fill=PANEL, outline=LINE)
    d.text((365, 765), "SPEAKER: Mallikarjun  |  PRODUCT DEMONSTRATION", fill=WHITE, font=F_TAG)
    teleprompter(d, "Hello everyone! I'm Mallikarjun, and today I'm introducing OpenSite, an SEO and Conversion Intelligence Agent.")
    img.save(os.path.join(FRAMES_DIR, "frame_01.png"))

    # Frame 02 (Scene 1: 0:15 - 0:30)
    img2 = Image.new("RGB", (1920, 1080), BG)
    d2 = ImageDraw.Draw(img2)
    header(d2, 1, "Introduction", "0:15–0:30")
    d2.text((120, 110), "Why OpenSite Exists", fill=WHITE, font=F_TITLE)
    d2.text((120, 165), "Bringing website intelligence and AI-driven recommendations together in one unified platform.", fill=MUTED, font=F_SUB)
    card(d2, 120, 220, 800, 680, t="THE OPENSITE APPROACH", sub="Bridging Search Visibility & Conversion Funnels")
    d2.text((150, 310), "OpenSite is designed to help website owners:", fill=WHITE, font=F_BOLD)
    py = 370
    for t, desc in [("1. Understand website performance", "Continuous telemetry across search rankings, traffic, and user behavior."), ("2. Improve search engine visibility", "Prioritized technical fixes, keyword opportunities, and algorithm defenses."), ("3. Analyze visitor behavior", "Correlating landing page adjustments with actual conversion lift and ARR."), ("4. Make better growth decisions", "Leveraging verified historical outcomes instead of guessing what works.")]:
        d2.ellipse([(150, py + 6), (160, py + 16)], fill=LIME)
        d2.text((180, py), t, fill=WHITE, font=F_BOLD)
        d2.text((180, py + 26), desc, fill=TEXT_MUT, font=F_TAG)
        py += 80
    card(d2, 960, 220, 840, 680, t="LIVE PRODUCT DASHBOARD", sub="Clean, dark-mode native growth intelligence workspace")
    mx, my = 1000, 320
    for i, (label, val, delta) in enumerate([("ORGANIC CLICKS", "42,000", "+14% vs baseline"), ("CONVERSION RATE", "2.4%", "Lead capture rate"), ("GROWTH MEMORIES", "8 Signals", "Hindsight store active"), ("POSITIVE EXPERIMENTS", "4 Wins", "6 Tests recorded")]):
        gx = mx + (i % 2) * 400
        gy = my + (i // 2) * 140
        d2.rounded_rectangle([(gx, gy), (gx + 370, gy + 115)], radius=10, fill=PANEL, outline=LINE)
        d2.text((gx + 20, gy + 15), label, fill=MUTED, font=F_TAG)
        d2.text((gx + 20, gy + 38), val, fill=WHITE, font=F_METRIC)
        d2.text((gx + 20, gy + 82), delta, fill=LIME, font=F_TAG)
    d2.rounded_rectangle([(1000, 630), (1760, 850)], radius=10, fill=PANEL, outline=HOVER)
    d2.text((1030, 660), "GROWTH BRIEFING FEED · RECENT SIGNALS", fill=LIME, font=F_TAG)
    d2.text((1030, 700), "• Google August Core Update: Deprecated 35 thin definition pages (-14% drop reversed)", fill=TEXT_MUT, font=F_CODE)
    d2.text((1030, 745), "• Exp #201 Pricing Headline: Monthly default + 20% annual callout delivered +31% Net ARR", fill=TEXT_MUT, font=F_CODE)
    d2.text((1030, 790), "• Exp #210 1-Click CTA: dispelled CC friction, surging signup conversion to 4.7%", fill=TEXT_MUT, font=F_CODE)
    teleprompter(d2, "OpenSite is designed to help website owners understand their website performance, improve search engine visibility, analyze visitor behaviour, and make better growth decisions. Our goal is to bring website intelligence and AI-driven recommendations together in one unified platform.")
    img2.save(os.path.join(FRAMES_DIR, "frame_02.png"))

    # Frame 03 (Scene 2: 0:30 - 0:55)
    img3 = Image.new("RGB", (1920, 1080), BG)
    d3 = ImageDraw.Draw(img3)
    header(d3, 2, "Problem Statement", "0:30–0:55")
    d3.text((120, 110), "The Four Growth Bottlenecks", fill=WHITE, font=F_TITLE)
    d3.text((120, 165), "Today, businesses face several challenges when managing their online presence.", fill=MUTED, font=F_SUB)
    problems = [
        ("1. FRAGMENTED DATA SILOS", "Understanding website performance requires analyzing information from multiple areas: SEO, keyword rankings, website health, content performance, and visitor behaviour."),
        ("2. MISSING VALIDATION LOOP", "Identifying an SEO issue is only the beginning. Businesses also need to understand whether their previous improvements actually worked over time."),
        ("3. ZERO HISTORICAL CONTEXT", "Most conventional analysis focuses on current performance rather than maintaining meaningful historical context of past tests and algorithm updates."),
        ("4. DATA OVERLOAD VS ACTION", "Businesses need actionable recommendations instead of just large amounts of reports, disconnected spreadsheets, and raw metrics dashboards.")
    ]
    gx, gy = 120, 230
    for i, (title, desc) in enumerate(problems):
        x = gx + (i % 2) * 850
        y = gy + (i // 2) * 320
        card(d3, x, y, 820, 290, t=title, border=(180, 60, 60) if i==0 else HOVER)
        d3.line([(x + 24, y + 60), (x + 796, y + 60)], fill=LINE, width=1)
        words = desc.split(" ")
        cur, l_list = "", []
        for w in words:
            if len(cur + " " + w) < 55: cur += (" " if cur else "") + w
            else: l_list.append(cur); cur = w
        if cur: l_list.append(cur)
        dy = y + 80
        for l in l_list:
            d3.text((x + 24, dy), l, fill=TEXT_MUT, font=F_BODY)
            dy += 30
        d3.rounded_rectangle([(x + 24, y + 230), (x + 360, y + 265)], radius=6, fill=PANEL, outline=LINE)
        d3.text((x + 36, y + 240), f"STATUS QUO PAIN POINT #{i+1}", fill=(255, 120, 120), font=F_TAG)
    teleprompter(d3, "Today, businesses face several challenges when managing their online presence. First, understanding website performance requires analyzing multiple areas. Second, identifying an issue is only the beginning. Third, conventional tools focus only on current data. And finally, businesses need actionable recommendations.")
    img3.save(os.path.join(FRAMES_DIR, "frame_03.png"))

    # Frame 04 (Scene 2: 0:55 - 1:15)
    img4 = Image.new("RGB", (1920, 1080), BG)
    d4 = ImageDraw.Draw(img4)
    header(d4, 2, "Problem Statement", "0:55–1:15")
    d4.text((120, 110), "The Core Research & Engineering Question", fill=WHITE, font=F_TITLE)
    d4.text((120, 165), "Moving from isolated, static reporting to continuous compounding intelligence.", fill=MUTED, font=F_SUB)
    card(d4, 120, 230, 1680, 670, border=(72, 93, 46), fill=(13, 14, 11))
    d4.line([(120, 230), (1800, 230)], fill=LIME, width=3)
    d4.text((200, 310), "THIS CREATES AN IMPORTANT PROBLEM:", fill=LIME, font=F_SUB)
    q_text = '"How can we build an AI agent that continuously understands\na website\'s performance, remembers its previous changes,\nand helps improve its growth over time?"'
    d4.text((200, 370), q_text, fill=WHITE, font=F_HERO)
    card(d4, 200, 600, 680, 240, t="TRADITIONAL SEO / CRO WORKFLOW", sub="Stateless & Fragmented")
    d4.text((230, 680), "• Runs one-off audit → forgets results next week", fill=TEXT_MUT, font=F_BODY)
    d4.text((230, 720), "• Team repeats identical failed headline experiments", fill=TEXT_MUT, font=F_BODY)
    d4.text((230, 760), "• No connection between algorithm shifts and site fixes", fill=TEXT_MUT, font=F_BODY)
    card(d4, 940, 600, 740, 240, t="OPENSITE + HINDSIGHT SOLUTION", sub="Stateful & Compounding")
    d4.text((970, 680), "• Retains every audit, experiment outcome & ranking delta", fill=LIME, font=F_BODY)
    d4.text((970, 720), "• Recalls historical wins before recommending new actions", fill=LIME, font=F_BODY)
    d4.text((970, 760), "• Closed-loop learning system that gets smarter with every test", fill=LIME, font=F_BODY)
    teleprompter(d4, "This creates an important problem: how can we build an AI agent that continuously understands a website's performance, remembers its previous changes, and helps improve its growth over time?")
    img4.save(os.path.join(FRAMES_DIR, "frame_04.png"))

    # Frame 05 (Scene 3: 1:15 - 1:30)
    img5 = Image.new("RGB", (1920, 1080), BG)
    d5 = ImageDraw.Draw(img5)
    header(d5, 3, "Introducing OpenSite", "1:15–1:30")
    d5.text((120, 110), "Introducing OpenSite", fill=WHITE, font=F_TITLE)
    d5.text((120, 165), "OpenSite brings multiple website growth capabilities together into one unified platform.", fill=MUTED, font=F_SUB)
    card(d5, 120, 230, 1680, 670, t="UNIFIED GROWTH ENGINE ARCHITECTURE", sub="Telemetry Ingestion, Real-Time Crawling & Persistent Hindsight Bank")
    cols = [
        ("DATA INGESTION", ["Google Search Console", "GA4 & Plausible", "PostHog & Umami", "Google Search Central RSS", "CrUX & PageSpeed"]),
        ("CORE INTELLIGENCE", ["Technical Site Auditor", "SERP & Keyword Tracker", "A/B Experiment Engine", "Content Evaluator", "Local SEO & Maps"]),
        ("PERSISTENT MEMORY", ["Hindsight Client SDK", "Local Durable Store", "Durable Memory Banks", "Semantic Tagging", "Temporal Versioning"]),
        ("AI GROWTH AGENT", ["Evidence Retrieval", "Outcome Comparison", "Predictive Synthesis", "Automated Action Plans", "Executive Briefings"])
    ]
    cx = 160
    for title, items in cols:
        card(d5, cx, 320, 370, 520, t=title, border=HOVER)
        iy = 410
        for it in items:
            d5.rounded_rectangle([(cx + 20, iy), (cx + 350, iy + 50)], radius=6, fill=PANEL, outline=LINE)
            d5.text((cx + 35, iy + 15), it, fill=WHITE if "Hindsight" in it or "Agent" in it else TEXT_MUT, font=F_BOLD if "Hindsight" in it else F_BODY)
            iy += 66
        cx += 400
    d5.line([(530, 580), (560, 580)], fill=LIME, width=3)
    d5.line([(930, 580), (960, 580)], fill=LIME, width=3)
    d5.line([(1330, 580), (1360, 580)], fill=LIME, width=3)
    teleprompter(d5, "To address these challenges, we developed OpenSite. OpenSite brings multiple website growth capabilities into one platform: SEO intelligence, keyword analysis, technical website auditing, content optimization, competitor intelligence, conversion analysis, and local SEO.")
    img5.save(os.path.join(FRAMES_DIR, "frame_05.png"))

    # Frame 06 (Scene 3: 1:30 - 1:45)
    img6 = Image.new("RGB", (1920, 1080), BG)
    d6 = ImageDraw.Draw(img6)
    header(d6, 3, "Introducing OpenSite", "1:30–1:45")
    d6.text((120, 110), "What Makes OpenSite Different?", fill=WHITE, font=F_TITLE)
    d6.text((120, 165), "Persistent intelligence: It does not just analyze today—it remembers past analyses for future recommendations.", fill=MUTED, font=F_SUB)
    card(d6, 120, 220, 800, 670, t="WITHOUT PERSISTENT MEMORY", sub="The traditional stateless AI agent trap")
    d6.text((150, 320), "Standard AI agents start from scratch every session:", fill=WHITE, font=F_BOLD)
    d6.text((150, 380), "• Analyzes today's rankings with zero context", fill=TEXT_MUT, font=F_BODY)
    d6.text((150, 430), "• Cannot recall if a title tag was changed last month", fill=TEXT_MUT, font=F_BODY)
    d6.text((150, 480), "• Repeats recommendations that already failed in past A/B tests", fill=TEXT_MUT, font=F_BODY)
    d6.text((150, 530), "• Treats every user question as an isolated event", fill=TEXT_MUT, font=F_BODY)
    d6.text((150, 580), "• No ability to connect algorithm changes to site modifications", fill=TEXT_MUT, font=F_BODY)
    d6.rounded_rectangle([(150, 740), (500, 790)], radius=8, fill=(35, 15, 15), outline=(100, 40, 40))
    d6.text((180, 755), "RESULT: FRAGMENTED & REPETITIVE", fill=(255, 120, 120), font=F_TAG)
    card(d6, 960, 220, 840, 670, t="THE OPENSITE ADVANTAGE: HINDSIGHT", sub="Continuous compounding intelligence", border=(72, 93, 46))
    d6.line([(960, 230), (1800, 230)], fill=LIME, width=3)
    d6.text((990, 320), "OpenSite maintains a persistent site memory bank:", fill=WHITE, font=F_BOLD)
    d6.text((990, 380), "• Retains audit snapshots, technical fixes, and ranking shifts", fill=LIME, font=F_BODY)
    d6.text((990, 430), "• Remembers hypotheses, tested variants, and measured ARR lift", fill=LIME, font=F_BODY)
    d6.text((990, 480), "• Recalls past evidence before generating new recommendations", fill=LIME, font=F_BODY)
    d6.text((990, 530), "• Contextualizes Google Core Updates against your past changes", fill=LIME, font=F_BODY)
    d6.text((990, 580), "• Builds an enduring knowledge base unique to your domain", fill=LIME, font=F_BODY)
    d6.rounded_rectangle([(990, 740), (1450, 790)], radius=8, fill=(24, 32, 15), outline=(72, 93, 46))
    d6.text((1020, 755), "RESULT: EVIDENCE-BACKED COMPOUNDING GROWTH", fill=LIME, font=F_TAG)
    teleprompter(d6, "But what makes OpenSite different is its focus on persistent intelligence. It doesn't just analyze what is happening today. It is designed to remember relevant previous analyses and use that information when generating future recommendations.")
    img6.save(os.path.join(FRAMES_DIR, "frame_06.png"))
    print("Rendered Scenes 1 to 3 (frames 01 to 06).")

if __name__ == "__main__":
    render_scenes_1_to_3()
