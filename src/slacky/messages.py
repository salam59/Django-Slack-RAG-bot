import os
import helpers
import requests
import json

from app.settings import BASE_DIR

SLACK_BOT_TOKEN = helpers.config("SLACK_BOT_TOKEN", default=None, cast=str)


def get_file_info(file_path):
    file_name = os.path.join(BASE_DIR, 'data', 'images', file_path)
    file_size = os.path.getsize(file_name)
    return file_path, file_size


def send_message(message, channel_id=None, user_id=None, thread_ts=None, image_path=None):
    url = ' https://slack.com/api/files.getUploadURLExternal'
    headers = {
        "Content-Type": 'application/x-www-form-urlencoded',
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Accept": "application/json"
    }
    image_name, image_size = get_file_info(image_path)
    data = {
        "filename": image_name,
        "length": image_size
    }
    response = requests.post(url=url, headers=headers, data=data)
    if response.status_code == 200:
        data = response.json()
        upload_url = data['upload_url']
        file_id = data['file_id']
    else:
        return response.json()

    file_uplod_response = requests.post(url=upload_url, files={'file': open(
        os.path.join(BASE_DIR, 'data', 'images', image_path), 'rb')})
    if file_uplod_response.status_code == 200:
        final_upload_url = 'https://slack.com/api/files.completeUploadExternal'
        headers = {
            "Content-Type": 'application/json; charset=utf-8',
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Accept": "application/json"
        }
        data = {
            "files": [{"id": file_id}],
            "channel_id": f"{channel_id}",
            "thread_ts": f"{thread_ts}"
        }
        if user_id:
            message = f"<@{user_id}> {message}".strip()
            data['initial_comment'] = message
        final_upload_response = requests.post(
            url=final_upload_url, headers=headers, json=data)
        return final_upload_response.json()
    else:
        return file_uplod_response.json()
    


#     return response.json()
# def send_message(message, channel_id=None, user_id=None, thread_ts=None, image_url=None):
#     url = 'https://slack.com/api/files.upload'
#     # 'https://slack.com/api/chat.postMessage'
#     upload_image(image_url,channel_id=channel_id,user_id=user_id,thread_ts=thread_ts,message=message)
#     headers = {
#         "Content-Type": 'application/json; charset=utf-8',
#         "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
#         "Accept": "application/json"
#     }
#     if user_id:
#         message = f"<@{user_id}> {message}".strip()
#     data = {
#         "channel": f"{channel_id}",
#         "text": message
#     }
#     if thread_ts is not None:
#         data["thread_ts"] = thread_ts
#     return requests.post(url=url, headers=headers, json=data)
