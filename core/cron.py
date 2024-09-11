import logging
from django.conf import settings

from .models import UserCredential
from src.zoom import ZoomJWTClient, ZoomRecording
from celery import shared_task


logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)
logger.info("Cron Job Output message")


@shared_task()
def run_user_zoom_downloader(official_data):
    logger = logging.getLogger('core.cron')


    logger.info('Start...')

    # extracting the data from the official_data
    user = official_data['user']
    zoom_client_id = official_data['zoom_client_id']
    zoom_client_secret = official_data['zoom_client_secret']
    zoom_account_id = official_data['zoom_account_id']
    zoom_email = official_data['zoom_email']
    min_duration = official_data['min_duration']
    from_day_delta = official_data['from_day_delta']
    page_size = official_data['page_size']

    logger.info(f"Retrieving custom user for: {user}")
    
    # Get the custom user or raise an error if it doesn't exist
    custom_user = UserCredential.objects.get(user=user)
    logger.info(f"Retrieved custom_user: {custom_user}")

    # generating the zoom_client
    logger.info("Generating Zoom client...")
    zoom_client = ZoomJWTClient(
        zoom_client_id,
        zoom_client_secret,
        zoom_account_id,
        86400
    )
    logger.info("Zoom client generated successfully.")
    
    for email in zoom_email.split(','):
        logger.info(f"Using email : {email}")

        zoom = ZoomRecording(
            zoom_client,
            email,
            duration_min=min_duration,
            filter_meeting_by_name=settings.FILTER_MEETING_BY_NAME,
            only_meeting_names=settings.ONLY_MEETING_NAMES,
            from_day_delta=from_day_delta,
            page_size=page_size
        )

        zoom.download_meetings(
            custom_user,
            settings.MEDIA_ROOT,
            settings.DOWNLOADED_FILES
        )
        logger.info(f"Meetings downloaded for email: {email}")
    
    logger.info('End.')
    print('End')
    
    


