import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import json

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RideOps | Support Operations Console",
    page_icon="https://img.icons8.com/fluency-systems-filled/48/FF9900/taxi.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ENTERPRISE DESIGN SYSTEM (AWS / AMAZON INTERNAL OPS CONSOLE INSPIRED)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Canvas */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0F172A;
    }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #F4F6F9 !important;
        color: #0F172A !important;
    }

    /* Hide default Streamlit branding & menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Top Enterprise Navbar */
    .top-nav {
        background-color: #161E2D;
        color: #FFFFFF;
        padding: 12px 24px;
        border-radius: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
        border-bottom: 3px solid #FF9900;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .top-nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-badge {
        background-color: #FF9900;
        color: #161E2D;
        font-weight: 700;
        font-size: 11px;
        padding: 2px 7px;
        border-radius: 3px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .brand-title {
        font-size: 16px;
        font-weight: 600;
        letter-spacing: -0.2px;
        color: #F8FAFC !important;
    }
    .brand-sub {
        font-size: 12px;
        color: #94A3B8 !important;
        border-left: 1px solid #334155;
        padding-left: 12px;
    }
    .top-nav-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #CBD5E1 !important;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #CBD5E1 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }

    /* FORCE HIGH-CONTRAST LIGHT MODE ON ALL NATIVE STREAMLIT TEXT & WIDGETS */
    label, .stRadio label p, .stCheckbox label p, .stSelectbox label p, .stTextInput label p, .stTextArea label p,
    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
    }
    [data-testid="stCaptionContainer"] p {
        color: #475569 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] div {
        color: #0F172A !important;
    }

    /* Clean White Inputs & Dropdowns */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
    }
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    ul[role="listbox"] li {
        color: #0F172A !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: #F8FAFC !important;
        border: 1px dashed #94A3B8 !important;
        color: #0F172A !important;
    }
    [data-testid="stFileUploaderDropzone"] * {
        color: #0F172A !important;
    }

    /* KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 18px;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 14px 18px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #475569 !important;
        margin-bottom: 6px;
    }
    .kpi-val {
        font-size: 24px;
        font-weight: 700;
        color: #0F172A !important;
        line-height: 1.1;
    }
    .kpi-delta-bad {
        font-size: 11px;
        font-weight: 600;
        color: #B91C1C !important;
        margin-top: 5px;
    }
    .kpi-delta-good {
        font-size: 11px;
        font-weight: 600;
        color: #047857 !important;
        margin-top: 5px;
    }
    .kpi-delta-neutral {
        font-size: 11px;
        font-weight: 500;
        color: #475569 !important;
        margin-top: 5px;
    }

    /* Clean White Surface Panels */
    .ops-panel {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }
    .panel-header {
        font-size: 14px;
        font-weight: 600;
        color: #0F172A !important;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 10px;
        margin-bottom: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Priority & Status Pills */
    .pill {
        display: inline-block;
        padding: 2px 8px;
        font-size: 11px;
        font-weight: 600;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }
    .pill-p1 { background: #FEE2E2; color: #991B1B !important; border: 1px solid #FCA5A5; }
    .pill-p2 { background: #FFEDD5; color: #9A3412 !important; border: 1px solid #FDBA74; }
    .pill-p3 { background: #E0F2FE; color: #075985 !important; border: 1px solid #7DD3FC; }
    .pill-p4 { background: #F1F5F9; color: #334155 !important; border: 1px solid #CBD5E1; }
    .pill-tag { background: #F8FAFC; color: #1E293B !important; border: 1px solid #CBD5E1; font-family: 'Inter', sans-serif; font-weight: 500; }

    /* Enterprise Alert Banners */
    .banner-warn {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 4px solid #D97706;
        padding: 12px 14px;
        border-radius: 4px;
        font-size: 13px;
        color: #78350F !important;
        margin-bottom: 12px;
    }
    .banner-danger {
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        border-left: 4px solid #DC2626;
        padding: 12px 14px;
        border-radius: 4px;
        font-size: 13px;
        color: #7F1D1D !important;
        margin-bottom: 12px;
    }
    .banner-success {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-left: 4px solid #059669;
        padding: 12px 14px;
        border-radius: 4px;
        font-size: 13px;
        color: #064E3B !important;
        margin-bottom: 12px;
    }

    /* Primary & Disabled Button Contrast */
    .stButton > button[kind="primary"] {
        background-color: #161E2D !important;
        color: #FFFFFF !important;
        border: 1px solid #161E2D !important;
        font-weight: 600;
        font-size: 13px;
        border-radius: 4px;
        padding: 8px 16px;
    }
    .stButton > button[kind="primary"] p {
        color: #FFFFFF !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #232F3E !important;
        border-color: #FF9900 !important;
    }
    .stButton > button:disabled {
        background-color: #E2E8F0 !important;
        color: #475569 !important;
        border: 1px solid #CBD5E1 !important;
        opacity: 1 !important;
    }
    .stButton > button:disabled p {
        color: #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING & PREPROCESSING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("rideops_support_tickets.csv")
    
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["first_response_at"] = pd.to_datetime(df["first_response_at"])
    df["first_closed_at"] = pd.to_datetime(df["first_closed_at"])
    df["final_closed_at"] = pd.to_datetime(df["final_closed_at"])
    
    pull_time = pd.to_datetime("2026-09-30 23:59:59")
    df["first_close_hrs"] = (df["first_closed_at"] - df["created_at"]).dt.total_seconds() / 3600.0
    df["final_close_hrs"] = (df["final_closed_at"] - df["created_at"]).dt.total_seconds() / 3600.0
    df["age_hrs"] = np.where(
        df["status"] != "Closed",
        (pull_time - df["created_at"]).dt.total_seconds() / 3600.0,
        df["final_close_hrs"]
    )
    df["month"] = df["created_at"].dt.to_period("M").astype(str)
    return df

# -----------------------------------------------------------------------------
# CATEGORY DIAGNOSTIC PLAYBOOKS
# -----------------------------------------------------------------------------
CATEGORY_PLAYBOOKS = {
    "Roster / booking not syncing": {
        "why_it_fails": "50.9% escalation rate; 55.4% of escalations are non-bugs (Config issues, Insufficient info, Duplicates).",
        "default_sample": "Booking cutoff changed but roster still uses old cutoff",
        "required_checks": [
            "Verified client Booking Cutoff timestamp in Admin Portal -> Shift Config (and flushed stale cutoff cache).",
            "Confirmed booking source (Bulk Excel vs. Ad-hoc UI) and inspected Row-level Import Error Log.",
            "Attached Shift ID, Roster Date, and at least 2 affected Employee IDs.",
            "Verified cancellation did not occur post-roster lock window (requires manual re-publish, not Eng)."
        ],
        "l1_self_serve_fix": """
1. Navigate to **Admin Console -> Client Settings -> Shift & Cutoff Rules**.
2. Execute **Force Sync Roster Cache** if cutoff rules were updated in the last 24h.
3. For cancelled bookings persisting in next-day roster: open **Roster Publisher -> Re-generate Draft** for target shift date.
4. For missing bulk Excel entries: inspect `import_audit.csv` for duplicate Employee IDs or invalid shift codes.
        """,
        "required_fields": ["Shift Date & Time", "Sample Employee ID(s)", "Config Cutoff Timestamp"]
    },
    "Live tracking / GPS incorrect": {
        "why_it_fails": "55.7% escalation rate (highest across RideOps); 52.8% returned due to missing Trip IDs or device GPS settings.",
        "default_sample": "Cab location frozen on map for last 20 mins",
        "required_checks": [
            "Verified Driver App telemetry heartbeat & GPS permission status in Fleet Monitor.",
            "Confirmed Trip ID is active (IN_PROGRESS) and boarding OTP was validated.",
            "Checked whether security tracking link failure is due to expired 12h token or corporate firewall.",
            "Captured Trip ID, Vehicle Registration No., Driver ID, and exact timestamp of GPS anomaly."
        ],
        "l1_self_serve_fix": """
1. Open **Fleet Live Monitor -> Search Vehicle/Trip ID -> Telemetry Ping**.
2. If last GPS ping > 5 mins old, trigger **SMS Location Refresh** and coordinate with vendor supervisor.
3. For expired security team tracking links: regenerate **Public Share Token** under *Trip Actions -> Share Live Link*.
        """,
        "required_fields": ["Trip ID", "Vehicle / Driver ID", "Anomaly Timestamp (IST)"]
    },
    "Report export failing": {
        "why_it_fails": "37.4% escalation rate; 29.9% of escalations are Duplicates of Known Issues (>15-day timeout & scheduled email cron).",
        "default_sample": "Monthly trip report download stuck at loading",
        "required_checks": [
            "Confirmed ticket is NOT a duplicate of active batch-export incident (ENG-4512).",
            "Tested export with date range <= 15 days (synchronous query cap).",
            "Verified client admin email domain whitelist / SPF logs for scheduled report delivery.",
            "Captured Report Name, Exact Date Range, and Request/Correlation ID."
        ],
        "l1_self_serve_fix": """
1. For **Monthly report stuck / >15 days fails**: export two 15-day batches (1st–15th and 16th–30th) while `ENG-4512` async batching ships.
2. For **Scheduled report not received**: open *Reports -> Schedules -> Re-verify Recipient* and click **Run Now**.
3. For **Blank billing Excel**: confirm billing cycle status is `FINALIZED` (draft cycles export blank).
        """,
        "required_fields": ["Report Type", "Date Range", "Export Format (CSV/XLSX)"]
    },
    "OTP / boarding issue": {
        "why_it_fails": "35.8% escalation rate; 61.8% are non-bugs (SMS DND blocks, driver offline, or geofence mismatch).",
        "default_sample": "OTP shown as invalid on driver app",
        "required_checks": [
            "Checked SMS Gateway delivery log for Employee Phone Number (ruled out DND / carrier block).",
            "Verified Driver App version >= v4.18 and vehicle location within 200m pickup geofence.",
            "Attached Trip ID, Employee ID, and OTP generation timestamp."
        ],
        "l1_self_serve_fix": """
1. Open **Trip Live Console -> Boarding Override** to manually confirm employee boarding with transport admin.
2. Enable **Dual-Channel OTP (App Push + SMS)** in Client Notification Config for carrier-blocked numbers.
        """,
        "required_fields": ["Trip ID", "Employee ID", "OTP Timestamp (IST)"]
    },
    "Billing / invoice discrepancy": {
        "why_it_fails": "29.5% escalation rate; median 39.6h resolution. Majority are unverified rate cards or cancellation rules.",
        "default_sample": "Invoice trip count does not match our records",
        "required_checks": [
            "Cross-checked Client Contract Rate Card effective date against Invoice Billing Period.",
            "Verified cancelled trip timestamps against free-cancellation cutoff window (dead-km rule).",
            "Attached Invoice ID, Disputed Trip IDs, and expected vs. billed variance."
        ],
        "l1_self_serve_fix": """
1. Open **Billing -> Rate Cards -> Audit Log** and verify new vendor rate card status is `ACTIVE`.
2. For duplicate toll or grace-period dead-km disputes, generate a **Credit Note Draft** for Finance sign-off.
        """,
        "required_fields": ["Invoice Number", "Disputed Trip ID(s)", "Rate Card ID"]
    }
}

DEFAULT_PLAYBOOK = {
    "why_it_fails": "L1 resolves >85% of tickets in this category directly via Admin Config & SOPs without Engineering.",
    "default_sample": "New admin unable to log in to dashboard",
    "required_checks": [
        "Reproduced issue or verified configuration state in Admin Console.",
        "Confirmed request is not a feature request (route feature requests to Product Backlog, not Eng Jira).",
        "Attached Client ID, affected User/Trip ID, and error screenshot/log."
    ],
    "l1_self_serve_fix": """
1. Inspect **Client Admin Config** for role permissions, shift rules, or geocode pin overrides.
2. Tag feature requests under `Product-Backlog` and share current workaround with client admin.
    """,
    "required_fields": ["Client ID", "Affected Entity ID", "Error / Log Reference"]
}

if "triaged_tickets" not in st.session_state:
    st.session_state.triaged_tickets = {}

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### RIDEOPS INTERNAL OPS")
    st.caption("Support Triage & Escalation Control")
    
    page = st.radio(
        "NAVIGATION",
        [
            "L1 Triage Gatekeeper",
            "Lead Backlog & Quality Radar",
            "Executive Diagnosis & Roadmap"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    uploaded = st.file_uploader("Data Source (CSV Override)", type=["csv"])
    df = load_data(uploaded)
    
    open_df = df[df["status"] != "Closed"]
    triaged_closed = sum(1 for v in st.session_state.triaged_tickets.values() if v["action"] == "Resolved at L1")
    effective_open = len(open_df) - triaged_closed
    
    st.divider()
    st.markdown("**LIVE QUEUE TELEMETRY**")
    st.metric("Open Backlog", f"{effective_open}", delta=f"-{triaged_closed} in session" if triaged_closed else "+60% vs Jul (30)", delta_color="normal" if triaged_closed else "inverse")
    st.metric("Non-Bug Escalations", "56.6%", delta="Target < 25.0%", delta_color="inverse")
    st.metric("Ping-Pong Rate (>=2 Handoffs)", "47.1%", delta="Target < 15.0%", delta_color="inverse")

# -----------------------------------------------------------------------------
# TOP ENTERPRISE HEADER BAR
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="top-nav">
    <div class="top-nav-brand">
        <span class="brand-badge">RIDEOPS OPS</span>
        <span class="brand-title">Support Triage & Escalation Gatekeeper</span>
        <span class="brand-sub">Production Control Console • v0.9</span>
    </div>
    <div class="top-nav-meta">
        <span><span class="status-dot"></span>DATASET: 1,444 TICKETS (JUL–SEP 2026)</span>
        <span>REGION: AP-SOUTH-1 (IST)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# VIEW 1: L1 TRIAGE GATEKEEPER
# -----------------------------------------------------------------------------
if page == "L1 Triage Gatekeeper":
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Active Open Queue</div>
            <div class="kpi-val">{effective_open} Tickets</div>
            <div class="kpi-delta-bad">34 Escalated (70.8%) • 14 L1</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Escalation Resolution Median</div>
            <div class="kpi-val">86.8 hrs</div>
            <div class="kpi-delta-bad">6.9x slower than L1 (12.6 hrs)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Invalid Escalation Rate</div>
            <div class="kpi-val">56.6%</div>
            <div class="kpi-delta-bad">275 / 486 returned or non-bugs</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">3-Handoff CSAT Penalty</div>
            <div class="kpi-val">2.10 / 5.0</div>
            <div class="kpi-delta-neutral">Down from 4.01 (Non-Escalated)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Intake Source",
        ["Live Open Queue (48 Tickets)", "New Incoming Ticket Simulation"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if mode == "Live Open Queue (48 Tickets)":
        with st.container(border=True):
            open_queue = df[df["status"] != "Closed"].sort_values(by=["priority", "age_hrs"], ascending=[True, False])
            c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 2.4])
            with c1:
                cat_filter = st.selectbox("Category", ["All Categories"] + sorted(open_queue["category"].unique().tolist()))
            with c2:
                status_filter = st.selectbox("Queue Status", ["All Statuses"] + sorted(open_queue["status"].unique().tolist()))
            with c3:
                agent_filter = st.selectbox("Owner", ["All Agents"] + sorted(open_queue["assigned_agent"].unique().tolist()))
                
            filtered_q = open_queue.copy()
            if cat_filter != "All Categories":
                filtered_q = filtered_q[filtered_q["category"] == cat_filter]
            if status_filter != "All Statuses":
                filtered_q = filtered_q[filtered_q["status"] == status_filter]
            if agent_filter != "All Agents":
                filtered_q = filtered_q[filtered_q["assigned_agent"] == agent_filter]
                
            if len(filtered_q) == 0:
                st.info("No open tickets match current filters.")
                st.stop()
                
            with c4:
                ticket_options = [
                    f"{row.ticket_id}  |  {row.priority}  |  {row.client_name}  —  {row.description[:48]} ({row.age_hrs:.0f}h)"
                    for _, row in filtered_q.iterrows()
                ]
                selected_label = st.selectbox("Select Active Ticket", ticket_options)
                selected_id = selected_label.split("  |  ")[0]
                ticket = df[df["ticket_id"] == selected_id].iloc[0].to_dict()
    else:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([1.4, 1.6, 0.8, 1.0])
            with c1:
                new_client = st.selectbox("Corporate Client", sorted(df["client_name"].unique().tolist()))
            with c2:
                new_cat = st.selectbox("Issue Category", sorted(df["category"].unique().tolist()))
            with c3:
                new_prio = st.selectbox("Severity", ["P1", "P2", "P3", "P4"], index=1)
            with c4:
                new_chan = st.selectbox("Channel", ["WhatsApp", "Phone", "Email", "Client portal"])
            
            default_desc = CATEGORY_PLAYBOOKS.get(new_cat, DEFAULT_PLAYBOOK)["default_sample"]
            new_desc = st.text_input("Client Issue Summary", value=default_desc)
            ticket = {
                "ticket_id": "SUP-11445",
                "created_at": pd.to_datetime("2026-10-01 09:00:00"),
                "channel": new_chan,
                "client_id": "CL-SIM",
                "client_name": new_client,
                "client_tier": "Enterprise",
                "category": new_cat,
                "priority": new_prio,
                "description": new_desc,
                "assigned_agent": "L1 Desk",
                "escalated_to_eng": "No",
                "eng_ticket_id": np.nan,
                "eng_handoffs": 0,
                "eng_outcome": np.nan,
                "status": "Open - with L1",
                "reopen_count": 0,
                "age_hrs": 0.4
            }

    left_col, right_col = st.columns([1.1, 1.35], gap="medium")
    
    with left_col:
        prio_cls = f"pill-{ticket['priority'].lower()}"
        st.markdown(f"""
        <div class="ops-panel">
            <div class="panel-header">
                <span>TICKET RECORD: <code>{ticket['ticket_id']}</code> • {ticket['client_name']}</span>
                <span class="pill {prio_cls}">{ticket['priority']}</span>
            </div>
            <div style="margin-bottom: 12px; display: flex; flex-wrap: wrap; gap: 6px;">
                <span class="pill pill-tag">Category: {ticket['category']}</span>
                <span class="pill pill-tag">Channel: {ticket['channel']}</span>
                <span class="pill pill-tag">Tier: {ticket['client_tier']}</span>
                <span class="pill pill-tag">Owner: {ticket['assigned_agent']}</span>
                <span class="pill pill-tag">Age: {ticket['age_hrs']:.1f}h</span>
                <span class="pill pill-tag">Handoffs: {int(ticket['eng_handoffs'])}</span>
            </div>
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:12px; border-radius:4px; font-size:13.5px; color:#0F172A;">
                <strong>Reported Issue:</strong> {ticket['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if pd.notna(ticket["eng_outcome"]):
            if ticket["eng_outcome"] == "Fixed":
                st.markdown(f"""
                <div class="banner-success">
                    <strong>ACTION REQUIRED — RESOLVED BY ENGINEERING ({ticket['eng_ticket_id']}):</strong><br>
                    Engineering has marked this issue <strong>Fixed</strong>. Confirm resolution with {ticket['client_name']} and close immediately to clear backlog.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="banner-danger">
                    <strong>RETURNED BY ENGINEERING ({ticket['eng_ticket_id']}) — {ticket['eng_outcome'].upper()}:</strong><br>
                    Do not re-escalate until all L1 verification gates and diagnostic IDs are completed.
                </div>
                """, unsafe_allow_html=True)

        similar_df = df[
            (df["category"] == ticket["category"]) &
            (df["ticket_id"] != ticket["ticket_id"]) &
            (df["eng_ticket_id"].notna())
        ]
        desc_prefix = str(ticket["description"])[:22].lower()
        exact_matches = similar_df[similar_df["description"].str.lower().str.startswith(desc_prefix)]
        
        if len(exact_matches) > 0:
            recent_match = exact_matches.sort_values("created_at", ascending=False).iloc[0]
            dup_count = (exact_matches["eng_outcome"] == "Duplicate of known issue").sum()
            cfg_count = (exact_matches["eng_outcome"] == "Config issue - returned to L1").sum()
            st.markdown(f"""
            <div class="banner-warn">
                <strong>KNOWN INCIDENT MATCH ({len(exact_matches)} historical escalations):</strong><br>
                Master Reference: <code>{recent_match['eng_ticket_id']}</code> (Latest Outcome: <strong>{recent_match['eng_outcome']}</strong>)<br>
                Historical Disposition: <strong>{cfg_count}</strong> Config Issues • <strong>{dup_count}</strong> Duplicates.<br>
                <span style="font-size:12px;">Recommendation: Apply L1 Runbook below or link to master incident instead of opening a new Eng ticket.</span>
            </div>
            """, unsafe_allow_html=True)

        playbook = CATEGORY_PLAYBOOKS.get(ticket["category"], DEFAULT_PLAYBOOK)
        with st.container(border=True):
            st.markdown("**L1 SELF-SERVE RESOLUTION RUNBOOK**")
            st.caption(playbook["why_it_fails"])
            st.markdown(playbook["l1_self_serve_fix"])

    with right_col:
        with st.container(border=True):
            st.markdown("**PRE-ESCALATION DIAGNOSTIC GATEKEEPER**")
            st.caption("Mandatory verification required before Engineering handoff is unlocked.")
            
            st.markdown("##### 1. Configuration & Telemetry Verification")
            checks_passed = []
            for idx, chk in enumerate(playbook["required_checks"]):
                val = st.checkbox(chk, key=f"chk_{ticket['ticket_id']}_{idx}")
                checks_passed.append(val)
                
            st.markdown("##### 2. Mandatory Diagnostic Identifiers")
            field_values = {}
            f_cols = st.columns(len(playbook["required_fields"]))
            for idx, fname in enumerate(playbook["required_fields"]):
                with f_cols[idx]:
                    field_values[fname] = st.text_input(fname, key=f"fld_{ticket['ticket_id']}_{idx}", placeholder="Required")
                    
            st.markdown("##### 3. L1 Investigation Log")
            agent_notes = st.text_area(
                "Verification Notes",
                key=f"notes_{ticket['ticket_id']}",
                height=85,
                placeholder="Document Admin Config state, cache refresh result, and reproduction steps..."
            )
            
            all_checked = all(checks_passed)
            all_fields_filled = all(len(v.strip()) > 0 for v in field_values.values())
            can_escalate = all_checked and all_fields_filled and len(agent_notes.strip()) >= 10
            
            st.divider()
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Resolve & Close at L1", type="primary", use_container_width=True):
                    st.session_state.triaged_tickets[ticket["ticket_id"]] = {
                        "action": "Resolved at L1",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    st.success(f"Closed {ticket['ticket_id']} at L1. Open backlog decremented.")
            with b2:
                btn_text = "Submit Validated Eng Handoff" if can_escalate else "Escalation Locked (Complete Gate)"
                if st.button(btn_text, disabled=not can_escalate, use_container_width=True):
                    st.session_state.triaged_tickets[ticket["ticket_id"]] = {
                        "action": "Validated Escalation",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    handoff_payload = {
                        "ticket_id": ticket["ticket_id"],
                        "client": f"{ticket['client_name']} ({ticket['client_tier']})",
                        "priority": ticket["priority"],
                        "category": ticket["category"],
                        "gate_verified": True,
                        "identifiers": field_values,
                        "l1_notes": agent_notes
                    }
                    st.success("Gate passed. Structured Engineering handoff generated:")
                    st.code(json.dumps(handoff_payload, indent=2), language="json")
                    
            if not can_escalate:
                missing = []
                if not all_checked:
                    missing.append(f"{sum(not c for c in checks_passed)} checklist items")
                if not all_fields_filled:
                    missing.append("diagnostic IDs")
                if len(agent_notes.strip()) < 10:
                    missing.append("investigation notes")
                st.caption(f"Gate Status: **LOCKED** — Pending {', '.join(missing)}.")

# -----------------------------------------------------------------------------
# VIEW 2: LEAD BACKLOG & QUALITY RADAR
# -----------------------------------------------------------------------------
elif page == "Lead Backlog & Quality Radar":
    open_df = df[df["status"] != "Closed"].copy()
    already_processed = open_df[open_df["eng_outcome"].notna()]
    
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Open Backlog</div>
            <div class="kpi-val">{len(open_df)} Tickets</div>
            <div class="kpi-delta-bad">+60.0% since Jul 31 (30 → 48)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Stale Post-Eng Tickets</div>
            <div class="kpi-val">{len(already_processed)} Tickets</div>
            <div class="kpi-delta-good">Immediate Day-1 burn-down (-42%)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Aged Open (> 48 hrs)</div>
            <div class="kpi-val">{int((open_df['age_hrs'] > 48).sum())} Tickets</div>
            <div class="kpi-delta-bad">54.2% of active open queue</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Overall Reopen Rate</div>
            <div class="kpi-val">{(df['reopen_count'] > 0).mean()*100:.1f}%</div>
            <div class="kpi-delta-bad">Karan B outlier at 29.5%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("**PRIORITY BURN-DOWN QUEUE: 20 OPEN TICKETS ALREADY PROCESSED BY ENGINEERING**")
        st.caption("These 20 tickets already have a completed Engineering verdict (`Fixed` or `Returned to L1`) sitting unclosed in L1's queue.")
        display_cols = ["ticket_id", "priority", "client_name", "category", "assigned_agent", "status", "eng_ticket_id", "eng_outcome", "eng_handoffs", "age_hrs"]
        st.dataframe(
            already_processed[display_cols].sort_values("age_hrs", ascending=False).style.format({"age_hrs": "{:.1f}h"}),
            use_container_width=True,
            hide_index=True
        )

    with st.container(border=True):
        st.markdown("**L1 AGENT QUALITY & CALIBRATION MATRIX**")
        st.caption("Exposing hidden failure modes: Premature closures (Karan B) vs. Over-escalation without config checks (Rahul T).")
        
        agent_summary = df.groupby("assigned_agent").agg(
            Tickets=("ticket_id", "count"),
            Open=("status", lambda x: (x != "Closed").sum()),
            Esc_Rate=("escalated_to_eng", lambda x: round((x == "Yes").mean() * 100, 1)),
            Invalid_Esc_Rate=("eng_outcome", lambda x: round((x[x.notna()] != "Fixed").mean() * 100, 1)),
            First_Close_Hrs=("first_close_hrs", lambda x: round(x.median(), 1)),
            Final_Close_Hrs=("final_close_hrs", lambda x: round(x.median(), 1)),
            Reopen_Rate=("reopen_count", lambda x: round((x > 0).mean() * 100, 1)),
            CSAT=("csat_score", lambda x: round(x.mean(), 2))
        ).reset_index()
        
        def flag_coaching(row):
            if row["Reopen_Rate"] > 15:
                return "CRITICAL: Premature Closures"
            elif row["Invalid_Esc_Rate"] > 65:
                return "HIGH: Over-Escalation"
            return "NORMAL"
            
        agent_summary["Audit_Flag"] = agent_summary.apply(flag_coaching, axis=1)
        st.dataframe(agent_summary, use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        with c1:
            chart1 = alt.Chart(agent_summary).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
                x=alt.X("assigned_agent:N", title="Agent", sort="-y"),
                y=alt.Y("Reopen_Rate:Q", title="Reopen Rate (%)"),
                color=alt.condition(alt.datum.Reopen_Rate > 15, alt.value("#DC2626"), alt.value("#1E293B")),
                tooltip=["assigned_agent", "Reopen_Rate", "CSAT"]
            ).properties(height=240, title="Ticket Reopen Rate (%) by Agent")
            st.altair_chart(chart1, use_container_width=True)
            
        with c2:
            chart2 = alt.Chart(agent_summary).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
                x=alt.X("assigned_agent:N", title="Agent", sort="-y"),
                y=alt.Y("Invalid_Esc_Rate:Q", title="Invalid Escalation Rate (%)"),
                color=alt.condition(alt.datum.Invalid_Esc_Rate > 65, alt.value("#D97706"), alt.value("#1E293B")),
                tooltip=["assigned_agent", "Invalid_Esc_Rate", "Esc_Rate"]
            ).properties(height=240, title="Non-Bug / Returned Escalation Rate (%) by Agent")
            st.altair_chart(chart2, use_container_width=True)

# -----------------------------------------------------------------------------
# VIEW 3: EXECUTIVE DIAGNOSIS & ROADMAP
# -----------------------------------------------------------------------------
elif page == "Executive Diagnosis & Roadmap":
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        with st.container(border=True):
            st.markdown("**1. EVIDENCE-BASED ROOT CAUSE DIAGNOSIS**")
            st.markdown("""
            - **Backlog Composition (+60% Jul → Sep):** Open tickets rose from **30** (Jul 31) to **48** (Sep 30). **70.8% (34/48)** sit in Engineering escalations; **62.5% (30/48)** are concentrated in *Roster / booking sync* (17) and *Live tracking / GPS* (13).
            - **56.6% Non-Bug Escalation Waste:** Out of **486 escalations**, only **211 (43.4%)** required a code fix (`Fixed`). **275 (56.6%)** were `Insufficient info` (18.3%), `Config issue` (17.3%), `Duplicate` (11.5%), `How-to` (4.9%), or `Not reproducible` (4.5%).
            - **Ping-Pong Latency Multiplier:** **47.1% (229/486)** bounced ≥2 times between L1 and Engineering. Resolution degrades from **58.7h** (1 handoff, 3.56 CSAT) to **110.4h** (2 handoffs, 2.80 CSAT) and **169.9h** (3 handoffs, 2.10 CSAT).
            - **Premature Closure Distortion:** Karan B closes non-escalated tickets in **6.4h** (vs. ~12.5h peers) but triggers a **29.5% reopen rate**, pushing reopened tickets to **53.7h** and **2.00 CSAT**.
            """)
    with c2:
        with st.container(border=True):
            st.markdown("**2. WEEKLY SUCCESS SCORECARD & GUARDRAILS**")
            metrics_df = pd.DataFrame([
                {"Metric": "Aged Open Tickets (> 48h)", "Baseline": "26", "4-Wk Target": "< 10 (-62%)"},
                {"Metric": "Total Open Tickets (EOW)", "Baseline": "48", "4-Wk Target": "< 25 (-48%)"},
                {"Metric": "Invalid Escalation Rate", "Baseline": "56.6%", "4-Wk Target": "< 25.0%"},
                {"Metric": "Multi-Handoff Ping-Pong Rate", "Baseline": "47.1%", "4-Wk Target": "< 15.0%"},
                {"Metric": "Ticket Reopen Rate (Guardrail)", "Baseline": "10.5%", "4-Wk Target": "< 7.0%"},
                {"Metric": "Client CSAT (Guardrail)", "Baseline": "3.70", "4-Wk Target": ">= 4.10"}
            ])
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)

            st.markdown("**3. DELIBERATE NON-GOALS**")
            st.markdown("""
            - **No New L1 Hires:** Zero budget; adding L1 headcount without an escalation gate merely floods Engineering faster.
            - **No Ticketing CRM Migration:** Avoids a 4+ week replatforming delay; lightweight gatekeeper layer integrates immediately.
            - **No Auto-Closure Rules:** Artificially depresses open counts while spiking reopens and eroding enterprise trust.
            """)

    with st.container(border=True):
        st.markdown("**4. FOUR-WEEK EXECUTION ROADMAP**")
        roadmap_df = pd.DataFrame([
            {"Timeline": "Week 1", "Workstream": "Queue Burn-Down & Gatekeeper Rollout", "Deliverables": "Action 20 stale post-Eng open tickets (-42% backlog Day 1); mandate Gatekeeper for Roster Sync, GPS & Report Exports; 1:1 calibration with Karan B & Rahul T."},
            {"Timeline": "Week 2", "Workstream": "Known-Incident Sync & L1 Config Access", "Deliverables": "Pin master ENG incidents to cut the 11.5% duplicate escalations; grant L1 direct roster cutoff-cache flush & scheduled report re-run permissions."},
            {"Timeline": "Week 3", "Workstream": "Structured Intake & SLA Aging Alerts", "Deliverables": "Enforce mandatory Trip/Employee/Shift IDs on WhatsApp & Phone intake; deploy 24h/48h alerts on Engineering-returned tickets."},
            {"Timeline": "Week 4", "Workstream": "Top-3 Engineering Root-Cause Fixes", "Deliverables": "Prioritize permanent fixes by ticket volume: (1) Cutoff cache invalidation, (2) Cancelled trips persisting in roster, (3) Async >15-day report export."}
        ])
        st.dataframe(roadmap_df, use_container_width=True, hide_index=True)
