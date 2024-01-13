import os
import json
from google.cloud import pubsub_v1
from dotenv import load_dotenv
from sht31 import SHT31
from storage_client import StorageClient
from picamera import Camera

KEY_PATH_PUBSUB = "sa_slack-integration-service.json"
IMAGE_NAME = "ir_image.png"
JSON_NAME = "sht31.json"


def create_json_file(temp: float, hum: float, filename: str):
    data = {"temperature": temp, "humidity": hum}

    # JSONファイルに書き込む
    with open(filename, "w") as file:
        json.dump(data, file)


def create_sensor_data_file():
    temperature, humidity = SHT31.get_temperature_humidity()

    temperature = round(temperature, 1)
    humidity = round(humidity, 1)

    create_json_file(temp=temperature, hum=humidity, filename=JSON_NAME)


def create_image_data_file():
    camera = Camera()
    camera.capture_image(IMAGE_NAME)
    camera.close_camera()


def callback(message):
    print(f"Received message: {message}")
    message.ack()

    # データ作成
    create_sensor_data_file()
    create_image_data_file()

    # Cloud Storageへアップロード
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    StorageClient.upload_file(bucket_name, JSON_NAME, JSON_NAME)
    StorageClient.upload_file(bucket_name, IMAGE_NAME, IMAGE_NAME)


def main():
    # .env ファイルから環境変数を読み込む
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    subscription_name = os.getenv("SUBSCRIPTION_NAME")

    # サブスクライバーとパブリッシャークライアントの初期化
    subscriber = pubsub_v1.subscriber.Client.from_service_account_file(KEY_PATH_PUBSUB)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # サブスクリプションのリッスン開始
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    # スクリプトが終了しないように待機
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()


if __name__ == "__main__":
    main()
