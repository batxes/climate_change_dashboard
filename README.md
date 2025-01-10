# Ocean Temperature Dashboard

A Streamlit dashboard showing historical ocean temperature data.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.streamlit/secrets.toml`
4. Run: `streamlit run streamlit_app.py`

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