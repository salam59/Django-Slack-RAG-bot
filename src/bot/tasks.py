from celery import shared_task
import slacky

from .utils import query_rag

@shared_task
def slack_message_task(message, channel_id=None, user_id=None, thread_ts=None):
    response = query_rag(message)
    r = slacky.send_message(response, channel_id, user_id, thread_ts)
    return r.status_code