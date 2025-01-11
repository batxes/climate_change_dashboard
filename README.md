# Ocean Temperature Dashboard

A Streamlit dashboard showing historical ocean temperature data.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.streamlit/secrets.toml`
4. Run: `streamlit run streamlit_app.py`

## Design schema

![Design schema](images/Climate_Dashboard.png)

## Deployment

This app is deployed using:
- Streamlit Cloud for the web application
- Railway for PostgreSQL database

## Environment Variables

Required secrets in Streamlit Cloud:
``` toml
    [postgres_prod]
    DATABASE_URL = "postgresql://user:password@host:port/database"
```

## To add
https://www.ncei.noaa.gov/cdo-web/datasets
    Global Temperature: https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt
    Compare with: https://royalsociety.org/news-resources/projects/climate-change-evidence-causes/basics-of-climate-change/
