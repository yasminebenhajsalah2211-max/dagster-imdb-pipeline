from dagster import ScheduleDefinition
from .jobs import imdb_job


imdb_schedule = ScheduleDefinition(
    job=imdb_job,
    cron_schedule="0 9 * * *"
)