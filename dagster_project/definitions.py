from dagster import Definitions

from .assets import (
    extract_imdb_movies,
    extract_imdb_series,
    save_imdb_movies,
    save_imdb_series,
    transform_imdb_movies,
    transform_imdb_series,
    top_movies_by_rating,
    movies_by_year,
    movies_vs_series,
    load_movies_to_postgres,
    load_series_to_postgres,
)

defs = Definitions(
    assets=[
        extract_imdb_movies,
        save_imdb_movies,
        transform_imdb_movies,
        top_movies_by_rating,
        movies_by_year,
        load_movies_to_postgres,
    ]
)