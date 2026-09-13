# CityRide 360 — Microsoft Fabric DP-700 Portfolio

A deployment-ready Streamlit portfolio for presenting an end-to-end Microsoft Fabric data engineering project.

## Included

- Project overview and business story
- Architecture page
- Batch Pipeline / Lakehouse walkthrough
- PySpark examples
- Eventstream / Eventhouse / KQL walkthrough
- Spark Structured Streaming example
- Warehouse / T-SQL examples
- Security and CI/CD
- Monitoring and optimization
- DP-700 coverage matrix
- Interactive synthetic demo metrics
- The full CityRide project PDF

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a public GitHub repository, for example `cityride-fabric-dp700`.
2. Upload the contents of this folder to the repository root.
3. Sign in to Streamlit Community Cloud.
4. Create an app from the GitHub repository.
5. Select `app.py` as the entry point.
6. Deploy.

## Optional public links

The app reads these environment variables:

```text
CITYRIDE_GITHUB_URL
CITYRIDE_POWERBI_URL
CITYRIDE_VIDEO_URL
CITYRIDE_CONTACT_URL
```

Use them for GitHub, a safe Power BI report, a short demo video, and your professional contact/profile page.

## Recommended full repository structure

```text
cityride-fabric-dp700/
├── README.md
├── app.py
├── requirements.txt
├── assets/
│   ├── architecture.png
│   └── screenshots/
├── notebooks/
│   ├── 01_bronze_ingestion.ipynb
│   ├── 02_silver_transform.ipynb
│   ├── 03_gold_metrics.ipynb
│   └── 04_structured_streaming.ipynb
├── sql/
│   ├── create_dimensions.sql
│   ├── create_fact_trip.sql
│   ├── load_warehouse.sql
│   ├── security.sql
│   └── optimization.sql
├── kql/
│   ├── realtime_metrics.kql
│   └── monitoring_queries.kql
├── pipelines/
├── docs/
│   ├── CityRide_DP700_Capstone_Project_Guide.pdf
│   └── dp700-mapping.md
└── .streamlit/
    └── config.toml
```

## Security

Keep the Fabric backend private. Do not commit credentials, access tokens, connection strings, private tenant information, or real PII. The public demo should use synthetic/public data and safe screenshots or report links.
