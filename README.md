# OpenSite

**SEO & Conversion Intelligence Agent for Growth & Marketing teams.** OpenSite remembers ranking history, landing page experiments, content performance, and algorithm updates so teams can learn which changes actually improve search visibility and conversion.

## Run OpenSite

```bash
python -m venv .venv
source .venv/bin/activate
pip install streamlit pandas pydantic python-dotenv
streamlit run app/main.py
```

This repository includes a `venv` directory in some development environments. If it is already set up, run `./venv/bin/streamlit run app/main.py`.

## Deploy to Firebase

The Python/Streamlit app runs as a container on Cloud Run; Firebase Hosting provides the public HTTPS URL and routes requests to that service. Install the Firebase CLI and Google Cloud CLI, select a Firebase project you control, then:

```bash
firebase use <your-firebase-project-id>
firebase hosting:sites:create opensite
firebase target:apply hosting opensite opensite
gcloud run deploy opensite --source . --region us-central1 --allow-unauthenticated --port 8080
firebase deploy --only hosting
```

The local JSON memory store is not durable on Cloud Run because its container filesystem is ephemeral. Configure Hindsight Cloud or another durable memory backend before relying on deployed memory; do not treat a Cloud Run instance's local file as a backup. Set `OPENSITE_ACCESS_PASSWORD` as a Cloud Run secret for the optional shared-password gate. Configure secrets with Google Secret Manager/Cloud Run environment variables, never commit `.env` or credentials.

## What it does

- **Overview:** review site baselines, historical signals, recent changes, and recall-based recommendations.
- **SEO audit:** crawl public same-host pages, respect `robots.txt`, check titles, descriptions, headings, canonical links, image alt text, and store timestamped audit snapshots.
- **Keyword rankings:** fetch Search Console query performance or position history from a connected SerpBear instance.
- **Experiments:** inspect A/B and content experiments, filter by type, and record new hypotheses and outcomes.
- **Rankings & updates:** keep search ranking, technical SEO, and algorithm update history alongside content results.
- **Memory bank:** search the site's durable history and review the records that inform OpenSite's answers.

The Overview's growth advisor retrieves relevant history first. To enable generated local synthesis, install Ollama, pull a model such as `qwen2.5:7b`, and set `OLLAMA_ENABLED=true`, `OLLAMA_BASE_URL`, and `OLLAMA_MODEL` in `.env`. Without Ollama, it returns matching stored evidence without inventing a generated answer.

## Current scope

This is a runnable local-first product foundation. Live data requires the site's owner to configure provider credentials and property access. Scheduled polling, account authentication, a multi-user PostgreSQL deployment, full local map rendering, automated competitor SERP/backlink analysis, and direct GrowthBook experiment creation/management are not implemented in this version. SERP and competitor datasets generally require a separately configured provider. Search update timing is contextual and should not be treated as proof of cause.

OpenSite keeps local memories in `app/data/memories.json`. They persist across restarts. If the Hindsight SDK and `HINDSIGHT_API_KEY` are configured, OpenSite also mirrors writes and uses remote recall, with local fallback when remote access is unavailable.

Add your property from the sidebar before connecting private data. Custom properties are stored in `app/data/sites.json`; their metrics are blank until you import or record real data.

## Live data connections

Open **Data connections** in the app to make read-only requests to Google Search Console, Google Analytics 4, Plausible, PostHog, Umami, Matomo, GrowthBook, Chrome UX Report, or Google's PageSpeed Insights. Use **Keyword rankings** for Search Console query metrics or SerpBear position history. Google Search Console and GA4 use OAuth access tokens; the other analytics providers use their API keys or read-only tokens. PageSpeed Insights can run without a key at normal personal usage.

The user supplies valid provider credentials and grants property access; OpenSite cannot connect to private analytics accounts without them. Credentials entered in the app stay in the current Streamlit browser session and are not saved to the memory bank. A successful pull stores a timestamped metrics snapshot in the selected site's memory bank so OpenSite can build history over repeated imports. For ongoing production ingestion, configure Streamlit behind HTTPS and add a managed secrets vault or OAuth authorization flow. Google access tokens expire, so the current UI requires a fresh token when needed.

OpenSite's analytics connectors are read-only. GrowthBook experiment records can be imported; otherwise use the Experiments form. Live conversion rates require a GA4/Plausible/PostHog/Matomo goal or event configured in that provider. The built-in crawler limits scope to public pages on the entered host, caps a crawl at 100 pages, and skips URLs disallowed by `robots.txt`. The update monitor reads Google's official Search Central RSS feed and presents announcements as context, not proof of causality.

`app/seed_seo_data.py` remains as illustrative history for the demo sites. Treat those seeded values as examples; live connectors return separate provider data and do not silently replace the demo history.

Copy `.env.example` to `.env` to configure Hindsight or model credentials. Do not commit secret keys.
