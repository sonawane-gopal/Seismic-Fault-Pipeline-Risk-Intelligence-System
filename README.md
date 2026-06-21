<<<<<<< HEAD
# SFPRIS — Seismic-Fault Pipeline Risk Intelligence System

## Overview
An end-to-end geospatial machine learning project that predicts pipeline risk 
across the United States by combining seismic fault proximity, earthquake history, 
and pipeline incident data.

## Tech Stack
- PostgreSQL + PostGIS — spatial database
- Python — data loading, ML training
- ArcGIS Pro — spatial analysis
- ArcGIS Online — hosted feature layers
- Streamlit — interactive dashboard
- Docker — containerization

## Data Sources
- PHMSA Hazardous Liquid Incidents
- PHMSA Gas Transmission & Gathering Incidents
- USGS Quaternary Fault and Fold Database
- HIFLD Natural Gas Pipelines (REST API)
- HIFLD Hazardous Liquid Pipelines (REST API)
- USGS Earthquake Catalog (REST API)

## Project Structure
sfpris/

├── data/

│   ├── raw/          # original downloaded files

│   └── processed/    # cleaned outputs

├── notebooks/        # EDA notebooks

├── src/              # Python scripts

├── models/           # saved ML models

├── outputs/          # maps, charts, exports

├── requirements.txt

├── .gitignore

├── README.md

└── .env

## Phases
- Phase 1 — ELT (PostGIS data loading)
- Phase 2 — Spatial Analysis (ArcGIS Pro)
- Phase 3 — ML Training (Isolation Forest + XGBoost + SHAP)
- Phase 4 — Publish to ArcGIS Online
- Phase 5 — Streamlit + Docker Deployment

## Author
Gopal Sonawane — Geospatial Analyst
=======
# Seismic-Fault-Pipeline-Risk-Intelligence-System
End-to-end geospatial ML project predicting US pipeline incident risk using seismic fault proximity, earthquake history, and PHMSA incident data. Built with PostGIS, Python, ArcGIS Pro, XGBoost, and Streamlit.
>>>>>>> 5be5d704cf42595ecf6b60e989a83e668381bcc2
