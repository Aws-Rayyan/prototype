"""Seed knowledge base documents (runs once when empty)."""

import json

from database import get_connection


def seed_documents(force: bool = False) -> int:
    """Insert seed documents if table is empty unless force."""
    conn = get_connection()
    try:
        count = conn.execute("SELECT COUNT(*) AS c FROM documents").fetchone()["c"]
        if count > 0 and not force:
            return 0

        if force:
            conn.execute("DELETE FROM documents")

        docs = _documents()
        conn.executemany(
            """
            INSERT INTO documents (id, title, content, department, allowed_roles)
            VALUES (:id, :title, :content, :department, :allowed_roles)
            """,
            docs,
        )
        conn.commit()
        return len(docs)
    finally:
        conn.close()


def _documents() -> list[dict]:
    # allowed_roles stored as JSON array string
    return [
        {
            "id": "doc-sales-pipeline-q3",
            "title": "Q3 Sales Pipeline Report",
            "content": """
The North America pipeline for Q3 shows $4.2M in qualified opportunities across enterprise accounts.
Key deal Acme renewal is staged at Negotiation with projected close Sep 28. Competitive risk: Pricing for
premium tier was flagged by the champion. Discount approvals above 15% require VP Sales sign-off per policy.
Rolling weekly forecast commits are stored in Salesforce under reports/Sales_NA_Q3.
            """.strip(),
            "department": "sales",
            "allowed_roles": json.dumps(["sales_manager"]),
        },
        {
            "id": "doc-territory-rules",
            "title": "Territory Assignment Rules 2026",
            "content": """
Territories are adjusted annually. SMB accounts (<500 employees) default to SMB pod; enterprise (>500)
routes to Named Account teams. Expansion into EMEA duplicates must be coordinated with Territory Ops to
avoid overlap. Contacts must be tagged with geo and segment before quoting.
            """.strip(),
            "department": "sales",
            "allowed_roles": json.dumps(["sales_manager"]),
        },
        {
            "id": "doc-spiff-program",
            "title": "Sales SPIFF Guidelines",
            "content": """
SPIFF payouts for accelerator products are pooled monthly from marketing budget SKU-ACC-9012.
Eligible reps receive payment if deal closes within the promotion window documented in Slack #sales-news.
Finance reconciles payouts with NetSuite SKU lines; disputes go to Revenue Ops within 14 days.
            """.strip(),
            "department": "sales",
            "allowed_roles": json.dumps(["sales_manager"]),
        },
        {
            "id": "doc-discount-matrix",
            "title": "Enterprise Discount Matrix",
            "content": """
Standard discount tiers: up to 10% AE-only, 11-15% needs Sales Manager, 16-25% VP Sales, above 25% CFO.
Multi-year prepay can add 2% additional discount with Legal review of contract terms. Public sector deals
follow separate policy PS-DISC-01 (not in this document).
            """.strip(),
            "department": "sales",
            "allowed_roles": json.dumps(["sales_manager"]),
        },
        {
            "id": "doc-benefits-guide",
            "title": "Employee Benefits Guide 2026",
            "content": """
Medical plans: PPO Gold, PPO Silver, HDHP with HSA. Enrollment changes allowed during open enrollment
or qualifying life events within 30 days. Parental leave: 16 weeks primary, 8 weeks secondary, paid per
local policy HR-PL-440. HSA employer contribution is deposited quarterly if enrolled in eligible plan.
401(k) match vests after 2 years; details in payroll portal.
            """.strip(),
            "department": "hr",
            "allowed_roles": json.dumps(["hr_manager"]),
        },
        {
            "id": "doc-hiring-playbook",
            "title": "Manager Hiring Playbook",
            "content": """
All reqs require HRBP approval before posting. Interview panels must include one cross-functional member
for L5+ roles. Offer letters route through DocuSign template HR-OFFER-STD. Compensation bands are in
Workday; outliers require CHRO weekly review memo. Background checks initiate only after verbal acceptance.
            """.strip(),
            "department": "hr",
            "allowed_roles": json.dumps(["hr_manager"]),
        },
        {
            "id": "doc-performance-cycle",
            "title": "Performance Review Cycle Instructions",
            "content": """
Annual cycle runs Nov-Jan. Calibration sessions are scheduled per org; ratings must cite evidence tied to
company values. Mandatory training on bias must be completed before submitting ratings. Appeals follow
ERG-APT-STEP3 within two weeks after release in Workday. HRBPs adjudicate escalation path.
            """.strip(),
            "department": "hr",
            "allowed_roles": json.dumps(["hr_manager"]),
        },
        {
            "id": "doc-workplace-incidents",
            "title": "Workplace Incident Intake Procedures",
            "content": """
Reports filed via Integrity Line or HR inbox are triaged within 24 business hours. Sensitive cases require
minimal distribution per legal hold instructions. Investigations may involve external counsel for HR
matters referencing policy HR-INV-009. Witness interviews conducted separately; documentation stored in HRIS
restricted vault.
            """.strip(),
            "department": "hr",
            "allowed_roles": json.dumps(["hr_manager"]),
        },
        {
            "id": "doc-company-holidays",
            "title": "Company Holiday Calendar",
            "content": """
US observes New Year's Day, MLK Jr Day, Memorial Day, Independence Day, Labor Day, Thanksgiving (+day after),
and Christmas week floating day per region announcements. Offices in Berlin follow German public holidays
listed on the intranet. Optional floating holidays (2/year) expire Dec 31; request via HR calendar tool.
Company-wide blackout for PTO applies during customer launch weeks published by Operations.
            """.strip(),
            "department": "hr",
            "allowed_roles": json.dumps(["sales_manager", "hr_manager"]),
        },
        {
            "id": "doc-expense-policy",
            "title": "Travel & Expense Policy",
            "content": """
Economy airfare default; business class flights over 6 hours with VP approval. Per diems follow IRS
guidelines; receipts required over $75. Client entertainment requires business justification in Concur.
Sales team client dinners capped at $150/person unless pre-approved Sales Marketing budget alignment.
Late submissions past 45 days denied without finance exception Case ID.
            """.strip(),
            "department": "finance",
            "allowed_roles": json.dumps(["sales_manager", "hr_manager"]),
        },
        {
            "id": "doc-internal-brand",
            "title": "Internal Brand & Communications Standards",
            "content": """
Customer-facing collateral must come from Brand portal v3. Approved logos and HEX colors enforced in Deck
starter kit. Tone: professional, inclusive, avoid unverified performance claims. Social posts by employees
require review if mentioning revenue or customer names; route to Comms within 24h.
            """.strip(),
            "department": "communications",
            "allowed_roles": json.dumps(["sales_manager", "hr_manager"]),
        },
        {
            "id": "doc-engineering-oncall",
            "title": "Engineering On-Call Runbook",
            "content": """
Primary/secondary rotation managed in PagerDuty service prod-core. Severity 1 pages require ack within
5 minutes; runbook steps in wiki/eng/runbooks/SRE-001. Hotfix deploys need two approvals from platform on-call.
Post-incident reviews due within 5 business days for SEV1/2. Customer comms only via Status page template.
            """.strip(),
            "department": "engineering",
            "allowed_roles": json.dumps(["engineering_lead"]),
        },
    ]
