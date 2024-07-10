from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .tasks import slack_message_task

@csrf_exempt
@require_POST
def slack_events(request):
    json_data = {}
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print(e)

    data_type = json_data.get("type", None)
    valid_data_types = ["url_verification", "event_callback"]
    if data_type not in valid_data_types:
        return HttpResponse("Not Allowed", status=403)

    if data_type == "url_verification":
        challenge = json_data.get("challenge", None)
        if challenge:
            return HttpResponse(challenge, status=200)
        return HttpResponse("Not Allowed", status=403)
    elif data_type == "event_callback":
        event = json_data.get("event", {})
        channel_id = event.get("channel", None)
        user_id = event.get("user", None)
        try:
            message = event.get("blocks", [])[
                0]['elements'][0]['elements'][1]['text']
        except:
            message = event.get("text", None)
        msg_ts = event.get("ts", None)
        thread_ts = event.get("thread_ts", msg_ts)
        if channel_id:
            # response = slacky.send_message(message=message, channel_id=channel_id, user_id=user_id, thread_ts=thread_ts)
            # response = slack_message_task.delay(
            #     message, channel_id, user_id, thread_ts)
          
            slack_message_task.apply_async(kwargs={
                "message": f"{message}",
                "channel_id": channel_id,
                "user_id": user_id,
                "thread_ts": thread_ts,
                "image_url": None}, countdown=0)
            return HttpResponse("Success", status=200)
        return HttpResponse("Not Allowed", status=403)

    return HttpResponse("OK")

