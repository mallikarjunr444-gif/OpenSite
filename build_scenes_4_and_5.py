import os
from PIL import Image, ImageDraw
from build_video_part1 import (
    FRAMES_DIR, BG, PANEL, PANEL_HI, LINE, LIME, WHITE, MUTED, CARD, HOVER, TEXT_MUT, CYAN,
    F_TITLE, F_HERO, F_SUB, F_BODY, F_BOLD, F_METRIC, F_TAG, F_NARR, F_CODE,
    header, teleprompter, card
)

def render_scenes_4_and_5():
    # Frame 07 (Scene 4: 1:45 - 2:05)
    img7 = Image.new("RGB", (1920, 1080), BG)
    d7 = ImageDraw.Draw(img7)
    header(d7, 4, "OpenSite Features", "1:45–2:05")
    d7.text((120, 110), "The 12 Core Capabilities", fill=WHITE, font=F_TITLE)
    d7.text((120, 165), "A comprehensive suite covering every vector of organic visibility and conversion optimization.", fill=MUTED, font=F_SUB)
    feats = [
        ("01", "AI Growth Agent", "Synthesizes multi-source telemetry and directs next growth priorities."),
        ("02", "SEO Intelligence", "Analyzes organic search performance and uncovers ranking gaps."),
        ("03", "Keyword Intelligence", "Tracks Search Console queries, positions, impressions, and CTR."),
        ("04", "Technical Website Audit", "Crawls public pages, validates canonicals, robots.txt, and meta tags."),
        ("05", "Content Intelligence", "Evaluates depth, EEAT signals, author schemas, and dwell time."),
        ("06", "Competitor Intelligence", "Benchmarks public competitor domains, SERP shifts, and content."),
        ("07", "Conversion Intelligence", "Measures visitor funnels, lead form dropoffs, and landing page CTR."),
        ("08", "A/B Experiment Intelligence", "Logs hypotheses, test variants, and statistically verified outcomes."),
        ("09", "Local SEO & Maps", "Geographic search context and local ranking visibility signals."),
        ("10", "Historical Memory", "Durable site memory bank storing past tests and performance shifts."),
        ("11", "Algorithm Monitoring", "Live Google Search Central RSS feed correlation and update alerts."),
        ("12", "Growth Recommendations", "Evidence-grounded action plans synthesized by the AI advisor.")
    ]
    gx, gy = 120, 230
    for i, (num, name, desc) in enumerate(feats):
        x = gx + (i % 3) * 565
        y = gy + (i // 3) * 160
        card(d7, x, y, 545, 145, border=HOVER)
        d7.text((x + 20, y + 16), num, fill=LIME, font=F_BOLD)
        d7.text((x + 60, y + 16), name, fill=WHITE, font=F_BOLD)
        d7.text((x + 20, y + 55), desc, fill=TEXT_MUT, font=F_TAG)
    teleprompter(d7, "Let's explore the major capabilities of OpenSite. First, SEO Intelligence. Second, Keyword Intelligence. Third, Website Audit. Fourth, Content Intelligence. Fifth, Competitor Intelligence. Sixth, Conversion Intelligence. Seventh, Local SEO and Maps. And finally, the AI Growth Agent connects these capabilities.")
    img7.save(os.path.join(FRAMES_DIR, "frame_07.png"))

    # Frame 08 (Scene 4: 2:05 - 2:25)
    img8 = Image.new("RGB", (1920, 1080), BG)
    d8 = ImageDraw.Draw(img8)
    header(d8, 4, "OpenSite Features", "2:05–2:25")
    d8.text((120, 110), "Technical Audit & Keyword Intelligence", fill=WHITE, font=F_TITLE)
    d8.text((120, 165), "Real-time crawler + Google Search Console query performance integration.", fill=MUTED, font=F_SUB)
    card(d8, 120, 220, 800, 680, t="PAGE CRAWLER & SITE HEALTH AUDITOR", sub="Real-time same-host crawler respecting robots.txt")
    d8.text((150, 310), "Target Host: https://opensite.io", fill=WHITE, font=F_BOLD)
    cx = 150
    for lbl, val in [("PAGES CRAWLED", "30 Pages"), ("CRITICAL ERRORS", "0 Errors"), ("WARNINGS", "3 Warnings"), ("INFO NOTICES", "7 Notices")]:
        d8.rounded_rectangle([(cx, 360), (cx + 170, 430)], radius=6, fill=PANEL, outline=LINE)
        d8.text((cx + 12, 372), lbl, fill=MUTED, font=F_TAG)
        d8.text((cx + 12, 395), val, fill=WHITE if "0" in val or "30" in val else LIME, font=F_BOLD)
        cx += 185
    d8.text((150, 460), "Prioritized Audit Findings:", fill=WHITE, font=F_BOLD)
    fy = 500
    for sev, url, desc in [("Warning", "/glossary/api-gateway", "Missing meta description tag (H1 present)"), ("Warning", "/docs/quickstart", "Title exceeds 60 characters (68 chars)"), ("Info", "/pricing", "Image missing alt attribute (hero_graphic.svg)")]:
        d8.rounded_rectangle([(150, fy), (880, fy + 55)], radius=6, fill=PANEL, outline=LINE)
        d8.text((170, fy + 16), sev, fill=(255, 180, 80) if sev=="Warning" else CYAN, font=F_TAG)
        d8.text((260, fy + 16), url, fill=WHITE, font=F_CODE)
        d8.text((500, fy + 16), desc, fill=TEXT_MUT, font=F_TAG)
        fy += 65
    d8.rounded_rectangle([(150, 750), (880, 820)], radius=8, fill=(24, 32, 15), outline=(72, 93, 46))
    d8.text((170, 775), "SNAPSHOT AUTOMATICALLY RETAINED TO HINDSIGHT FOR TEMPORAL COMPARISON", fill=LIME, font=F_TAG)
    card(d8, 960, 220, 840, 680, t="SEARCH CONSOLE KEYWORD RANKINGS", sub="Query metrics: clicks, impressions, CTR, and average position")
    kw_data = [
        ("Query", "Clicks", "Impressions", "CTR", "Position"),
        ("event driven microservices", "1,840", "12,400", "14.8%", "#3.2"),
        ("rule of 40 calculator", "3,200", "18,900", "16.9%", "#1.1"),
        ("microservices architecture diagram", "920", "8,100", "11.3%", "#4.5"),
        ("saas pricing models", "640", "5,400", "11.8%", "#5.8"),
        ("developer platform tools", "410", "4,200", "9.7%", "#7.4")
    ]
    ky = 310
    for idx, row in enumerate(kw_data):
        bg = PANEL_HI if idx == 0 else PANEL
        d8.rectangle([(990, ky), (1770, ky + 45)], fill=bg, outline=LINE)
        d8.text((1010, ky + 13), row[0], fill=LIME if idx == 0 else WHITE, font=F_BOLD if idx == 0 else F_CODE)
        d8.text((1350, ky + 13), row[1], fill=LIME if idx == 0 else WHITE, font=F_BOLD if idx == 0 else F_CODE)
        d8.text((1460, ky + 13), row[2], fill=LIME if idx == 0 else TEXT_MUT, font=F_BOLD if idx == 0 else F_CODE)
        d8.text((1580, ky + 13), row[3], fill=LIME if idx == 0 else TEXT_MUT, font=F_BOLD if idx == 0 else F_CODE)
        d8.text((1680, ky + 13), row[4], fill=LIME if idx == 0 else CYAN, font=F_BOLD if idx == 0 else F_CODE)
        ky += 55
    d8.rounded_rectangle([(990, 750), (1770, 820)], radius=8, fill=PANEL, outline=HOVER)
    d8.text((1010, 775), "Live Search Console OAuth integration provides continuous 28-day query trends.", fill=TEXT_MUT, font=F_TAG)
    teleprompter(d8, "First, SEO Intelligence analyzes search performance and identifies opportunities. Second, Keyword Intelligence monitors ranking changes. Third, Website Audit identifies technical issues, broken links, and metadata opportunities.")
    img8.save(os.path.join(FRAMES_DIR, "frame_08.png"))

    # Frame 09 (Scene 4: 2:25 - 2:45)
    img9 = Image.new("RGB", (1920, 1080), BG)
    d9 = ImageDraw.Draw(img9)
    header(d9, 4, "OpenSite Features", "2:25–2:45")
    d9.text((120, 110), "Conversion & Experiment Intelligence", fill=WHITE, font=F_TITLE)
    d9.text((120, 165), "Tracking hypotheses, variants, measured ARR lift, and friction lessons.", fill=MUTED, font=F_SUB)
    card(d9, 120, 220, 1680, 680, t="A/B EXPERIMENT TIMELINE & CRO LEARNING LOOP", sub="Connecting what was changed to measured conversion impact")
    experiments_display = [
        ("EXP-210", "Hero Section CTA on /signup", "Tested 3 CTA variants. Dispelled credit card friction above fold.", "+67.8% Conversion Lift (2.8% → 4.7%)", "WINNER"),
        ("EXP-201", "Pricing Headline & Default Billing Toggle", "Tested monthly vs annual default. Devs resisted forced annual.", "+31% Net ARR (Kept monthly default with 20% pill)", "WINNER"),
        ("EXP-204", "Interactive Diagrams & Code Sandboxes", "Added executable sandboxes to technical blog posts.", "Dwell Time 1m45s → 4m12s | Rank #18 → #3", "WINNER")
    ]
    ex_y = 320
    for code, title, details, outcome, badge in experiments_display:
        card(d9, 160, ex_y, 1600, 145, border=HOVER)
        d9.rounded_rectangle([(180, ex_y + 20), (270, ex_y + 55)], radius=6, fill=PANEL, outline=LINE)
        d9.text((195, ex_y + 28), code, fill=LIME, font=F_BOLD)
        d9.text((290, ex_y + 25), title, fill=WHITE, font=F_BOLD)
        d9.text((290, ex_y + 65), details, fill=TEXT_MUT, font=F_BODY)
        d9.text((290, ex_y + 100), outcome, fill=LIME, font=F_BOLD)
        d9.rounded_rectangle([(1570, ex_y + 20), (1730, ex_y + 60)], radius=20, fill=(24, 32, 15), outline=(72, 93, 46))
        d9.text((1600, ex_y + 30), badge, fill=LIME, font=F_TAG)
        ex_y += 175
    teleprompter(d9, "Sixth, Conversion Intelligence helps understand visitor behaviour, conversion performance and landing page effectiveness. Finally, the AI Growth Agent connects these capabilities and turns available data into useful recommendations.")
    img9.save(os.path.join(FRAMES_DIR, "frame_09.png"))

    # Frame 10 (Scene 5: 2:45 - 3:00)
    img10 = Image.new("RGB", (1920, 1080), BG)
    d10 = ImageDraw.Draw(img10)
    header(d10, 5, "Hindsight Integration", "2:45–3:00")
    d10.text((120, 110), "Hindsight: The Intelligence Behind OpenSite", fill=WHITE, font=F_TITLE)
    d10.text((120, 165), "Persistent AI memory giving the Growth Agent the power to retain and recall across sessions.", fill=MUTED, font=F_SUB)
    card(d10, 120, 220, 1680, 680, t="HINDSIGHT DUAL-TIER MEMORY ARCHITECTURE", sub="Local-first durable storage with optional Hindsight Cloud synchronization")
    card(d10, 160, 320, 460, 520, t="OPENSITE AGENT", sub="Generates observations & queries")
    d10.text((190, 410), "1. Audit snapshots", fill=WHITE, font=F_BODY)
    d10.text((190, 460), "2. Title & metadata changes", fill=WHITE, font=F_BODY)
    d10.text((190, 510), "3. A/B test hypotheses & ARR", fill=WHITE, font=F_BODY)
    d10.text((190, 560), "4. Ranking position deltas", fill=WHITE, font=F_BODY)
    d10.text((190, 610), "5. Google Core Update impacts", fill=WHITE, font=F_BODY)
    d10.rounded_rectangle([(190, 730), (580, 780)], radius=6, fill=PANEL, outline=LINE)
    d10.text((210, 745), "Autonomous Growth Loop", fill=CYAN, font=F_TAG)

    card(d10, 680, 320, 560, 520, t="HINDSIGHT CLIENT INTEGRATION", sub="app/hindsight_manager.py", border=(72, 93, 46))
    d10.line([(680, 320), (1240, 320)], fill=LIME, width=3)
    d10.text((710, 410), "from hindsight_client import Hindsight", fill=LIME, font=F_CODE)
    d10.text((710, 460), "• retain(bank_id, content, tags, metadata)", fill=WHITE, font=F_CODE)
    d10.text((710, 500), "  Stores structured observation into bank", fill=MUTED, font=F_TAG)
    d10.text((710, 550), "• recall(bank_id, query, tags, limit)", fill=WHITE, font=F_CODE)
    d10.text((710, 590), "  Retrieves top matching memories", fill=MUTED, font=F_TAG)
    d10.text((710, 640), "• reflect(bank_id, query)", fill=WHITE, font=F_CODE)
    d10.text((710, 680), "  Synthesizes historical lessons into advice", fill=MUTED, font=F_TAG)
    d10.rounded_rectangle([(710, 750), (1210, 800)], radius=6, fill=(24, 32, 15), outline=(72, 93, 46))
    d10.text((730, 765), "Dual-Tier: Local JSON + Cloud API Mirroring", fill=LIME, font=F_TAG)

    card(d10, 1300, 320, 460, 520, t="DURABLE MEMORY BANKS", sub="Isolated per website domain")
    d10.text((1330, 410), "Bank: 'opensite_io'", fill=WHITE, font=F_BOLD)
    d10.text((1330, 450), "• Site Profile Baseline", fill=TEXT_MUT, font=F_BODY)
    d10.text((1330, 490), "• 6 Historical Milestones", fill=TEXT_MUT, font=F_BODY)
    d10.text((1330, 530), "• 4 Live Experiment Records", fill=TEXT_MUT, font=F_BODY)
    d10.text((1330, 570), "• Live Search Console Imports", fill=TEXT_MUT, font=F_BODY)
    d10.text((1330, 610), "• Core Update Corroborations", fill=TEXT_MUT, font=F_BODY)
    d10.rounded_rectangle([(1330, 730), (1720, 780)], radius=6, fill=PANEL, outline=LINE)
    d10.text((1350, 745), "Persistent Across Restarts", fill=CYAN, font=F_TAG)
    teleprompter(d10, "Now comes one of the most important parts of OpenSite: persistent AI memory. We use Hindsight to give our AI agent the ability to retain and recall relevant information from previous interactions.")
    img10.save(os.path.join(FRAMES_DIR, "frame_10.png"))

    # Frame 11 (Scene 5: 3:00 - 3:20)
    img11 = Image.new("RGB", (1920, 1080), BG)
    d11 = ImageDraw.Draw(img11)
    header(d11, 5, "Live Demo: Retain", "3:00–3:20")
    d11.text((120, 110), "Live Demonstration: Retain Operation", fill=WHITE, font=F_TITLE)
    d11.text((120, 165), "OpenSite analyzes a website and retains recommendations into Hindsight persistent memory.", fill=MUTED, font=F_SUB)
    card(d11, 120, 220, 800, 680, t="STEP 1: RETAINING RECOMMENDATION", sub="Actual Hindsight Python SDK Execution", border=(72, 93, 46))
    d11.line([(120, 220), (920, 220)], fill=LIME, width=3)
    code_block = [
        "# OpenSite agent executes Hindsight retain()",
        "hindsight_mgr.retain(",
        '    bank_id="opensite_io",',
        '    content="""[SEO RECOMMENDATION] Optimize page title',
        '    for /pricing to include high-intent keyword',
        '    \'Developer Infrastructure Pricing\'. Expected',
        '    ranking boost: Rank #8 -> Top 5.""",',
        '    tags=["seo", "title_optimization", "pricing_page"],',
        '    metadata={',
        '        "type": "Recommendation",',
        '        "action": "title_tag_rewrite",',
        '        "target_url": "/pricing",',
        '        "suggested_title": "Developer Infrastructure Pricing | OpenSite"',
        '    }',
        ")"
    ]
    cy = 310
    for line in code_block:
        color = MUTED if line.startswith("#") else (LIME if "hindsight_mgr" in line else WHITE)
        d11.text((150, cy), line, fill=color, font=F_CODE)
        cy += 32
    d11.rounded_rectangle([(150, 770), (880, 830)], radius=8, fill=(24, 32, 15), outline=(72, 93, 46))
    d11.text((170, 792), "✔ STATUS: Retained into bank 'opensite_io' with id 'mem_7a8f9b2c'", fill=LIME, font=F_TAG)
    card(d11, 960, 220, 840, 680, t="OPENSITE UI · MEMORY BANK CAPTURE", sub="Observation logged to durable memory stream")
    d11.rounded_rectangle([(990, 310), (1770, 510)], radius=10, fill=PANEL, outline=HOVER)
    d11.text((1010, 330), "2026-11-07 · RECOMMENDATION · OPENSITE AI", fill=MUTED, font=F_TAG)
    d11.text((1010, 365), "Title Tag Optimization on /pricing", fill=WHITE, font=F_BOLD)
    d11.text((1010, 405), "OpenSite recommended optimizing the page title of /pricing to include\nhigh-intent keyword 'Developer Infrastructure Pricing'.\nTarget: Improve SERP CTR and rank position.", fill=TEXT_MUT, font=F_BODY)
    tags = ["seo", "title_optimization", "pricing_page", "ai_recommendation"]
    tx = 1010
    for t in tags:
        d11.rounded_rectangle([(tx, 460), (tx + len(t)*10 + 20, 490)], radius=15, fill=(18, 24, 15), outline=(72, 93, 46))
        d11.text((tx + 10, 468), t, fill=LIME, font=F_TAG)
        tx += len(t)*10 + 30
    d11.rounded_rectangle([(990, 550), (1770, 810)], radius=10, fill=PANEL, outline=LINE)
    d11.text((1010, 570), "LIVE TELEMETRY SUMMARY", fill=LIME, font=F_TAG)
    d11.text((1010, 610), "• Memory Bank: opensite_io (Active)", fill=WHITE, font=F_CODE)
    d11.text((1010, 650), "• Stored Vector: Semantic keywords extracted", fill=WHITE, font=F_CODE)
    d11.text((1010, 690), "• Status: Ready for future recall when user inquires", fill=CYAN, font=F_CODE)
    d11.text((1010, 730), "• Durable across container restarts and sessions", fill=TEXT_MUT, font=F_CODE)
    teleprompter(d11, "For example, imagine OpenSite analyzes a website and recommends improving its page title. The agent can retain information about that analysis and recommendation. Let's demonstrate this retain operation.")
    img11.save(os.path.join(FRAMES_DIR, "frame_11.png"))

    # Frame 12 (Scene 5: 3:20 - 3:45)
    img12 = Image.new("RGB", (1920, 1080), BG)
    d12 = ImageDraw.Draw(img12)
    header(d12, 5, "Live Demo: Recall", "3:20–3:45")
    d12.text((120, 110), "Live Demonstration: Recall Operation", fill=WHITE, font=F_TITLE)
    d12.text((120, 165), "Querying previously retained recommendations to answer follow-up growth questions.", fill=MUTED, font=F_SUB)
    card(d12, 120, 220, 800, 680, t="STEP 2: RECALLING FROM HINDSIGHT", sub="Actual Hindsight Python SDK Execution", border=(72, 93, 46))
    d12.line([(120, 220), (920, 220)], fill=LIME, width=3)
    code_recall = [
        "# Later, user or agent queries site memory bank",
        "memories = hindsight_mgr.recall(",
        '    bank_id="opensite_io",',
        '    query="What improvements were previously suggested',
        '           for the pricing page title?",',
        '    limit=5',
        ")",
        "",
        "# Synthesizing evidence into growth advice",
        "advice = advise(query, memories)",
        "print(advice['answer'])"
    ]
    cy = 310
    for line in code_recall:
        color = MUTED if line.startswith("#") else (LIME if "hindsight_mgr" in line else WHITE)
        d12.text((150, cy), line, fill=color, font=F_CODE)
        cy += 32
    d12.rounded_rectangle([(150, 770), (880, 830)], radius=8, fill=(24, 32, 15), outline=(72, 93, 46))
    d12.text((170, 792), "✔ STATUS: Recall returned 3 matching memories (Score: 7.2)", fill=LIME, font=F_TAG)
    card(d12, 960, 220, 840, 680, t="OPENSITE UI · AGENT RESPONSE", sub="Evidence-based answer generated from recalled memories")
    d12.rounded_rectangle([(990, 310), (1770, 390)], radius=8, fill=PANEL, outline=LINE)
    d12.text((1010, 325), "USER QUESTION", fill=MUTED, font=F_TAG)
    d12.text((1010, 350), '"What improvements were previously suggested for our pricing page?"', fill=WHITE, font=F_BOLD)
    d12.rounded_rectangle([(990, 410), (1770, 720)], radius=10, fill=PANEL_HI, outline=HOVER)
    d12.line([(990, 410), (990, 720)], fill=LIME, width=4)
    d12.text((1020, 435), "OPENSITE GROWTH AGENT (MEMORY-BACKED SYNTHESIS)", fill=LIME, font=F_TAG)
    ans_text = (
        "Based on recalled site memories, OpenSite previously recommended:\n\n"
        "1. Title Tag Optimization: Recommended optimizing /pricing page title to\n"
        "   'Developer Infrastructure Pricing | OpenSite' to capture high-intent queries.\n\n"
        "2. Related Historical Finding (EXP-201): Keep monthly billing default with\n"
        "   a 20% annual discount callout pill to avoid developer signup friction.\n\n"
        "Next Recommended Action: Update the <title> tag and monitor impressions."
    )
    ay = 475
    for line in ans_text.split("\n"):
        d12.text((1020, ay), line, fill=WHITE if line.startswith("1.") or line.startswith("2.") else TEXT_MUT, font=F_CODE)
        ay += 26
    d12.rounded_rectangle([(990, 750), (1770, 810)], radius=8, fill=(24, 32, 15), outline=(72, 93, 46))
    d12.text((1010, 772), "CLOSED-LOOP VERIFICATION: AGENT USES PAST HISTORY TO ANSWER FOLLOW-UPS", fill=LIME, font=F_TAG)
    teleprompter(d12, "Now let's perform a recall operation. As you can see, the agent can use previously retained information to answer a follow-up question. This allows OpenSite to build on previous interactions instead of treating every analysis as an isolated task.")
    img12.save(os.path.join(FRAMES_DIR, "frame_12.png"))

    # Frame 13 (Scene 5: 3:40 - 3:45)
    img13 = Image.new("RGB", (1920, 1080), BG)
    d13 = ImageDraw.Draw(img13)
    header(d13, 5, "Hindsight Advantage", "3:40–3:45")
    d13.text((120, 110), "Why Hindsight Transforms OpenSite", fill=WHITE, font=F_TITLE)
    d13.text((120, 165), "Eliminating the memory gap in autonomous marketing & SEO agents.", fill=MUTED, font=F_SUB)
    card(d13, 120, 220, 1680, 680, t="PERSISTENT MEMORY AS A COMPETITIVE ADVANTAGE", sub="From Ephemeral Prompts to Durable Site Intelligence")
    px = 160
    for title, copy in [
        ("NO REPEATED MISTAKES", "If an A/B test showed that forced annual billing drops signups by 12%, OpenSite retains that lesson forever and never recommends forced annual billing again."),
        ("TEMPORAL ATTRIBUTION", "When a search ranking shifts after an algorithm update, OpenSite correlates the change with specific technical deployments made in the preceding 30 days."),
        ("CONTINUOUS COMPOUNDING", "Every crawl, query report, and CRO experiment enriches the Hindsight memory bank, making future growth recommendations progressively more accurate.")
    ]:
        card(d13, px, 320, 480, 510, t=title, border=(72, 93, 46))
        d13.line([(px, 320), (px + 480, 320)], fill=LIME, width=3)
        words = copy.split(" ")
        cur, l_list = "", []
        for w in words:
            if len(cur + " " + w) < 32: cur += (" " if cur else "") + w
            else: l_list.append(cur); cur = w
        if cur: l_list.append(cur)
        py = 420
        for l in l_list:
            d13.text((px + 24, py), l, fill=TEXT_MUT, font=F_BODY)
            py += 36
        px += 540
    teleprompter(d13, "This allows OpenSite to build on previous interactions instead of treating every analysis as an isolated task. Hindsight makes OpenSite truly continuous.")
    img13.save(os.path.join(FRAMES_DIR, "frame_13.png"))
    print("Rendered Scenes 4 and 5 (frames 07 to 13).")

if __name__ == "__main__":
    render_scenes_4_and_5()
