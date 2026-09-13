import os
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st  # type: ignore[import-not-found]
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CityRide 360 | Microsoft Fabric Portfolio",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

def setting(name: str) -> str:
    # Environment variables work locally/most hosting platforms; Streamlit secrets work on Community Cloud.
    value = os.getenv(name, "")
    if value:
        return value
    try:
        return str(st.secrets.get(name, ""))
    except Exception:
        return ""

GITHUB_URL = setting("CITYRIDE_GITHUB_URL")
POWERBI_URL = setting("CITYRIDE_POWERBI_URL")
VIDEO_URL = setting("CITYRIDE_VIDEO_URL")
CONTACT_URL = setting("CITYRIDE_CONTACT_URL")

st.markdown(
    """
<style>
.block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1280px;}
.hero {padding: 2.2rem 2.4rem; border: 1px solid rgba(128,128,128,.25); border-radius: 18px; margin-bottom: 1.5rem;}
.eyebrow {text-transform: uppercase; letter-spacing: .12em; font-size: .78rem; opacity: .7; margin-bottom: .5rem;}
.hero h1 {font-size: 3rem; margin: 0 0 .6rem 0;}
.hero p {font-size: 1.12rem; opacity: .85; max-width: 900px;}
.tag {display:inline-block; padding:.28rem .65rem; margin:.18rem .16rem .18rem 0; border:1px solid rgba(128,128,128,.35); border-radius:999px; font-size:.82rem;}
.section-note {padding:.8rem 1rem; border-left:4px solid rgba(128,128,128,.45); background:rgba(128,128,128,.06); border-radius:8px;}
</style>
""",
    unsafe_allow_html=True,
)

@st.cache_data
def make_demo_data(seed: int = 42, n_days: int = 45):
    rng = np.random.default_rng(seed)
    start = pd.Timestamp.today().normalize() - pd.Timedelta(days=n_days - 1)
    dates = pd.date_range(start, periods=n_days, freq="D")
    trips = rng.integers(6200, 11200, size=n_days)
    avg_fare = rng.normal(24.5, 2.2, size=n_days).clip(17, 34)
    revenue = trips * avg_fare
    avg_distance = rng.normal(5.7, 0.65, size=n_days).clip(3.8, 8.2)
    daily = pd.DataFrame({"date": dates, "trips": trips, "revenue": revenue, "avg_fare": avg_fare, "avg_distance": avg_distance})
    zones = pd.DataFrame({
        "zone": ["Midtown", "Downtown", "Airport", "Harbor", "Uptown", "West Side"],
        "trips": rng.integers(22000, 65000, size=6),
        "revenue": rng.integers(550000, 1700000, size=6),
        "avg_fare": rng.normal(25, 4, size=6).round(2),
    }).sort_values("trips", ascending=False)
    minutes = pd.date_range(pd.Timestamp.now().floor("min") - pd.Timedelta(minutes=59), periods=60, freq="min")
    realtime = pd.DataFrame({
        "minute": minutes,
        "trips_per_min": rng.integers(35, 120, size=60),
        "avg_live_fare": rng.normal(25, 3, size=60).clip(14, 42),
    })
    return daily, zones, realtime

daily, zones, realtime = make_demo_data()

st.sidebar.title("CityRide 360")
st.sidebar.caption("Microsoft Fabric • DP-700 Portfolio")
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Architecture",
        "Batch Engineering",
        "Real-Time Analytics",
        "Warehouse & BI",
        "Security & DevOps",
        "Monitoring & Optimization",
        "DP-700 Coverage",
        "About the Project",
    ],
)

st.sidebar.divider()
st.sidebar.markdown("**Portfolio links**")
if GITHUB_URL:
    st.sidebar.link_button("GitHub repository", GITHUB_URL, use_container_width=True)
else:
    st.sidebar.caption("Set CITYRIDE_GITHUB_URL to enable the GitHub button.")
if POWERBI_URL:
    st.sidebar.link_button("Live Power BI report", POWERBI_URL, use_container_width=True)
if VIDEO_URL:
    st.sidebar.link_button("Demo video", VIDEO_URL, use_container_width=True)
if CONTACT_URL:
    st.sidebar.link_button("Contact", CONTACT_URL, use_container_width=True)

st.sidebar.divider()
st.sidebar.caption("Public demo uses synthetic data. Keep the Fabric backend private/authenticated.")


def tags(items):
    html = "".join([f'<span class="tag">{item}</span>' for item in items])
    st.markdown(html, unsafe_allow_html=True)


def metric_row():
    last = daily.iloc[-1]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Trips", f"{int(last.trips):,}")
    c2.metric("Revenue", f"${last.revenue:,.0f}")
    c3.metric("Average Fare", f"${last.avg_fare:,.2f}")
    c4.metric("Average Distance", f"{last.avg_distance:,.1f} mi")


def show_code(title, code, language):
    st.markdown(f"#### {title}")
    st.code(code.strip(), language=language)


if page == "Overview":
    st.markdown(
        """
<div class="hero">
    <div class="eyebrow">End-to-End Data Engineering Portfolio</div>
    <h1>🚕 CityRide 360</h1>
    <p>
    A Microsoft Fabric data platform combining batch ingestion, medallion Lakehouse design,
    dimensional warehousing, real-time event processing, security, CI/CD, monitoring,
    and performance optimization. Built as a hands-on project aligned to DP-700.
    </p>
</div>
""",
        unsafe_allow_html=True,
    )
    tags(["Microsoft Fabric", "OneLake", "Lakehouse", "Delta Lake", "PySpark", "Data Factory", "Warehouse", "T-SQL", "Eventstream", "Eventhouse", "KQL", "Power BI", "Git", "Deployment Pipelines"])
    st.subheader("Business scenario")
    st.markdown("CityRide is a fictional urban mobility company. Operations needs near-real-time visibility into active trip demand, while management needs reliable historical analytics across zones, fares, distance, payments, and daily revenue.")
    st.subheader("Public demo")
    metric_row()
    c1, c2 = st.columns([1.45, 1])
    with c1:
        st.line_chart(daily.set_index("date")[["trips", "revenue"]])
    with c2:
        st.bar_chart(zones.set_index("zone")[["trips"]])
    st.markdown('<div class="section-note"><b>Portfolio pattern:</b> Streamlit is the public presentation layer. Fabric engineering workspaces stay private. Recruiters can inspect the architecture, source code, documentation, screenshots, and interactive demo without needing Fabric access.</div>', unsafe_allow_html=True)

elif page == "Architecture":
    st.title("Architecture")
    arch = Path(__file__).parent / "assets" / "architecture.png"
    if arch.exists():
        st.image(str(arch), use_container_width=True)
    else:
        st.info("Add your architecture image at assets/architecture.png.")
    st.markdown("""
### Logical flow

**Batch path**  
Historical trip files → Fabric Pipeline → Bronze Lakehouse → PySpark → Silver/Gold → Warehouse → Power BI

**Operational reference path**  
Fabric SQL Database → Mirroring / OneLake → Lakehouse / Warehouse

**Real-time path**  
Yellow Taxi sample stream → Eventstream → Eventhouse + Spark Structured Streaming → Lakehouse → monitoring

**Lifecycle path**  
GitHub → DEV → Deployment Pipeline → TEST → PROD
""")
    decisions = pd.DataFrame([
        ["Lakehouse", "Flexible Delta engineering layer for Bronze/Silver/Gold transformations."],
        ["Warehouse", "Relational star schema and T-SQL analytics for governed BI consumption."],
        ["Eventhouse", "Low-latency event/time-series analytics using KQL."],
        ["OneLake shortcuts", "Reuse governed data without unnecessary copies."],
        ["Streamlit", "Public portfolio layer independent of Fabric tenant access."],
    ], columns=["Decision", "Why"])
    st.subheader("Key design decisions")
    st.dataframe(decisions, use_container_width=True, hide_index=True)

elif page == "Batch Engineering":
    st.title("Batch Engineering")
    st.markdown("The batch pipeline loads historical taxi trips incrementally and transforms them through Bronze → Silver → Gold.")
    st.subheader("Pipeline sequence")
    st.code("""Lookup previous watermark
        ↓
Copy new trip records
        ↓
Dataflow Gen2: clean zone reference data
        ↓
PySpark notebook: clean / deduplicate / enrich
        ↓
Write Silver + Gold Delta tables
        ↓
Load Fabric Warehouse
        ↓
Update watermark""")
    show_code("Incremental-load predicate", """pickup_datetime > previous_watermark
AND pickup_datetime <= current_watermark""", "sql")
    show_code("PySpark Silver transformation", """
from pyspark.sql import functions as F

raw = spark.read.table("raw_trips")

silver = (
    raw
    .dropDuplicates(["trip_id"])
    .filter(F.col("pickup_datetime").isNotNull())
    .filter(F.col("total_amount") >= 0)
    .fillna({"passenger_count": 1})
    .withColumn("trip_date", F.to_date("pickup_datetime"))
    .withColumn(
        "trip_minutes",
        (F.unix_timestamp("dropoff_datetime") - F.unix_timestamp("pickup_datetime")) / 60.0
    )
    .withColumn(
        "revenue_per_mile",
        F.when(F.col("trip_distance") > 0, F.col("total_amount") / F.col("trip_distance"))
    )
)

silver.write.mode("overwrite").format("delta").saveAsTable("trips_clean")
""", "python")
    show_code("PySpark Gold aggregation", """
gold = (
    silver
    .groupBy("trip_date", "pickup_zone")
    .agg(
        F.count("*").alias("trip_count"),
        F.sum("total_amount").alias("revenue"),
        F.avg("total_amount").alias("avg_fare"),
        F.avg("trip_distance").alias("avg_distance"),
    )
)

gold.write.mode("overwrite").format("delta").saveAsTable("daily_zone_metrics")
""", "python")
    st.subheader("DP-700 concepts")
    tags(["Pipelines", "Parameters", "Dynamic expressions", "Incremental ingestion", "Dataflow Gen2", "PySpark", "Delta", "Medallion architecture", "Data cleansing", "Deduplication", "Aggregations"])

elif page == "Real-Time Analytics":
    st.title("Real-Time Analytics")
    st.markdown("The streaming branch uses Eventstream to route taxi events to Eventhouse for KQL analytics and to Spark Structured Streaming for Delta processing.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Trips/min", f"{int(realtime.iloc[-1].trips_per_min)}")
    c2.metric("Avg live fare", f"${realtime.iloc[-1].avg_live_fare:.2f}")
    c3.metric("60-min peak", f"{int(realtime.trips_per_min.max())} trips/min")
    st.line_chart(realtime.set_index("minute")[["trips_per_min"]])
    show_code("KQL: trips and revenue per minute", """
TaxiTrips
| summarize
    Trips = count(),
    Revenue = sum(todouble(total_amount))
  by bin(pickup_datetime, 1m)
| order by pickup_datetime desc
""", "text")
    show_code("KQL: high-value trips", """
TaxiTrips
| where todouble(total_amount) > 50
| project pickup_datetime, dropoff_datetime, trip_distance, total_amount
""", "text")
    show_code("Structured Streaming: 5-minute windows", """
from pyspark.sql import functions as F

events = (
    spark.readStream
    .format("eventhubs")
    .options(**eventhub_options)
    .load()
)

parsed = (
    events
    .withWatermark("event_time", "10 minutes")
    .groupBy(F.window("event_time", "5 minutes"))
    .agg(F.count("*").alias("trips"), F.avg("total_amount").alias("avg_fare"))
)

query = (
    parsed.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path)
    .toTable("stream_trip_metrics")
)
""", "python")
    st.subheader("DP-700 concepts")
    tags(["Eventstream", "Eventhouse", "KQL", "Structured Streaming", "Watermarks", "Windowing", "Late data", "Real-time analytics"])

elif page == "Warehouse & BI":
    st.title("Warehouse & BI")
    st.markdown("Curated Gold data is loaded into a dimensional Fabric Warehouse for analytical consumption.")
    st.code("""                DimDate
                   │
DimPickupZone ─── FactTrip ─── DimDropoffZone
                   │
                DimPayment""")
    show_code("T-SQL: warehouse load pattern", """
MERGE dbo.DimPickupZone AS target
USING (
    SELECT DISTINCT pickup_zone_id, pickup_zone_name
    FROM dbo.StageTrip
) AS source
ON target.PickupZoneId = source.pickup_zone_id
WHEN MATCHED THEN
    UPDATE SET PickupZoneName = source.pickup_zone_name
WHEN NOT MATCHED THEN
    INSERT (PickupZoneId, PickupZoneName)
    VALUES (source.pickup_zone_id, source.pickup_zone_name);
""", "sql")
    show_code("T-SQL: window function", """
SELECT
    PickupZoneKey,
    DateKey,
    TotalAmount,
    SUM(TotalAmount) OVER (
        PARTITION BY PickupZoneKey
        ORDER BY DateKey
    ) AS RunningRevenue
FROM dbo.FactTrip;
""", "sql")
    st.subheader("Interactive BI demo")
    metric_row()
    st.dataframe(zones.style.format({"revenue": "${:,.0f}", "avg_fare": "${:,.2f}"}), use_container_width=True, hide_index=True)
    if POWERBI_URL:
        st.link_button("Open live Power BI report", POWERBI_URL)
    else:
        st.info("Set CITYRIDE_POWERBI_URL to add your Power BI report link.")

elif page == "Security & DevOps":
    st.title("Security & DevOps")
    security = pd.DataFrame([
        ["Workspace", "Admin / Member / Contributor / Viewer"],
        ["Item", "Grant access only to required Fabric items"],
        ["Row-level", "Restrict analysts to authorized zones"],
        ["Column / object", "Protect sensitive driver attributes and tables"],
        ["Dynamic masking", "Mask email or license values"],
        ["OneLake", "Apply data access boundaries to files/tables"],
        ["Governance", "Sensitivity labels and endorsement"],
    ], columns=["Layer", "Implementation"])
    st.subheader("Security layers")
    st.dataframe(security, use_container_width=True, hide_index=True)
    show_code("T-SQL: dynamic masking example", """
CREATE TABLE dbo.DriverSecure (
    DriverId INT,
    FullName VARCHAR(100),
    Email VARCHAR(200) MASKED WITH (FUNCTION = 'email()'),
    LicenseNumber VARCHAR(50)
);
""", "sql")
    st.subheader("CI/CD")
    st.code("""GitHub
  ↓
Fabric DEV
  ↓
Deployment Pipeline
  ↓
TEST
  ↓
PROD""")
    st.markdown("""
Recommended portfolio practice:
- Keep DEV/TEST/PROD Fabric workspaces private.
- Publish source-controlled definitions to GitHub.
- Give technical interviewers Viewer access only when needed.
- Never publish secrets, connection strings, tokens, or real PII.
""")
    tags(["Workspace permissions", "RLS", "CLS", "Masking", "Sensitivity labels", "Git integration", "Deployment pipelines", "DEV/TEST/PROD"])

elif page == "Monitoring & Optimization":
    st.title("Monitoring & Optimization")
    failures = pd.DataFrame([
        ["Pipeline", "Wrong source path", "Pipeline run output", "Correct parameter/path"],
        ["Dataflow Gen2", "Invalid type conversion", "Refresh history", "Fix transform/schema"],
        ["Notebook", "Missing column", "Spark logs", "Correct schema/reference"],
        ["Eventstream", "Bad destination mapping", "Eventstream monitoring", "Correct mapping"],
        ["Eventhouse", "Type mismatch", "KQL ingestion diagnostics", "Fix ingestion mapping"],
        ["Shortcut", "Permission removed", "OneLake diagnostics", "Restore access"],
    ], columns=["Component", "Injected failure", "Diagnose with", "Remediation"])
    st.subheader("Break / fix scenarios")
    st.dataframe(failures, use_container_width=True, hide_index=True)
    show_code("Delta optimization", """OPTIMIZE trips_clean
ZORDER BY (trip_date)
VORDER;""", "sql")
    st.markdown("""
Compare:
- baseline vs optimized Delta file layout,
- standard join vs broadcast join in Spark,
- filtered vs unfiltered Warehouse queries,
- native Eventhouse table vs standard shortcut vs accelerated shortcut,
- pipeline with redundant copies vs simplified orchestration.
""")
    tags(["Monitoring Hub", "Spark diagnostics", "Pipeline troubleshooting", "Query optimization", "Delta OPTIMIZE", "Z-Order", "V-Order", "Eventhouse optimization", "Alerting"])

elif page == "DP-700 Coverage":
    st.title("DP-700 Coverage Matrix")
    coverage = pd.DataFrame([
        ["Manage an analytics solution", "Workspace, domains, settings, Git, deployment pipeline", "Implemented"],
        ["Security & governance", "Workspace/item security, masking, OneLake, labels", "Implemented"],
        ["Batch ingestion", "Fabric Pipeline + watermark incremental loads", "Implemented"],
        ["Dataflow Gen2", "Reference data cleansing", "Implemented"],
        ["Lakehouse engineering", "Bronze / Silver / Gold Delta tables", "Implemented"],
        ["PySpark", "Cleaning, joins, enrichment, aggregation", "Implemented"],
        ["Warehouse", "Star schema and T-SQL loads", "Implemented"],
        ["Mirroring / shortcuts", "Operational data + OneLake reuse", "Implemented"],
        ["Streaming", "Eventstream + Spark Structured Streaming", "Implemented"],
        ["Eventhouse / KQL", "Real-time taxi analytics", "Implemented"],
        ["Monitoring", "Pipelines, Spark, Eventstream, Eventhouse", "Implemented"],
        ["Optimization", "Delta, Spark, Warehouse, Eventhouse", "Implemented"],
        ["Troubleshooting", "Intentional failure and root-cause exercises", "Implemented"],
    ], columns=["Exam theme", "CityRide evidence", "Status"])
    st.dataframe(coverage, use_container_width=True, hide_index=True)
    st.markdown("""
### Interview talking points

1. Why Lakehouse vs Warehouse vs Eventhouse?
2. How does the incremental load prevent duplicate or missed records?
3. How are late streaming events handled?
4. Why use a OneLake shortcut instead of copying data?
5. How is access separated between analysts and engineers?
6. Which bottleneck did you measure before optimizing?
7. How do Git and deployment pipelines support safe promotion?
""")

elif page == "About the Project":
    st.title("About the Project")
    st.markdown("""
**CityRide 360** is a fictional portfolio project designed to demonstrate practical Microsoft Fabric data engineering skills in one coherent system.

It combines batch and streaming ingestion, Lakehouse and Warehouse patterns, PySpark, SQL, KQL, Data Factory orchestration, Real-Time Intelligence, governance, security, CI/CD, monitoring, troubleshooting, and performance tuning.

The public Streamlit app uses synthetic/demo data so it remains safe and accessible even when the private Fabric environment is unavailable.
""")
    guide = Path(__file__).parent / "docs" / "CityRide_DP700_Capstone_Project_Guide.pdf"
    if guide.exists():
        with open(guide, "rb") as f:
            st.download_button("Download the project guide (PDF)", f, file_name=guide.name, mime="application/pdf")
    if VIDEO_URL:
        st.video(VIDEO_URL)
    else:
        st.info("Optional: set CITYRIDE_VIDEO_URL to surface your 3–5 minute walkthrough.")
    st.subheader("Suggested CV entry")
    st.markdown("""
**CityRide 360 — Microsoft Fabric Data Engineering Platform**  
Designed and deployed an end-to-end batch and streaming analytics platform using Fabric Lakehouse, Delta Lake, PySpark, Data Factory, Warehouse/T-SQL, Eventstream, Eventhouse/KQL, Power BI, Git, security controls, monitoring, and performance optimization.
""")

st.divider()
st.caption("CityRide 360 • Public portfolio demo • Synthetic data only")
