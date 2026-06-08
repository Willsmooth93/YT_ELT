from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json

#define the local timezone
local_tz = pendulum.timezone("America/New_York")


#Default arguments for the DAG
default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": ["data@engineers.com"],
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2025, 1, 1, tzinfo=local_tz),
    #"end_date": datetime(2024, 12, 31, tzinfo=local_tz),
}

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='Produce JSON file with raw data from YouTube API',
    schedule='0 14 * * *',
    catchup=False
) as dag:

    #Define the tasks in the DAG
    playlistid = get_playlist_id()
    video_ids = get_video_ids(playlistid)
    extracted_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extracted_data)

    #Define the task dependencies
    playlistid >> video_ids >> extracted_data >> save_to_json_task