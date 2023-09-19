from celery import shared_task
from src.youtube import YoutubeRecording


@shared_task()
def upload_to_youtube_from_dir(google_client_id, google_client_secret, google_refresh_token, video_path, title):
    youtube_recording = YoutubeRecording(
        client_id=google_client_id,
        client_secret=google_client_secret,
        refresh_token=google_refresh_token
    )
    print(video_path)
    print(title)

    youtube_url = youtube_recording.upload_from_dir(video_path, title)
    return youtube_url

