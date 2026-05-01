# 🎬 Dagster IMDb Data Pipeline

## 📌 Description

This project implements an end-to-end data pipeline using **Dagster** as an orchestrator.  
The pipeline follows an **ETL (Extract, Transform, Load)** process to collect, process, store, and visualize movie data from an external API.

---

## 🚀 Features

- 🔄 Data extraction from IMDb API (via RapidAPI)
- 🧹 Data transformation (cleaning, formatting)
- 🗄️ Data storage in PostgreSQL
- 📊 Interactive dashboard using Streamlit + Plotly
- ⚙️ Orchestration with Dagster (Assets, Jobs, Schedules, Sensors)
- 🧪 Unit testing with pytest
- 🐳 Containerization with Docker

---

## 🏗️ Project Architecture

```text
dagster_imdb_project/
│
├── dagster_project/        # Dagster pipeline (assets, jobs, schedules, sensors)
├── dashboard/              # Streamlit dashboard
├── data/                   # Generated files (charts)
├── tests/                  # Unit tests (pytest)
├── docker-compose.yml      # Docker services (Dagster + PostgreSQL)
├── Dockerfile
├── requirements.txt
└── README.md
⚙️ Technologies Used
Python 🐍
Dagster
PostgreSQL
Docker
Streamlit
Plotly
Pandas
pytest
🔄 Pipeline Steps
1. Extract

Fetch movie data from IMDb API (RapidAPI)

2. Transform
Convert data types (rating → float, year → int)
Clean dataset
3. Load

Store processed data into PostgreSQL database

4. Visualize

Display insights using Streamlit dashboard:

Top 10 movies by rating
Movies distribution by year
Rating distribution
Genre analysis
🐳 Run the Project (Docker)
docker compose up --build
🌐 Access Interfaces
📊 Dagster UI
http://localhost:3000
📈 Streamlit Dashboard
streamlit run dashboard/app.py
🗄️ PostgreSQL

Database connection:

Host: localhost
Port: 5433
Database: imdb_db
User: imdb_user
Password: imdb_password

## 📊 Interactive Dashboard

The dashboard allows users to explore movie data with filters and dynamic visualizations.

### 🔍 Features
- Filter by year range
- Filter by minimum rating
- View top movies dataset
- Interactive charts (Plotly)

### 📸 Preview

![Dashboard](dashboard/dashboard.png)

🧪 Run Tests
pytest
📊 Dashboard Features
🎛️ Interactive filters (year, rating)
📈 Dynamic charts (Plotly)
📊 KPI metrics
📋 Data table visualization
⚡ Improvements

Possible future improvements:

Add Machine Learning model (prediction/recommendation)
Add real-time streaming data
Deploy dashboard online
Advanced analytics
👩‍💻 Author

Yasmine Ben Haj Salah
