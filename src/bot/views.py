from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json, helpers

SLACK_BOT_TOKEN = helpers.config("SLACK_BOT_TOKEN", default=None, cast=str)
@csrf_exempt
@require_POST
def slack_events(request):
    json_data = {}
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print(e)
    print(SLACK_BOT_TOKEN)
    data_type = json_data.get("type", None)
    if data_type != "url_verification":
        return HttpResponse("Not Allowed", status=403)
    challenge = json_data.get("challenge", None)
    if challenge:
        return HttpResponse(challenge, status=200)
    return HttpResponse("OK")
