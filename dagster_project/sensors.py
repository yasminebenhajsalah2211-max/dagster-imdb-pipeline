from dagster import sensor, RunRequest
from .jobs import imdb_job


@sensor(job=imdb_job)
def imdb_sensor():
    return RunRequest(run_key=None)