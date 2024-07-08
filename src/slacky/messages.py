import helpers, requests

SLACK_BOT_TOKEN = helpers.config("SLACK_BOT_TOKEN", default=None, cast=str)


def send_message(message, channel_id=None, user_id=None, thread_ts=None):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        "Content-Type": 'application/json; charset=utf-8',
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Accept": "application/json"
    }
    if user_id:
        message = f"<@{user_id}> {message}".strip()
    data = {
        "channel": f"{channel_id}",
        "text": message
    }
    if thread_ts is not None:
        data["thread_ts"] = thread_ts
    return requests.post(url=url, headers=headers, json=data)