"""OpenSite growth intelligence workspace."""
import html
import hmac
import os
from datetime import datetime

import pandas as pd
import streamlit as st

from app.hindsight_manager import hindsight_mgr
from app import integrations
from app.site_auditor import crawl_site
from app.site_registry import add_site, load_custom_sites
from app.growth_agent import advise
from app.seed_seo_data import SEED_SITES, seed_seo_memories


st.set_page_config(page_title="OpenSite | Growth intelligence", page_icon="◉", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root{--white:#f4f4f1;--muted:#85867f;--line:#282923;--panel:#12130f;--lime:#d5ff82;--black:#090a08;--panel-hi:#171812}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:var(--black);color:var(--white)}
section[data-testid="stSidebar"]{background:#10110e;border-right:1px solid #22231e}section[data-testid="stSidebar"] *{color:var(--white)}
.block-container{padding-top:1.7rem;max-width:1420px}h1,h2,h3{color:var(--white);letter-spacing:-.045em}
.stApp header{background:rgba(9,10,8,.8)}
.stApp [data-testid="stVerticalBlock"]{gap:.8rem}
.stApp [data-testid="stHorizontalBlock"]{gap:1rem}
.brand{font-weight:800;letter-spacing:-.085em;font-size:29px;line-height:1;color:#fafaf8;margin:4px 0}.brand span{color:#85867f}
.eyebrow{font:500 10px 'DM Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.page-title{font-size:35px;font-weight:700;letter-spacing:-.06em;margin:2px 0 4px}.subtle{color:var(--muted);font-size:13px}
.card{background:linear-gradient(145deg,#151610 0%,#10110e 74%);border:1px solid var(--line);border-radius:15px;padding:19px 20px;height:100%;box-shadow:0 12px 28px rgba(0,0,0,.12);transition:transform .18s ease,border-color .18s ease,background .18s ease}
.card:hover{transform:translateY(-2px);border-color:#43463a;background:linear-gradient(145deg,#191b13 0%,#11120f 74%)}
.metric-label{font:500 10px 'DM Mono',monospace;letter-spacing:.12em;color:var(--muted);text-transform:uppercase}
.metric-value{font-size:29px;letter-spacing:-.05em;font-weight:700;margin:7px 0 2px}.metric-delta{color:var(--lime);font-size:12px}
.section-title{font-size:18px;font-weight:700;letter-spacing:-.035em;margin:0 0 4px}
.tag{display:inline-block;padding:4px 8px;border:1px solid #33352d;border-radius:99px;color:#c6c8bb;font:10px 'DM Mono',monospace;margin:2px 4px 2px 0}
.tag-lime{border-color:#485d2e;color:var(--lime);background:#18200f}.event-title{font-size:14px;font-weight:600;margin-bottom:4px}
.event-meta{color:var(--muted);font:10px 'DM Mono',monospace;margin-bottom:7px}.event-copy{color:#b4b5ad;font-size:12px;line-height:1.6}
.insight{border-left:2px solid var(--lime);padding:2px 0 2px 14px;color:#d9dacd;font-size:13px;line-height:1.6;margin:12px 0}
.divider{border-top:1px solid var(--line);margin:15px 0}
div[data-testid="stMetric"]{background:linear-gradient(145deg,#171812 0%,#11120f 100%);padding:17px 18px;border:1px solid var(--line);border-radius:14px;box-shadow:0 10px 24px rgba(0,0,0,.12);transition:transform .18s ease,border-color .18s ease}
div[data-testid="stMetric"]:hover{transform:translateY(-2px);border-color:#45483c}
div[data-testid="stMetricLabel"]{color:var(--muted);font:500 10px 'DM Mono',monospace;text-transform:uppercase;letter-spacing:.11em}
div[data-testid="stMetricValue"]{color:var(--white);font-size:27px;letter-spacing:-.04em}div[data-testid="stMetricDelta"]{color:var(--lime)}
.stButton button{border-radius:9px;border:1px solid #37392f;background:#171812;color:#eff0e8;font-weight:600;transition:all .18s ease}
.stButton button:hover{border-color:var(--lime);color:var(--lime);background:#1d2115;transform:translateY(-1px)}
.stButton button[kind="primary"]{background:#e9f8d0;color:#12140e;border-color:#e9f8d0}.stButton button[kind="primary"]:hover{background:var(--lime);color:#0b0c09}
.stTextInput input,.stTextArea textarea{background:#12130f;color:var(--white);border-color:var(--line);border-radius:9px}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:#91ad61;box-shadow:0 0 0 1px #91ad61}
.stSelectbox div[data-baseweb="select"]>div{background:#12130f;border-color:var(--line)}
[data-testid="stForm"]{background:linear-gradient(145deg,#151610 0%,#10110e 74%);border:1px solid var(--line);border-radius:15px;padding:18px;box-shadow:0 12px 28px rgba(0,0,0,.12)}
[data-testid="stRadio"] label{border-radius:9px;padding:3px 5px;transition:background .15s ease}
[data-testid="stRadio"] label:hover{background:#1c1e17}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:11px;overflow:hidden}
[data-testid="stExpander"]{border:1px solid var(--line);border-radius:12px;background:#11120f}
@media(max-width:800px){.block-container{padding:1rem .8rem}.page-title{font-size:28px}.card{padding:16px}.stApp [data-testid="stHorizontalBlock"]{gap:.5rem}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;scroll-behavior:auto!important}}
</style>
""", unsafe_allow_html=True)


def require_access_password():
    expected=os.getenv("OPENSITE_ACCESS_PASSWORD","")
    if not expected or st.session_state.get("opensite_authenticated"):
        return
    st.markdown('<div style="max-width:420px;margin:12vh auto 0;text-align:center"><div class="brand" style="font-size:40px">OpenSite</div><div class="eyebrow" style="margin:10px 0 24px">SEO & conversion intelligence</div></div>',unsafe_allow_html=True)
    with st.form("opensite_access"):
        password=st.text_input("Workspace password",type="password")
        submitted=st.form_submit_button("Unlock OpenSite",type="primary",use_container_width=True)
        if submitted:
            if hmac.compare_digest(password,expected):
                st.session_state["opensite_authenticated"]=True
                st.rerun()
            else: st.error("That password was not accepted.")
    st.stop()


require_access_password()


def esc(value):
    return html.escape(str(value))


def all_memories(site_id):
    """Combine canonical sample history with durable user-recorded memories."""
    site = next((item for item in SEED_SITES if item["site_id"] == site_id), None)
    seeded = []
    if site:
        seeded = [{**event, "source": "history"} for event in site["history"]]
    extras = hindsight_mgr.get_bank_memories(site_id)
    existing = {event.get("title") for event in seeded}
    recorded = []
    for item in extras:
        content = item.get("content", "")
        if item.get("metadata", {}).get("type") == "Experiment" or "[NEW EXPERIMENT]" in content or "[RANKING UPDATE]" in content or "[ALGORITHM UPDATE]" in content:
            title = content.split(":", 1)[0].replace("[NEW EXPERIMENT]", "").replace("[RANKING UPDATE]", "").replace("[ALGORITHM UPDATE]", "").strip()
            if title not in existing:
                recorded.append({"date": item.get("timestamp", ""), "category": "experiment", "title": title or "Recorded growth signal", "content": content.split(":", 1)[-1].strip(), "tags": item.get("tags", []), "metadata": item.get("metadata", {}), "source": "memory"})
    return seeded + recorded


def add_page_header(kicker, title, description):
    st.markdown(f'<div class="eyebrow">{esc(kicker)}</div><div class="page-title">{esc(title)}</div><div class="subtle">{esc(description)}</div>', unsafe_allow_html=True)


def remember_import(site_id, provider, summary, details=None):
    """Keep a timestamped, compact snapshot so future recall can compare imports."""
    import json
    payload=json.dumps(details or {},ensure_ascii=False,sort_keys=True,default=str)
    content=f"[LIVE DATA IMPORT] {provider}: {summary}. Snapshot: {payload[:7000]}"
    hindsight_mgr.retain(site_id,content,tags=["live_data",provider.lower().replace(" ","_"),"analytics_snapshot"],metadata={"type":"Live data import","provider":provider})


if not st.session_state.get("seeded"):
    # Only seed missing sample sites, so reruns and app restarts never duplicate history.
    existing = set(hindsight_mgr.get_all_banks())
    if any(site["site_id"] not in existing for site in SEED_SITES):
        seed_seo_memories()
    st.session_state.seeded = True

sites_by_id = {site["site_id"]: site for site in SEED_SITES}
sites_by_id.update({site["site_id"]:site for site in load_custom_sites()})
with st.sidebar:
    st.markdown('<div class="brand">OpenSite</div><div class="eyebrow" style="margin:5px 0 25px">SEO & conversion intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Workspace</div>', unsafe_allow_html=True)
    page = st.radio("Navigation", ["Overview", "SEO audit", "Content intelligence", "Competitor analysis", "Keyword rankings", "Experiments", "Rankings & updates", "Memory bank", "Data connections"], label_visibility="collapsed")
    st.markdown('<div class="divider"></div><div class="eyebrow">Tracked sites</div>', unsafe_allow_html=True)
    site_id = st.selectbox("Property", list(sites_by_id), format_func=lambda key: sites_by_id[key]["domain"], label_visibility="collapsed", key="property_select")
    site = sites_by_id[site_id]
    if os.getenv("OPENSITE_ACCESS_PASSWORD") and st.button("Lock workspace",use_container_width=True):
        st.session_state["opensite_authenticated"]=False
        st.rerun()
    with st.expander("Add your website"):
        with st.form("add_property"):
            new_domain=st.text_input("Domain or URL",placeholder="example.com")
            add_property=st.form_submit_button("Add property")
            if add_property:
                try:
                    new_site_id=add_site(new_domain)
                    st.session_state["property_select"]=new_site_id
                    st.rerun()
                except ValueError as exc: st.error(str(exc))
    st.markdown('<div style="margin-top:16px"><span class="tag tag-lime">● Local memory active</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="position:fixed;bottom:20px;color:#686a61;font:10px DM Mono,monospace">OPEN SITE · GROWTH INTELLIGENCE</div>', unsafe_allow_html=True)

events = all_memories(site_id)
experiments = [item for item in events if any(word in item.get("category", "") for word in ("experiment", "ab_test", "cro"))]
updates = [item for item in events if item.get("category") in ("algorithm_update", "technical_seo", "ranking")]
site_memories = hindsight_mgr.get_bank_memories(site_id)

if page == "Overview":
    now = datetime.now().astimezone()
    st.markdown(f'<div class="eyebrow">{now.strftime("%A, %B %d, %Y").upper()} &nbsp;·&nbsp; GROWTH BRIEFING</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">Your growth, with the history to explain it.</div><div class="subtle">OpenSite connects search changes, content performance, and experiments for {esc(site["domain"])}.</div>', unsafe_allow_html=True)
    st.write("")
    wins = sum(1 for item in experiments if any(token in item["content"].lower() for token in ["winner", "increased", "generated", "surged", "drove"]))
    c1,c2,c3,c4 = st.columns(4)
    gsc_live=st.session_state.get("gsc_live")
    ga_live=st.session_state.get("ga4_live")
    plausible_live=st.session_state.get("plausible_live")
    c1.metric("Organic clicks · 28d", f'{gsc_live["clicks"]:,}' if gsc_live else f'{site["baseline_monthly_organic"]:,}', "Live Search Console" if gsc_live else "Demo baseline")
    if ga_live:
        c2.metric("GA4 conversion events · 28d", f'{ga_live["conversions"]:,.0f}', "Live Google Analytics")
    elif plausible_live:
        plausible_results=plausible_live.get("results",[])
        visitors=next((row.get(" Visitors",row.get("visitors")) for row in plausible_results if row.get("metric")=="visitors"),None)
        c2.metric("Plausible visitors", str(visitors or "Connected"), "Live Plausible")
    else:
        c2.metric("Baseline conversion", site["baseline_conversion_rate"], "Demo · visitor → lead")
    c3.metric("Growth memories", len(site_memories) if site_memories else len(site["history"])+1, "Durable signals")
    c4.metric("Positive experiments", wins, f'{len(experiments)} recorded')
    left,right = st.columns([1.35,1])
    with left:
        st.markdown('<div class="card"><div class="eyebrow">Historical evidence</div><div class="section-title">What has moved performance?</div><div class="subtle">Signals from experiments and search updates</div><div class="divider"></div>', unsafe_allow_html=True)
        if gsc_live and gsc_live.get("rows"):
            chart_rows=[{"Date":row.get("keys",[""])[0],"Clicks":row.get("clicks",0),"Impressions":row.get("impressions",0)} for row in gsc_live["rows"]]
            chart_df=pd.DataFrame(chart_rows)
            if not chart_df.empty:
                chart_df["Date"]=pd.to_datetime(chart_df["Date"])
                st.caption(f"Live Search Console · {gsc_live['range']}")
                st.line_chart(chart_df.set_index("Date")[["Clicks","Impressions"]],height=230)
        elif site["history"]:
            chart_rows=[]
            for item in sorted(site["history"],key=lambda event:event["date"]):
                outcome=item.get("metadata",{}).get("outcome") or item.get("metadata",{}).get("impact") or item["category"].replace("_"," ").title()
                chart_rows.append({"Date":pd.to_datetime(item["date"]),"Signal":item["title"][:42],"Outcome":outcome})
            chart_df=pd.DataFrame(chart_rows).set_index("Date")
            st.dataframe(chart_df, use_container_width=True, height=230, hide_index=False)
        else:
            st.info("Record your first ranking or experiment to begin a performance history.")
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        question = st.text_input("Ask OpenSite",placeholder="What patterns drove our best results?",label_visibility="collapsed",key="overview_question")
        if question:
            st.markdown('<div class="card"><div class="eyebrow">MEMORY BASED ANSWER</div>',unsafe_allow_html=True)
            evidence=hindsight_mgr.recall(site_id,question,limit=8)
            brief=advise(question,evidence)
            st.markdown(f'<div class="insight">{esc(brief["answer"])}</div><div class="event-meta">{esc(brief["mode"])}</div></div>',unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><div class="eyebrow">OPEN SITE · RECOMMENDATION</div><div class="section-title">Patterns worth repeating</div><div class="subtle">Derived from recorded outcomes for this site</div><div class="divider"></div>',unsafe_allow_html=True)
            relevant=hindsight_mgr.recall(site_id,"winning content conversion rankings helpful proof signup",limit=3)
            if relevant:
                for memory in relevant:
                    st.markdown(f'<div class="insight">{esc(memory["content"][:330])}</div>',unsafe_allow_html=True)
            else:
                st.markdown('<div class="event-copy">Add experiments and ranking outcomes to build evidence-backed recommendations.</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
    st.write("")
    left,right=st.columns([1.3,1])
    with left:
        st.markdown('<div class="section-title">Recent growth signals</div><div class="subtle">Your SEO, content, and conversion timeline</div>',unsafe_allow_html=True)
        for item in sorted(events,key=lambda event:event.get("date", ""),reverse=True)[:4]:
            st.markdown(f'<div class="card" style="padding:14px 17px;margin-top:9px"><div class="event-meta">{esc(item.get("date","")[:10])} &nbsp;·&nbsp; {esc(item.get("category","signal").replace("_"," ").upper())}</div><div class="event-title">{esc(item["title"])}</div><div class="event-copy">{esc(item["content"][:280])}</div></div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-title">Add a growth signal</div><div class="subtle">Keep your learning loop current</div>',unsafe_allow_html=True)
        with st.form("quick_capture"):
            signal_type=st.selectbox("Signal type",["Experiment result","Ranking change","Algorithm update","Content performance"])
            signal_title=st.text_input("Title",placeholder="e.g. Product page title test")
            signal_result=st.text_area("What happened?",placeholder="Include the change, timeframe, and measured outcome.",height=90)
            save=st.form_submit_button("Save to OpenSite memory")
            if save:
                if not signal_title.strip() or not signal_result.strip(): st.error("Add a title and an outcome before saving.")
                else:
                    tag=signal_type.lower().replace(" ","_")
                    prefix={"Experiment result":"NEW EXPERIMENT","Ranking change":"RANKING UPDATE","Algorithm update":"ALGORITHM UPDATE","Content performance":"CONTENT PERFORMANCE"}[signal_type]
                    hindsight_mgr.retain(site_id,f"[{prefix}] {signal_title.strip()}: {signal_result.strip()}",tags=[tag,"user_recorded"],metadata={"type":signal_type,"title":signal_title.strip()})
                    st.success("Saved. OpenSite will include this signal in future recall.")
                    st.rerun()

elif page == "SEO audit":
    add_page_header("TECHNICAL SEO · SITE HEALTH","Website auditor","Crawl your public website, find on-page technical issues, and retain audit snapshots for comparison over time.")
    st.write("")
    with st.form("site_crawl"):
        url=st.text_input("Website URL",value=f"https://{site['domain']}")
        limit=st.slider("Maximum pages",min_value=5,max_value=100,value=30,step=5)
        run=st.form_submit_button("Run technical SEO audit",type="primary")
    if run:
        try:
            with st.spinner("Crawling same-host pages and checking metadata…"):
                audit=crawl_site(url,max_pages=limit)
            st.session_state["last_audit"]=audit
            summary=audit["summary"]
            details={"summary":summary,"findings":audit["findings"],"pages":audit["pages"][:100],"crawl_errors":audit["errors"]}
            remember_import(site_id,"OpenSite Website Auditor",f"{summary['pages_crawled']} pages crawled, {summary['errors']} errors, {summary['warnings']} warnings",details)
        except Exception as exc:
            st.error(f"Audit could not complete: {exc}")
    audit=st.session_state.get("last_audit")
    if audit:
        summary=audit["summary"]
        a,b,c,d=st.columns(4); a.metric("Pages crawled",summary["pages_crawled"]); b.metric("Errors",summary["errors"]); c.metric("Warnings",summary["warnings"]); d.metric("Info",summary["info"])
        st.markdown('<div class="section-title">Prioritized findings</div>',unsafe_allow_html=True)
        if audit["findings"]:
            findings=pd.DataFrame(audit["findings"])
            st.dataframe(findings,use_container_width=True,hide_index=True)
        else: st.success("No issues found in the pages crawled.")
        with st.expander(f"Crawled pages ({len(audit['pages'])})"):
            st.dataframe(pd.DataFrame(audit["pages"]),use_container_width=True,hide_index=True)
        if audit["errors"]:
            with st.expander(f"Fetch notes ({len(audit['errors'])})"):
                st.dataframe(pd.DataFrame(audit["errors"]),use_container_width=True,hide_index=True)

elif page == "Content intelligence":
    add_page_header("CONTENT · COVERAGE · OPPORTUNITY", "Content intelligence", "Review content structure and crawl-level signals to find pages worth improving. This is page analysis, not a substitute for analytics outcomes.")
    st.write("")
    content_audit = st.session_state.get("last_audit")
    if not content_audit:
        st.info("Run a Website auditor crawl first. OpenSite will reuse that crawl so it does not fetch the same pages twice.")
        if st.button("Open SEO audit", type="primary"):
            st.session_state["content_audit_hint"] = True
    else:
        pages = content_audit.get("pages", [])
        if not pages:
            st.info("The most recent crawl did not return HTML pages.")
        else:
            page_df = pd.DataFrame([{
                "Page": item.get("url", ""), "Words": item.get("word_count", 0),
                "H1": " · ".join(item.get("h1", [])), "H2 count": len(item.get("h2", [])),
                "Title": item.get("title", ""), "Images missing alt": item.get("images_missing_alt", 0),
            } for item in pages])
            total_words = int(page_df["Words"].sum())
            a, b, c = st.columns(3)
            a.metric("Pages analyzed", len(pages))
            b.metric("Average words per page", f"{total_words / max(len(pages), 1):,.0f}")
            c.metric("Pages under 300 words", int((page_df["Words"] < 300).sum()))
            st.dataframe(page_df.sort_values("Words"), use_container_width=True, hide_index=True)
            selected_url = st.selectbox("Inspect page structure", [item.get("url", "") for item in pages])
            selected_page = next((item for item in pages if item.get("url") == selected_url), {})
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### Headings")
                st.markdown("**H1**")
                st.write("\n".join(f"- {heading}" for heading in selected_page.get("h1", [])) or "No H1 headings found")
                st.markdown("**H2**")
                st.write("\n".join(f"- {heading}" for heading in selected_page.get("h2", [])) or "No H2 headings found")
            with col_b:
                st.markdown("#### Extracted text sample")
                st.caption(selected_page.get("text_sample", "")[:1000] or "No visible text captured")
            if st.button("Save content crawl snapshot"):
                remember_import(site_id, "OpenSite Content Intelligence", f"Analyzed structure of {len(pages)} pages", page_df.to_dict("records"))
                st.success("Content snapshot saved to property memory.")

elif page == "Competitor analysis":
    add_page_header("COMPETITIVE RESEARCH · PUBLIC PAGES", "Competitor analysis", "Compare public on-page content and technical signals. OpenSite does not infer competitor traffic, rankings, or backlinks from a page crawl.")
    st.write("")
    competitor_url = st.text_input("Competitor website", placeholder="https://competitor.example")
    competitor_limit = st.slider("Pages to inspect", min_value=1, max_value=20, value=5)
    if st.button("Analyze competitor pages", type="primary"):
        try:
            with st.spinner("Crawling public pages and respecting robots.txt…"):
                result = crawl_site(competitor_url, max_pages=competitor_limit)
            st.session_state["competitor_audit"] = result
            remember_import(site_id, "OpenSite Competitor Analysis", f"Inspected {len(result['pages'])} public pages on {result['start_url']}", {"summary": result["summary"], "pages": result["pages"]})
        except Exception as exc:
            st.error(f"Competitor crawl could not complete: {exc}")
    competitor_audit = st.session_state.get("competitor_audit")
    if competitor_audit:
        competitor_pages = competitor_audit.get("pages", [])
        a, b, c = st.columns(3)
        a.metric("Public pages inspected", len(competitor_pages))
        b.metric("Avg. word count", f"{sum(p.get('word_count',0) for p in competitor_pages) / max(len(competitor_pages),1):,.0f}")
        c.metric("Findings", len(competitor_audit.get("findings", [])))
        if competitor_pages:
            st.dataframe(pd.DataFrame([{"URL": p["url"], "Title": p["title"], "Words": p.get("word_count",0), "H1": " · ".join(p.get("h1", [])), "H2 count": len(p.get("h2", [])), "Missing alt": p.get("images_missing_alt",0)} for p in competitor_pages]), use_container_width=True, hide_index=True)
        if competitor_audit.get("findings"):
            with st.expander("Public technical findings"):
                st.dataframe(pd.DataFrame(competitor_audit["findings"]), use_container_width=True, hide_index=True)

elif page == "Keyword rankings":
    add_page_header("SEARCH VISIBILITY · QUERIES","Keyword rankings","Track query clicks, impressions, click-through rate, and average position from Search Console or SerpBear history.")
    st.write("")
    rank_source=st.radio("Ranking source",["Google Search Console","SerpBear"],horizontal=True)
    if rank_source=="Google Search Console":
        with st.form("gsc_query_rankings"):
            token=st.text_input("OAuth access token",type="password",help="Needs the webmasters.readonly scope and access to this property.")
            property_name=st.text_input("Search Console property",value=site["domain"])
            submitted=st.form_submit_button("Fetch query rankings",type="primary")
        if submitted:
            try:
                result=integrations.search_console_queries(token,property_name)
                st.session_state["rank_rows"]=result["rows"]
                remember_import(site_id,"Google Search Console query rankings",f"{len(result['rows'])} query rows for {result['range']}",result["rows"])
            except Exception as exc: st.error(f"Could not load query rankings: {exc}")
    else:
        with st.form("serpbear_rankings"):
            host=st.text_input("SerpBear URL",placeholder="https://serpbear.example.com")
            key=st.text_input("SerpBear API key",type="password")
            tracked_domain=st.text_input("Tracked domain",value=site["domain"])
            submitted=st.form_submit_button("Fetch tracked keywords",type="primary")
        if submitted:
            try:
                result=integrations.serp_bear_keywords(host,key,tracked_domain)
                st.session_state["rank_rows"]=result["keywords"]
                remember_import(site_id,"SerpBear keyword rankings",f"{len(result['keywords'])} tracked keywords",result["keywords"])
            except Exception as exc: st.error(f"Could not load SerpBear rankings: {exc}")
    rank_rows=st.session_state.get("rank_rows",[])
    if rank_rows:
        st.dataframe(pd.DataFrame(rank_rows),use_container_width=True,hide_index=True)
        st.download_button("Download ranking data",pd.DataFrame(rank_rows).to_csv(index=False),file_name="opensite-keyword-rankings.csv",mime="text/csv")
    else:
        st.caption("Rank history requires Search Console or a configured SERP provider such as SerpBear. Search Console reports queries for your own verified properties; it does not provide competitor rankings or search volume.")

elif page == "Experiments":
    add_page_header("LEARN · TEST · COMPOUND","Experiment history","Review what changed, the measured result, and the lesson to carry into the next test.")
    st.write("")
    positive=sum(any(token in item["content"].lower() for token in ["winner","increased","generated","surged","drove","lift"]) for item in experiments)
    a,b,c=st.columns(3); a.metric("Experiments",len(experiments)); b.metric("Positive outcomes",positive); c.metric("Property",site["domain"])
    st.write("")
    category_filter=st.selectbox("Filter experiments",["All types","A/B tests","Content tests","Conversion tests"])
    visible=[]
    for item in experiments:
        category=item["category"].lower()
        if category_filter=="A/B tests" and "ab_test" not in category: continue
        if category_filter=="Content tests" and "content" not in category: continue
        if category_filter=="Conversion tests" and "cro" not in category: continue
        visible.append(item)
    if not visible: st.info("No experiments match that filter yet. Record your next test below.")
    for item in sorted(visible,key=lambda event:event.get("date", ""),reverse=True):
        st.markdown(f'<div class="card" style="margin-bottom:11px"><div class="event-meta">{esc(item.get("date","")[:10])} &nbsp;·&nbsp; {esc(item["category"].upper().replace("_"," "))}</div><div class="section-title">{esc(item["title"])}</div><div class="event-copy" style="font-size:13px;margin-top:7px">{esc(item["content"])}</div><div style="margin-top:10px">'+''.join(f'<span class="tag tag-lime">{esc(tag)}</span>' for tag in item.get("tags",[])[:5])+'</div></div>',unsafe_allow_html=True)
    with st.expander("Record a new experiment"):
        with st.form("new_experiment"):
            title=st.text_input("Experiment name")
            hypothesis=st.text_input("Hypothesis",placeholder="We believe changing X will improve Y because…")
            result=st.text_area("Result and learning",placeholder="Variant, sample/timeframe, measured outcome, and decision")
            submitted=st.form_submit_button("Save experiment")
            if submitted:
                if not title.strip() or not result.strip(): st.error("An experiment name and result are required.")
                else:
                    description=f"Hypothesis: {hypothesis.strip()}. Result: {result.strip()}" if hypothesis.strip() else result.strip()
                    hindsight_mgr.retain(site_id,f"[NEW EXPERIMENT] {title.strip()}: {description}",tags=["experiment","ab_test","user_recorded"],metadata={"type":"Experiment","title":title.strip()})
                    st.success("Experiment saved to persistent site memory."); st.rerun()

elif page == "Rankings & updates":
    add_page_header("RANKINGS · CONTENT · ALGORITHM","Search visibility","Keep ranking changes and search updates connected to what your team published and fixed.")
    st.write("")
    col1,col2=st.columns([1.15,1])
    with col1:
        st.markdown('<div class="section-title">Search and technical timeline</div>',unsafe_allow_html=True)
        if not updates: st.info("No ranking changes or algorithm updates recorded yet.")
        for item in sorted(updates,key=lambda event:event.get("date", ""),reverse=True):
            st.markdown(f'<div class="card" style="margin:9px 0"><div class="event-meta">{esc(item.get("date","")[:10])} &nbsp;·&nbsp; {esc(item["category"].replace("_"," ").upper())}</div><div class="event-title">{esc(item["title"])}</div><div class="event-copy">{esc(item["content"])}</div><div style="margin-top:8px"><span class="tag tag-lime">{esc(item.get("metadata",{}).get("impact","Impact recorded"))}</span></div></div>',unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="section-title">Content performance memory</div><div class="subtle">Measured content outcomes</div>',unsafe_allow_html=True)
        content_events=[item for item in events if "content" in item["category"] or any(tag in " ".join(item.get("tags",[])).lower() for tag in ["rankings","dwell_time","backlinks"])]
        if not content_events: st.info("Record content outcomes to build this view.")
        for item in content_events:
            outcome=item.get("metadata",{}).get("outcome") or item.get("metadata",{}).get("impact") or "Outcome captured"
            st.markdown(f'<div class="card" style="margin:9px 0"><div class="eyebrow">{esc(item.get("date","")[:10])} · CONTENT SIGNAL</div><div class="section-title" style="margin-top:7px">{esc(item["title"])}</div><div class="metric-delta" style="margin:8px 0">{esc(outcome)}</div><div class="event-copy">{esc(item["content"][:280])}</div></div>',unsafe_allow_html=True)
        with st.expander("Record ranking or update"):
            with st.form("ranking_record"):
                title=st.text_input("Keyword, page, or update")
                kind=st.selectbox("Signal type",["Ranking change","Algorithm update","Technical SEO"])
                detail=st.text_area("Change and impact")
                submitted=st.form_submit_button("Save signal")
                if submitted:
                    if not title.strip() or not detail.strip(): st.error("Add a subject and what changed.")
                    else:
                        prefix="RANKING UPDATE" if kind=="Ranking change" else "ALGORITHM UPDATE"
                        hindsight_mgr.retain(site_id,f"[{prefix}] {title.strip()}: {detail.strip()}",tags=[kind.lower().replace(" ","_"),"rankings","user_recorded"],metadata={"type":kind,"title":title.strip()})
                        st.success("Signal saved to site memory."); st.rerun()
    st.markdown('<div class="divider"></div><div class="section-title">Official Google Search updates</div><div class="subtle">Recent posts from Google Search Central. Treat timing as context, not proof of cause.</div>',unsafe_allow_html=True)
    if st.button("Check official update feed"):
        try: st.session_state["google_search_updates"]=integrations.google_search_updates()
        except Exception as exc: st.error(f"Could not read official feed: {exc}")
    for update in st.session_state.get("google_search_updates",{}).get("updates",[]):
        st.markdown(f'<div class="card" style="margin:8px 0;padding:14px 17px"><div class="event-meta">{esc(update["published"])}</div><div class="event-title">{esc(update["title"])}</div><div class="event-copy">{esc(update["summary"][:450])}</div><a href="{esc(update["url"])}" target="_blank">Open Google Search Central ↗</a></div>',unsafe_allow_html=True)

elif page == "Memory bank":
    add_page_header("HINDSIGHT · SITE LEARNING","OpenSite memory","Search your durable growth history. Every recorded experiment and ranking signal improves future recall.")
    st.write("")
    query=st.text_input("Search memories",placeholder="Try: signup conversion, ranking gains, helpful content update",label_visibility="collapsed")
    if query:
        memories=hindsight_mgr.recall(site_id,query,limit=10)
        st.markdown(f'<div class="eyebrow" style="margin:18px 0 8px">{len(memories)} MATCHING MEMORIES</div>',unsafe_allow_html=True)
        if not memories: st.info("No matching memories yet. Add a signal from the Overview or Experiments page.")
        for memory in memories:
            st.markdown(f'<div class="card" style="margin:8px 0"><div class="event-meta">{esc(memory.get("timestamp","")[:10])}</div><div class="event-copy" style="font-size:13px">{esc(memory["content"])}</div><div style="margin-top:8px">'+''.join(f'<span class="tag">{esc(tag)}</span>' for tag in memory.get("tags",[])[:5])+'</div></div>',unsafe_allow_html=True)
    else:
        st.markdown('<div class="eyebrow" style="margin:18px 0 8px">ASK OPEN SITE</div>',unsafe_allow_html=True)
        prompts=st.columns(3)
        for col,prompt in zip(prompts,["What improved conversion?","Which content earned ranking gains?","What did algorithm updates reward?"]):
            with col:
                if st.button(prompt,use_container_width=True): st.session_state.memory_query=prompt
        if st.session_state.get("memory_query"):
            for memory in hindsight_mgr.recall(site_id,st.session_state.memory_query,limit=6):
                st.markdown(f'<div class="card" style="margin:8px 0"><div class="event-copy">{esc(memory["content"])}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="divider"></div><div class="eyebrow">RECENT SITE MEMORY · LOCAL STORE SURVIVES RESTARTS</div>',unsafe_allow_html=True)
    for memory in reversed(site_memories[-30:]):
        st.markdown(f'<div class="card" style="margin:7px 0;padding:12px 16px"><div class="event-meta">{esc(memory.get("timestamp","")[:10])} &nbsp;·&nbsp; {esc(", ".join(memory.get("tags",[])[:4]))}</div><div class="event-copy">{esc(memory["content"][:400])}</div></div>',unsafe_allow_html=True)

elif page == "Data connections":
    add_page_header("CONNECT YOUR STACK","Live data connections","Connect read-only Search Console, analytics, and experiment data. Credentials stay in this browser session and are never written to OpenSite memory.")
    st.write("")
    st.info("Google Search Console and GA4 need a valid Google OAuth access token with the matching read-only scope. Plausible, PostHog, and Umami require their own API keys. These providers do not expose account data without your authorization.")
    top_left,top_right=st.columns(2)
    with top_left:
        with st.form("gsc_connect"):
            st.markdown("#### Google Search Console")
            gsc_token=st.text_input("OAuth access token",type="password",help="Scope: https://www.googleapis.com/auth/webmasters.readonly")
            gsc_property=st.text_input("Verified property",value=site["domain"],help="Use sc-domain:example.com for a Domain property, or the exact URL prefix.")
            gsc_submit=st.form_submit_button("Fetch Search Console data",type="primary")
        if gsc_submit:
            try:
                result=integrations.search_console_report(gsc_token,gsc_property)
                st.session_state["gsc_live"]=result
                remember_import(site_id,result["provider"],f"{result['clicks']} clicks, {result['impressions']} impressions, CTR {result['ctr']:.2%}, average position {result['average_position']}",result["rows"])
                st.success(f"Connected · {result['clicks']:,} clicks · {result['impressions']:,} impressions · average position {result['average_position'] or '—'}")
            except Exception as exc: st.error(f"Search Console connection failed: {exc}")
        if st.session_state.get("gsc_live"):
            frame=pd.DataFrame([{"date":row.get("keys",[""])[0],"clicks":row.get("clicks",0),"impressions":row.get("impressions",0)} for row in st.session_state["gsc_live"]["rows"]])
            if not frame.empty:
                frame["date"]=pd.to_datetime(frame["date"])
                st.line_chart(frame.set_index("date")[["clicks","impressions"]])
    with top_right:
        with st.form("ga4_connect"):
            st.markdown("#### Google Analytics 4")
            ga_token=st.text_input("OAuth access token",type="password",key="ga_token",help="Scope: https://www.googleapis.com/auth/analytics.readonly")
            ga_property=st.text_input("GA4 property ID",placeholder="123456789")
            ga_submit=st.form_submit_button("Fetch GA4 data",type="primary")
        if ga_submit:
            try:
                result=integrations.ga4_report(ga_token,ga_property)
                st.session_state["ga4_live"]=result
                remember_import(site_id,result["provider"],f"{result['sessions']} sessions, {result['users']} users, {result['conversions']} conversions",result["rows"])
                st.success(f"Connected · {result['sessions']:,} sessions · {result['users']:,} users · {result['conversions']:,.0f} conversions")
            except Exception as exc: st.error(f"GA4 connection failed: {exc}")
        if st.session_state.get("ga4_live"):
            st.dataframe(pd.DataFrame(st.session_state["ga4_live"]["rows"]),use_container_width=True,hide_index=True)
    st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a:
        with st.form("plausible_connect"):
            st.markdown("#### Plausible Analytics")
            pl_key=st.text_input("Stats API key",type="password",key="pl_key")
            pl_domain=st.text_input("Site domain",value=site["domain"],key="pl_domain")
            pl_host=st.text_input("Plausible host",value="https://plausible.io",key="pl_host")
            pl_submit=st.form_submit_button("Fetch Plausible stats")
        if pl_submit:
            try:
                st.session_state["plausible_live"]=integrations.plausible_report(pl_key,pl_domain,pl_host)
                remember_import(site_id,"Plausible Analytics","30 day stats fetched",st.session_state["plausible_live"].get("results",[]))
                st.success("Plausible data loaded.")
            except Exception as exc: st.error(f"Plausible connection failed: {exc}")
        if st.session_state.get("plausible_live"): st.json(st.session_state["plausible_live"].get("results",[]))
    with b:
        with st.form("posthog_connect"):
            st.markdown("#### PostHog")
            ph_key=st.text_input("Personal API key",type="password",key="ph_key")
            ph_project=st.text_input("Project ID",key="ph_project")
            ph_host=st.text_input("Private API host",value="https://us.posthog.com",key="ph_host")
            ph_submit=st.form_submit_button("Fetch PostHog events")
        if ph_submit:
            try:
                st.session_state["posthog_live"]=integrations.posthog_report(ph_key,ph_project,ph_host)
                remember_import(site_id,"PostHog","30 day event trend fetched",st.session_state["posthog_live"].get("rows",[]))
                st.success("PostHog event data loaded.")
            except Exception as exc: st.error(f"PostHog connection failed: {exc}")
        if st.session_state.get("posthog_live"): st.dataframe(pd.DataFrame(st.session_state["posthog_live"]["rows"],columns=st.session_state["posthog_live"]["columns"]),use_container_width=True,hide_index=True)
    with c:
        with st.form("umami_connect"):
            st.markdown("#### Umami Analytics")
            um_key=st.text_input("API key",type="password",key="um_key")
            um_website=st.text_input("Website ID",key="um_website")
            um_host=st.text_input("API base URL",value="https://api.umami.is/v1",key="um_host")
            um_submit=st.form_submit_button("Fetch Umami stats")
        if um_submit:
            try:
                st.session_state["umami_live"]=integrations.umami_report(um_key,um_website,um_host)
                remember_import(site_id,"Umami","30 day site stats fetched",st.session_state["umami_live"])
                st.success("Umami stats loaded.")
            except Exception as exc: st.error(f"Umami connection failed: {exc}")
        if st.session_state.get("umami_live"): st.json(st.session_state["umami_live"])
    with st.expander("Connect Matomo (self-hosted or cloud)"):
        with st.form("matomo_connect"):
            st.markdown("#### Matomo Analytics")
            mt_host=st.text_input("Matomo URL",placeholder="https://analytics.example.com")
            mt_site=st.text_input("Site ID")
            mt_token=st.text_input("Read-only token_auth",type="password")
            mt_submit=st.form_submit_button("Fetch Matomo stats")
        if mt_submit:
            try:
                st.session_state["matomo_live"]=integrations.matomo_report(mt_host,mt_site,mt_token)
                remember_import(site_id,"Matomo","last 30 days of daily visits fetched",st.session_state["matomo_live"].get("results",{}))
                st.success("Matomo stats loaded.")
            except Exception as exc: st.error(f"Matomo connection failed: {exc}")
        if st.session_state.get("matomo_live"): st.json(st.session_state["matomo_live"].get("results",{}))
    with st.expander("Connect GrowthBook experiment history"):
        with st.form("growthbook_connect"):
            gb_host=st.text_input("GrowthBook API URL",value="https://api.growthbook.io")
            gb_key=st.text_input("Read-only API key",type="password")
            gb_submit=st.form_submit_button("Fetch experiments")
        if gb_submit:
            try:
                result=integrations.growthbook_experiments(gb_host,gb_key)
                st.session_state["growthbook_live"]=result.get("experiments",[])
                remember_import(site_id,"GrowthBook experiments",f"{len(st.session_state['growthbook_live'])} experiments",st.session_state["growthbook_live"])
                st.success(f"Loaded {len(st.session_state['growthbook_live'])} experiments.")
            except Exception as exc: st.error(f"GrowthBook connection failed: {exc}")
        if st.session_state.get("growthbook_live"): st.dataframe(pd.DataFrame(st.session_state["growthbook_live"]),use_container_width=True,hide_index=True)
    with st.expander("Connect Chrome UX Report (CrUX)"):
        st.caption("CrUX needs a Google Cloud API key with Chrome UX Report API enabled.")
        with st.form("crux_connect"):
            crux_key=st.text_input("Google API key",type="password")
            crux_url=st.text_input("Page or origin URL",value=f"https://{site['domain']}")
            crux_submit=st.form_submit_button("Fetch field Core Web Vitals")
        if crux_submit:
            try:
                result=integrations.crux_report(crux_key,crux_url)
                st.session_state["crux_live"]=result
                remember_import(site_id,"Chrome UX Report",f"Field vitals fetched for {crux_url}",result.get("metrics",{}))
                st.success("Chrome UX field data loaded.")
            except Exception as exc: st.error(f"CrUX request failed: {exc}")
        if st.session_state.get("crux_live"): st.json(st.session_state["crux_live"].get("metrics",{}))
    st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
    with st.form("pagespeed_check"):
        st.markdown("#### Google PageSpeed Insights")
        p1,p2=st.columns([3,1])
        with p1: audit_url=st.text_input("Page URL",value=f"https://{site['domain']}")
        with p2: strategy=st.selectbox("Device",["mobile","desktop"])
        audit_submit=st.form_submit_button("Run free Lighthouse audit")
    if audit_submit:
        try:
            audit=integrations.pagespeed_report(audit_url,strategy)
            st.session_state["pagespeed_live"]={"scores":audit["scores"],"url":audit["url"],"strategy":audit["strategy"]}
            remember_import(site_id,"Google PageSpeed Insights",f"{strategy} scores {audit['scores']}",audit["scores"])
            score_cols=st.columns(len(audit["scores"]) or 1)
            for col,(name,value) in zip(score_cols,audit["scores"].items()): col.metric(name.title(),f"{value}/100")
        except Exception as exc: st.error(f"PageSpeed request failed: {exc}")
    st.caption("All API integrations are read-only. Google Search Central updates and site ranking history are shown as related context, not causal proof.")
