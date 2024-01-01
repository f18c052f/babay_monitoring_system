import base64
import json
import requests
import os
from google.cloud import pubsub_v1

# 環境変数から設定を読み込む
slack_token = os.getenv("SLACK_TOKEN")
webhook_url = os.getenv("SLACK_WEBHOOK_URL")
project_id = os.getenv("GCP_PROJECT_ID")
subscription_name = os.getenv("GCP_SUBSCRIPTION_NAME")


# Slackに温度と湿度のデータ、および画像を送信する関数
def send_to_slack(temperature, humidity, image_file_path):
    # テキストメッセージの送信
    message = {"text": f"温度: {temperature} °C, 湿度: {humidity} %"}
    response = requests.post(webhook_url, json=message)
    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )

    # 画像のアップロード
    with open(image_file_path, "rb") as image_file:
        files = {"file": image_file}
        payload = {
            "token": slack_token,
            "channels": "#channel_name",  # ここに画像を投稿するSlackチャンネルを指定
            "filename": image_file_path,
            "title": "Received Image",
        }
        response = requests.post(
            url="https://slack.com/api/files.upload", params=payload, files=files
        )
        if response.status_code != 200:
            raise ValueError(
                f"Image upload to Slack returned an error {response.status_code}, the response is:\n{response.text}"
            )


def callback(message):
    print(f"Received message: {message}")
    message.ack()

    # メッセージの解析
    data = json.loads(message.data.decode("utf-8"))
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    image_data = base64.b64decode(data["image_data"])

    # 画像データを一時ファイルに保存
    image_file_path = "temp_received_image.jpg"
    with open(image_file_path, "wb") as image_file:
        image_file.write(image_data)

    # 温度と湿度のデータをSlackに通知
    send_to_slack(temperature, humidity, image_file_path)


# サブスクライバークライアントの初期化
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

# サブスクリプションのリッスン開始
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
streaming_pull_future.result()
