import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from dagster import asset

from sqlalchemy import create_engine


load_dotenv()

DATA_DIR = "data"

def get_postgres_engine():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

def clean_movies(df):
    df["rating"] = df["rating"].astype(float)
    df["year"] = df["year"].astype(int)
    return df

def fetch_imdb(endpoint: str):
    api_key = os.getenv("RAPIDAPI_KEY")
    host = os.getenv("RAPIDAPI_HOST")

    url = f"https://{host}{endpoint}"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": host,
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code in [403, 429]:
        print("API blocked, using local CSV fallback")

        if endpoint == "/":
            return pd.read_csv("data/imdb_movies.csv").to_dict(orient="records")

        if endpoint == "/series/":
            return pd.read_csv("data/imdb_series.csv").to_dict(orient="records")

    response.raise_for_status()
    return response.json()

@asset
def load_movies_to_postgres(transform_imdb_movies):
    engine = get_postgres_engine()
    transform_imdb_movies.to_sql(
        "imdb_movies",
        engine,
        if_exists="replace",
        index=False
    )
    return "Table imdb_movies loaded into PostgreSQL"

@asset
def transform_imdb_movies(extract_imdb_movies):
    return clean_movies(extract_imdb_movies)

@asset
def load_series_to_postgres(transform_imdb_series):
    engine = get_postgres_engine()
    transform_imdb_series.to_sql(
        "imdb_series",
        engine,
        if_exists="replace",
        index=False
    )
    return "Table imdb_series loaded into PostgreSQL"

@asset
def extract_imdb_movies():
    data = fetch_imdb("/")
    df = pd.DataFrame(data)
    return df


@asset
def extract_imdb_series():
    data = fetch_imdb("/series/")
    df = pd.DataFrame(data)
    return df


@asset
def save_imdb_movies(extract_imdb_movies):
    path = f"{DATA_DIR}/imdb_movies.csv"
    extract_imdb_movies.to_csv(path, index=False)
    return path


@asset
def save_imdb_series(extract_imdb_series):
    path = f"{DATA_DIR}/imdb_series.csv"
    extract_imdb_series.to_csv(path, index=False)
    return path


@asset
def transform_imdb_movies(extract_imdb_movies):
    df = extract_imdb_movies.copy()

    columns_to_keep = [
        "rank",
        "title",
        "description",
        "rating",
        "year",
        "genre",
        "thumbnail",
        "imdbid",
    ]

    existing_columns = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_columns]

    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    return df


@asset
def transform_imdb_series(extract_imdb_series):
    df = extract_imdb_series.copy()

    columns_to_keep = [
        "rank",
        "title",
        "description",
        "rating",
        "year",
        "genre",
        "thumbnail",
        "imdbid",
    ]

    existing_columns = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_columns]

    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    return df


@asset
def top_movies_by_rating(transform_imdb_movies):
    df = transform_imdb_movies.sort_values("rating", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(df["title"], df["rating"])
    plt.xlabel("Rating IMDb")
    plt.ylabel("Movie")
    plt.title("Top 10 Movies by IMDb Rating")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    path = f"{DATA_DIR}/top_movies_by_rating.png"
    plt.savefig(path)
    plt.close()

    return path


@asset
def movies_by_year(transform_imdb_movies):
    df = transform_imdb_movies.dropna(subset=["year"])
    counts = df["year"].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    counts.plot(kind="bar")
    plt.xlabel("Year")
    plt.ylabel("Number of movies")
    plt.title("Movies by Year")
    plt.tight_layout()

    path = f"{DATA_DIR}/movies_by_year.png"
    plt.savefig(path)
    plt.close()

    return path


@asset
def movies_vs_series(transform_imdb_movies, transform_imdb_series):
    counts = {
        "Movies": len(transform_imdb_movies),
        "Series": len(transform_imdb_series),
    }

    plt.figure(figsize=(6, 5))
    plt.bar(counts.keys(), counts.values())
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.title("Movies vs Series")
    plt.tight_layout()

    path = f"{DATA_DIR}/movies_vs_series.png"
    plt.savefig(path)
    plt.close()

    return path