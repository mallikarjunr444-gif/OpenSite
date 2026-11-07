<p align="center">
  <img src="assets/opensite-logo.svg" alt="OpenSite" width="720" />
</p>

<h1 align="center">OpenSite</h1>
<p align="center"><strong>SEO & Conversion Intelligence Agent</strong><br />Understand. Optimize. Grow.</p>

OpenSite is a growth intelligence workspace for marketing teams. It brings search visibility, website health, analytics, content performance, and experiment outcomes into one history, then uses that evidence to help decide what to improve next.

## What OpenSite does

- **Growth overview:** review saved site signals and ask the advisor questions grounded in that history.
- **Website auditor:** crawl a public site, respect `robots.txt`, and flag missing or duplicate metadata, heading issues, and images without alt text. Audit results become memories.
- **Keyword rankings:** import query metrics from Google Search Console or position history from SerpBear.
- **Analytics connections:** read metrics from GA4, Plausible, PostHog, Umami, and Matomo.
- **Experiments:** record hypotheses and outcomes; import experiment records from GrowthBook.
- **Search updates:** view Google Search Central announcements alongside a site's history. Timing indicates context, not cause.
- **Performance:** run PageSpeed Insights and import Chrome UX Report field metrics.
- **Historical memory:** search saved audits, analytics snapshots, ranking history, and team-entered experiments.

## Quick start

Python 3.12 is used by the deployment container. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

In the app, choose **Add your website** in the sidebar, then open **Data connections** to authorize providers. Demo properties and history are examples; add your own site before using any data for reporting.

## How memory works

OpenSite gives each property its own memory bank. A successful data import, crawl, or manually recorded experiment is stored with its date, source tags, and metadata. Search and the growth advisor retrieve relevant memories before responding. Recommendations should distinguish observed changes from hypotheses; a ranking change near an algorithm update is correlation, not proof of causation.

The default local backend stores memory in `app/data/memories.json`, so it survives local app restarts. For a deployed service, use Firestore by setting `OPENSITE_MEMORY_BACKEND=firestore`; the Cloud Run service account needs Firestore access. The Firestore collection defaults to `opensite_memories`. Hindsight can also be enabled as an optional remote memory service by installing `hindsight-client` and setting `HINDSIGHT_BASE_URL` and `HINDSIGHT_API_KEY`. OpenSite keeps local/Firestore memory as its data source and mirrors writes to Hindsight when configured.

For generated natural-language synthesis, run Ollama locally, pull a model such as `qwen2.5:7b`, and set `OLLAMA_ENABLED=true`, `OLLAMA_BASE_URL`, and `OLLAMA_MODEL`. Without Ollama, the advisor presents relevant stored evidence without claiming to run an LLM.

## Connectors and credentials

All analytics connectors are read-only. OpenSite does not receive private account data until the site owner supplies credentials and grants property access.

| Source | OpenSite uses | Access needed |
| --- | --- | --- |
| Google Search Console | Clicks, impressions, CTR, position, and query rows | OAuth token with `webmasters.readonly` and verified property access |
| Google Analytics 4 | Sessions, users, conversion events | OAuth token with `analytics.readonly` and GA4 property access |
| SerpBear | Tracked keywords and saved position history | SerpBear URL and API key |
| Plausible, PostHog, Umami, Matomo | Analytics summaries and events | Provider API key/token and site/project ID |
| GrowthBook | Existing experiment records | Read-only GrowthBook API key |
| PageSpeed Insights | Lighthouse performance, SEO, and accessibility audits | Normally no key for personal use; quotas apply |
| Chrome UX Report | Aggregated real-user Core Web Vitals | Google Cloud API key with CrUX API enabled |
| Google Search Central | Official search announcements | Public RSS feed |

Credentials entered in the Streamlit UI remain in that browser session and are not written to the memory bank. Google OAuth access tokens expire and must be refreshed. External SERP positions, search-volume estimates, and backlink indexes need a separately configured data provider; open-source software alone cannot supply those datasets.

## Run with `.env`

Copy `.env.example` to `.env` for local options. Do not commit `.env` or provider keys.

```bash
cp .env.example .env
```

`OPENSITE_ACCESS_PASSWORD` enables an optional shared-password gate for a public deployment. It is unset locally by default. For deployed secrets, prefer Google Secret Manager over checked-in files or plain-text shell history.

## Firebase deployment

OpenSite's Python/Streamlit server runs on Cloud Run; Firebase Hosting routes its HTTPS requests to the container. The repository is configured for Firebase project `opensite-growth-mr444`, Hosting site `opensite-growth-mr444-hosting`, and Cloud Run service `opensite` in `us-central1`.

The project and Hosting site have been created. Cloud Run requires an active billing account even when staying within its free quota. After linking one to this Firebase project and enabling the Cloud Run, Cloud Build, Artifact Registry, and Firestore APIs:

1. Create a Secret Manager secret named `opensite-access-password` containing a strong password, then grant the Cloud Run service account access to that secret.
2. Configure `OPENSITE_MEMORY_BACKEND=firestore` and grant the service account Firestore access.
3. Deploy from the repository root:

```bash
gcloud config set project opensite-growth-mr444
gcloud run deploy opensite --source . --project opensite-growth-mr444 --region us-central1 --allow-unauthenticated --port 8080 --min 0 --max 2 --memory 1Gi --set-env-vars OPENSITE_MEMORY_BACKEND=firestore --set-secrets OPENSITE_ACCESS_PASSWORD=opensite-access-password:latest
firebase deploy --only hosting --project opensite-growth-mr444
```

Cloud Run requires an open billing account even though it has a free usage quota. The Google Cloud account available during setup had a closed billing account, so the Cloud Run service and Firebase Hosting rewrite are configured but not deployed. Reactivate/link an open billing account before running the commands above. Usage beyond included quotas can be billed. Firebase Hosting by itself only serves static content; it cannot run this Python app.

## GitHub Pages project site

The repository includes a responsive static OpenSite project landing page in `docs/`. GitHub Actions publishes it from the `main` branch using `.github/workflows/deploy-pages.yml`. After pushing the workflow, enable **Settings → Pages → Build and deployment → Source: GitHub Actions** in the repository. The landing page is separate from the Streamlit application: it describes OpenSite and links to setup instructions, while interactive dashboards, API connections, and persistent memory need the Python backend deployed on Cloud Run or another server host. The expected Pages address is `https://mallikarjunr444-gif.github.io/OpenSite/` after the first successful workflow run.

## Current scope

Implemented now: Streamlit workspace, local and Firestore memory backends, optional Hindsight mirroring, user-added sites, technical crawler, crawl-based content analysis, public competitor page comparison, Search Console/SerpBear rankings, analytics and GrowthBook imports, PageSpeed/CrUX, official search update feed, optional Ollama synthesis, and a static GitHub Pages landing page.

Still requiring additional implementation or provider configuration: scheduled sync and alerts, user accounts and team permissions, a full PostgreSQL/pgvector migration, map rendering/local pack rank tracking, automated competitor SERP/backlink research, and direct GrowthBook experiment creation/management. SERP and competitor datasets may require a separately configured provider. Review third-party licenses before redistributing integrated services.

## Project layout

```text
app/                 Streamlit UI, connectors, crawler, and memory
assets/              OpenSite brand assets
docs/                Static GitHub Pages project site
.github/workflows/   Pages publishing workflow
public/              Firebase Hosting assets
Dockerfile           Cloud Run container
firebase.json        Firebase Hosting rewrite to Cloud Run
.firebaserc          OpenSite Firebase project and Hosting target
.env.example         Local configuration template
```
