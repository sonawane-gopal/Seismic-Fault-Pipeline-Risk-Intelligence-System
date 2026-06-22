<<<<<<< HEAD
# SFPRIS — Seismic-Fault Pipeline Risk Intelligence System

## Live Demo
https://seismic-fault-pipeline-risk-intelligence-system-tddfwmfy7bmtk6.streamlit.app/

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

## Data Sources
- PHMSA Hazardous Liquid Incidents
- PHMSA Gas Transmission & Gathering Incidents
- USGS Quaternary Fault and Fold Database
- HIFLD Natural Gas Pipelines (REST API)
- HIFLD Hazardous Liquid Pipelines (REST API)
- USGS Earthquake Catalog (REST API)

## Project Structure

```
Seismic-Fault-Pipeline-Risk-Intelligence-System/
│
├── notebooks/
│   ├── 01_explore_phmsa.ipynb        # Load PHMSA HL and Gas incidents to PostGIS
│   ├── 02_load_faults.ipynb          # Load USGS Quaternary fault lines to PostGIS
│   ├── 03_load_hifld.ipynb           # Load EIA pipeline network to PostGIS
│   ├── 04_load_earthquakes.ipynb     # Fetch USGS earthquake API and load to PostGIS
│   ├── 05_export_shapefiles.ipynb    # Export PostGIS tables to shapefiles for QGIS
│   └── 06_ml_training.ipynb         # Feature engineering, XGBoost training, SHAP
│
├── data/
│   ├── raw/                          # Original downloaded shapefiles and Excel files
│   └── processed/                    # QGIS spatial outputs and ML datasets
│
├── models/
│   └── xgboost_pipeline_risk.pkl    # Trained XGBoost classifier (local)
│
├── app.py                            # Full Streamlit dashboard (local version)
├── app_demo.py                       # Demo Streamlit dashboard (deployed version)
├── sample_data.csv                   # 500 sample incidents for Streamlit Cloud
├── model_demo.pkl                    # Demo XGBoost model for deployment
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Excludes data, models, venv, .env
├── README.md                         # Project documentation
└── .env                              # Database credentials (not pushed to GitHub)

## Phases
- Phase 1 — ELT (PostGIS data loading)
- Phase 2 — Spatial Analysis (ArcGIS Pro)
- Phase 3 — ML Training (Isolation Forest + XGBoost + SHAP)
- Phase 4 — Publish to ArcGIS Online

## Author
Gopal Sonawane — Geospatial Analyst

# Seismic-Fault-Pipeline-Risk-Intelligence-System
End-to-end geospatial ML project predicting US pipeline incident risk using seismic fault proximity, earthquake history, and PHMSA incident data. Built with PostGIS, Python, ArcGIS Pro, XGBoost, and Streamlit.
>>>>>>> 5be5d704cf42595ecf6b60e989a83e668381bcc2
