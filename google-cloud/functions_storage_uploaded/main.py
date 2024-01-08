from datetime import datetime
from functions_framework import cloud_event
from slack import Slack
from storage_client import StorageClient

IMAGE_NAME = "ir_image.png"
JSON_NAME = "sht31.json"


def check_status(response_status: int) -> str:
    result = "Process Failed"

    if response_status == 200:
        result = "Process Successed"
    elif response_status == 404:
        result = "File Not Found in CloudStorage"

    return result


@cloud_event
def process_file_upload(event):
    """GCSにファイルがアップロードされたときに実行される関数"""
    storage_client = StorageClient(event)

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if storage_client.file_name == IMAGE_NAME:
        data = storage_client.get_image_data()

        # TODO: 寝返り検知処理

        response_status = Slack.send_image(
            data=data, initial_comment="部屋の様子だよー", title=current_datetime
        )
    elif storage_client.file_name == JSON_NAME:
        temp, hum = storage_client.get_message_data()
        message = f"温度： {temp}[℃] / 湿度： {hum}[%]"
        response_status = Slack.send_text(message=message)
    else:
        response_status = 404

    result_status = check_status(response_status=response_status)

    print(result_status)
