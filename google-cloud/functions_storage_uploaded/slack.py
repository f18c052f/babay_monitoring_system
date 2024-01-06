import os
import requests


class slack:
    _SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    _SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
    _headers = {"Authorization": f"Bearer {_SLACK_TOKEN}"}

    @classmethod
    def send_text(cls, message: str) -> int:
        data = {"channel": cls._SLACK_CHANNEL_ID, "text": message}

        response = requests.post(
            url="https://slack.com/api/chat.postMessage",
            headers=cls._headers,
            data=data,
        )

        return response.status_code

    @classmethod
    def send_image(
        cls, data: bytes, initial_comment: str, title: str, file_name: str = "image"
    ) -> int:
        files = {"file", data}
        param = {
            "channels": cls._SLACK_CHANNEL_ID,
            "filename": file_name,
            "initial_comment": initial_comment,
            "title": title,
        }

        response = requests.post(
            url="https://slack.com/api/files.upload",
            headers=cls._headers,
            files=files,
            params=param,
        )

        return response.status_code
