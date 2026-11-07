from app.hindsight_manager import hindsight_mgr

SEED_SITES = [
    {
        "site_id": "opensite_io",
        "domain": "opensite.io",
        "title": "Opensite Developer Platform",
        "niche": "B2B SaaS Developer Infrastructure & API Tools",
        "baseline_monthly_organic": 42000,
        "baseline_conversion_rate": "2.4%",
        "history": [
            {
                "date": "2026-08-14T09:00:00Z",
                "category": "algorithm_update",
                "title": "Google August Core Update Rollout",
                "content": (
                    "Google rolled out the August Core Update. opensite.io observed a 14% drop in impressions across "
                    "generic programmatic glossary pages (/glossary/*). Google's quality raters prioritized in-depth, original "
                    "benchmarks over surface-level keyword definitions. Action taken: Deprecated 35 thin definition pages "
                    "and merged them into 4 comprehensive engineering deep-dives."
                ),
                "tags": ["algorithm:google_august_core", "rankings", "thin_content", "seo_penalty"],
                "metadata": {"type": "Algorithm Event", "impact": "-14% impressions on glossary"}
            },
            {
                "date": "2026-09-02T11:30:00Z",
                "category": "ab_test",
                "title": "Experiment #EXP-201: /pricing Headline & Default Billing Toggle",
                "content": (
                    "A/B Test on /pricing: Tested Variant A (Monthly billing default, headline: 'Flexible Pricing for Modern Teams') "
                    "vs Variant B (Annual billing default with 'Save 20%' badge, headline: 'Production-Ready Pricing'). "
                    "Result: Variant B increased Net ARR per signup by 31%, but raw visitor-to-signup conversion dropped by 12% "
                    "due to friction for indie developers. Key insight: Developer audience strongly resisted forced annual default. "
                    "Winning resolution: Kept monthly default with a prominent 20% annual savings callout pill."
                ),
                "tags": ["ab_test:exp_201", "cro", "pricing_page", "conversion_lift", "friction"],
                "metadata": {"type": "A/B Test", "outcome": "+31% ARR / -12% indie signup friction"}
            },
            {
                "date": "2026-09-20T15:00:00Z",
                "category": "content_experiment",
                "title": "Experiment #EXP-204: Interactive Architecture Diagrams & Code Snippets",
                "content": (
                    "Tested adding interactive executable code sandboxes and Mermaid architectural diagrams to technical blog posts "
                    "(e.g., /blog/event-driven-microservices and /docs/quickstart). "
                    "Outcome: Average session duration surged from 1m 45s to 4m 12s. Search position for 'event driven microservices architecture' "
                    "leaped from Rank #18 to Rank #3 on Google US within 2 weeks. Organic CTR increased by 48%."
                ),
                "tags": ["content_experiment", "rankings", "dwell_time", "code_snippets", "rank_boost"],
                "metadata": {"type": "Content Test", "outcome": "Rank #18 -> #3, +48% CTR"}
            },
            {
                "date": "2026-10-08T10:15:00Z",
                "category": "cro_experiment",
                "title": "Experiment #EXP-210: Hero Section CTA on /signup",
                "content": (
                    "Tested three hero CTA variants on /signup landing page: "
                    "A: 'Start Your Free 14-Day Trial' (baseline, 2.8% conversion) "
                    "B: 'Get Started with Google OAuth' (one-click, 3.9% conversion) "
                    "C: 'Deploy with 1-Click (No Credit Card Required)' (winner, 4.7% conversion). "
                    "Winner: Variant C delivered a +67.8% relative conversion lift. Developer friction dropped immediately "
                    "when credit card requirement was explicitly dispelled above the fold."
                ),
                "tags": ["ab_test:exp_210", "cro", "signup_page", "cta_optimization", "conversion_winner"],
                "metadata": {"type": "A/B Test", "outcome": "+67.8% conversion lift to 4.7%"}
            },
            {
                "date": "2026-10-25T13:45:00Z",
                "category": "algorithm_update",
                "title": "Google October Spam & Helpful Content Refresh",
                "content": (
                    "Google refreshed its Helpful Content classifier. Competitor site 'DevStackMetrics' lost 40% organic traffic "
                    "due to automated AI-generated listicles. opensite.io traffic grew +22% because of our authentic customer case studies "
                    "and verifiable author bios with schema markup (Person + Organization json-ld). "
                    "Takeaway: Google rewards first-party telemetry data and verified author schemas; strictly avoid generic AI listicles."
                ),
                "tags": ["algorithm:helpful_content", "rankings", "eeat", "competitor_traffic", "schema_org"],
                "metadata": {"type": "Algorithm Event", "impact": "+22% organic traffic surge"}
            },
            {
                "date": "2026-11-01T08:30:00Z",
                "category": "technical_seo",
                "title": "Core Web Vitals & INP (Interaction to Next Paint) Optimization",
                "content": (
                    "Resolved INP latency degradation on mobile devices caused by heavy third-party tracking scripts (Hotjar + Intercom). "
                    "Deferred non-critical JS to requestIdleCallback. INP dropped from 290ms (Poor) to 48ms (Good). "
                    "Mobile organic impressions climbed 16% over the following 7 days."
                ),
                "tags": ["technical_seo", "core_web_vitals", "inp", "mobile_traffic", "page_speed"],
                "metadata": {"type": "Technical SEO", "impact": "INP 290ms -> 48ms (+16% mobile traffic)"}
            }
        ]
    },
    {
        "site_id": "saasmetrics_dev",
        "domain": "saasmetrics.dev",
        "title": "SaaS Metrics & Revenue Analytics",
        "niche": "B2B Subscription Analytics",
        "baseline_monthly_organic": 28000,
        "baseline_conversion_rate": "1.9%",
        "history": [
            {
                "date": "2026-09-12T10:00:00Z",
                "category": "ab_test",
                "title": "Interactive Free Calculator Lead Magnet",
                "content": (
                    "Launched free SaaS Rule of 40 & Churn Calculator on /tools/rule-of-40. "
                    "Generated 3,200 monthly organic visits and converted 6.2% of visitors to newsletter and product signups. "
                    "Ranked #1 for 'rule of 40 calculator' within 30 days."
                ),
                "tags": ["lead_magnet", "interactive_tool", "rank_1", "cro"],
                "metadata": {"type": "Lead Magnet", "outcome": "Rank #1, 6.2% conversion"}
            },
            {
                "date": "2026-10-15T14:00:00Z",
                "category": "cro_experiment",
                "title": "Gated vs Ungated Benchmark Reports",
                "content": (
                    "Tested gating the 2026 SaaS Retention Benchmark Report behind email capture vs ungated with embedded CTAs. "
                    "Result: Ungated report with embedded contextual upgrade triggers drove 3.4x more product demo requests "
                    "than strict email gating, while also acquiring 45 high-authority backlinks from TechCrunch and Substack."
                ),
                "tags": ["cro", "backlinks", "ungated_content", "product_led_growth"],
                "metadata": {"type": "Content Strategy", "outcome": "3.4x demo requests, 45 backlinks"}
            }
        ]
    }
]

def seed_seo_memories() -> int:
    """Populates Hindsight memory banks with historical SEO, ranking, A/B test, and algorithm data."""
    count = 0
    for site in SEED_SITES:
        bank_id = site["site_id"]
        # Keep seeding idempotent when the app restarts or a new demo site is added.
        if hindsight_mgr.get_bank_memories(bank_id):
            continue
        # Seed Site Profile
        hindsight_mgr.retain(
            bank_id=bank_id,
            content=(
                f"Site Profile for {site['domain']}: Title: {site['title']}. Niche: {site['niche']}. "
                f"Baseline Monthly Organic Traffic: {site['baseline_monthly_organic']:,}. "
                f"Baseline Visitor-to-Lead Conversion Rate: {site['baseline_conversion_rate']}."
            ),
            tags=["profile", "domain_overview", "baseline"],
            metadata={"domain": site["domain"], "niche": site["niche"]}
        )
        count += 1
        
        # Seed historical events
        for item in site["history"]:
            hindsight_mgr.retain(
                bank_id=bank_id,
                content=f"[{item['category'].upper()}] {item['title']} (Date: {item['date']}): {item['content']}",
                timestamp=item["date"],
                tags=item["tags"],
                metadata=item["metadata"]
            )
            count += 1
            
    return count
