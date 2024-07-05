from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json, helpers, requests

SLACK_BOT_TOKEN = helpers.config("SLACK_BOT_TOKEN", default=None, cast=str)


def send_message(message, channel_id=None):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        "Content-Type": 'application/json',
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Accept": "application/json"
    }
    data = {
        "channel": f"{channel_id}",
        "text": message
    }
    return requests.post(url=url, headers=headers, json=data)

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
        message = event.get("text", None)
        if channel_id:
            response = send_message(message=message, channel_id=channel_id)
            return HttpResponse(response.text, status=response.status_code)
        return HttpResponse("Not Allowed", status=403)
    
    return HttpResponse("OK")
