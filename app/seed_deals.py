from app.hindsight_manager import hindsight_mgr

SEED_DEALS = [
    {
        "deal_id": "acme_cloud_security",
        "company_name": "Acme Cloud Security",
        "industry": "Cybersecurity & Cloud Infrastructure",
        "deal_size": "$120,000 ARR",
        "primary_contact": "Marcus Vance (VP of Engineering)",
        "stakeholders": [
            {"name": "Marcus Vance", "role": "VP of Engineering", "focus": "System scale & low latency"},
            {"name": "Elena Rostova", "role": "Chief Information Security Officer (CISO)", "focus": "SOC2 Type II & Data Residency"},
            {"name": "David Sterling", "role": "Chief Financial Officer (CFO)", "focus": "Budget lock-in & Q4 fiscal calendar"}
        ],
        "calls": [
            {
                "call_number": 1,
                "title": "Discovery & Initial Architecture Review",
                "date": "2026-10-12T14:30:00Z",
                "transcript_summary": (
                    "Initial discovery meeting with Marcus Vance (VP Engineering). Acme is looking to replace legacy "
                    "monitoring and agent telemetry. Current pain point: agent logs take 45+ minutes to index and query. "
                    "Marcus mentioned they evaluated Datadog but found data ingress costs prohibitive ($15k/mo unexpected). "
                    "Marcus requires sub-100ms query latency and seamless multi-region AWS support. Target go-live is Q1."
                ),
                "tags": ["discovery", "architecture", "competitor:datadog", "latency"],
                "metadata": {"stakeholder": "Marcus Vance", "meeting_type": "Discovery"}
            },
            {
                "call_number": 2,
                "title": "Security Deep Dive with CISO",
                "date": "2026-10-24T16:00:00Z",
                "transcript_summary": (
                    "Technical security review with Elena Rostova (CISO) and Marcus Vance. Elena raised critical objection: "
                    "Acme cannot allow raw customer telemetry to leave their AWS VPC without customer-managed encryption keys (CMEK). "
                    "She specifically demanded proof of SOC2 Type II compliance and ISO 27001 certification. "
                    "We committed to providing the third-party SOC2 Type II audit report under NDA by Oct 28 and verified our CMEK support."
                ),
                "tags": ["security", "objection:soc2", "objection:cmek", "compliance", "ciso"],
                "metadata": {"stakeholder": "Elena Rostova", "meeting_type": "Security Review"}
            },
            {
                "call_number": 3,
                "title": "Commercial Negotiation & Procurement Review",
                "date": "2026-11-02T11:00:00Z",
                "transcript_summary": (
                    "Pricing discussion with David Sterling (CFO) and Marcus Vance. David raised severe budget friction: "
                    "Acme's fiscal year ends December 31, and all new Capex/Opex commitments above $100k require board signoff. "
                    "David pushed back aggressively against the 3-year upfront contract commitment ($360k total). "
                    "He noted: 'If you can structure this with a Q4 pilot ramp at $15k and quarterly billing starting Q1, "
                    "I can approve it under my discretionary spending authority without board delay.'"
                ),
                "tags": ["pricing", "objection:upfront_commitment", "procurement", "budget_freeze", "cfo"],
                "metadata": {"stakeholder": "David Sterling", "meeting_type": "Commercial"}
            }
        ]
    },
    {
        "deal_id": "novafin_technologies",
        "company_name": "NovaFin Technologies",
        "industry": "FinTech & Real-Time Payments",
        "deal_size": "$85,000 ARR",
        "primary_contact": "Rachel Tan (Head of Platform)",
        "stakeholders": [
            {"name": "Rachel Tan", "role": "Head of Platform", "focus": "99.999% uptime SLA"},
            {"name": "Samir Patel", "role": "VP Product", "focus": "Developer experience & SDK support"}
        ],
        "calls": [
            {
                "call_number": 1,
                "title": "Platform Ingestion & Latency Evaluation",
                "date": "2026-10-18T10:00:00Z",
                "transcript_summary": (
                    "Evaluation call with Rachel Tan. NovaFin processes 2M transactions/day. "
                    "They had a major outage in September due to downstream webhook queuing. "
                    "Rachel requires contractual guarantee of 99.999% availability with financial penalty credits. "
                    "Rachel also noted they love Python and Go SDKs and hate manual API schemas."
                ),
                "tags": ["discovery", "sla:five_nines", "fintech", "reliability"],
                "metadata": {"stakeholder": "Rachel Tan", "meeting_type": "Discovery"}
            },
            {
                "call_number": 2,
                "title": "Commercial Terms & Competitor Benchmark",
                "date": "2026-10-30T15:30:00Z",
                "transcript_summary": (
                    "Commercial session with Rachel Tan and Samir Patel. Competitor Dynatrace offered a 30% first-year discount. "
                    "Samir said they prefer our modern architecture, but procurement will default to Dynatrace if we cannot match "
                    "the first-year cost offset or include premium 24/7 dedicated Slack support."
                ),
                "tags": ["competitor:dynatrace", "pricing", "support_sla", "procurement"],
                "metadata": {"stakeholder": "Samir Patel", "meeting_type": "Commercial"}
            }
        ]
    }
]

def seed_deal_memories():
    """Populates Hindsight banks with multi-call enterprise deal history."""
    count = 0
    for deal in SEED_DEALS:
        bank_id = deal["deal_id"]
        # Seed general profile
        hindsight_mgr.retain(
            bank_id=bank_id,
            content=f"Deal Profile for {deal['company_name']}: Industry: {deal['industry']}, Deal Size: {deal['deal_size']}, Primary Contact: {deal['primary_contact']}.",
            tags=["profile", "account_overview"],
            metadata={"company": deal["company_name"]}
        )
        count += 1
        
        # Seed each call
        for call in deal["calls"]:
            hindsight_mgr.retain(
                bank_id=bank_id,
                content=f"[Call #{call['call_number']} - {call['title']}] on {call['date']}: {call['transcript_summary']}",
                timestamp=call["date"],
                tags=call["tags"],
                metadata=call["metadata"]
            )
            count += 1
    return count
