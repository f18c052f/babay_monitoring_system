import os
import base64
from google.cloud import pubsub_v1
from dotenv import load_dotenv
from sht31 import SHT31


def read_sensor_data() -> (float, float):
    # temperature, humidity = sht31.get_temperature_humidity()
    # return temperature, humidity

    # テストデータ
    return 25.5, 40.0


def encode_image(image_path: str) -> bytes:
    # 画像をBase64エンコードする
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def read_image_data() -> bytes:
    # TODO: IRカメラから画像取得

    # テストデータ
    return encode_image("./underReadry.jpeg")


def callback(message):
    print(f"Received message: {message}")
    message.ack()

    # センサーデータと画像データの取得
    temperature, humidity = read_sensor_data()
    image = read_image_data()

    # TODO: Cloud Storageへアップロード


def main():
    # .env ファイルから環境変数を読み込む
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    subscription_name = os.getenv("SUBSCRIPTION_NAME")

    # サブスクライバーとパブリッシャークライアントの初期化
    subscriber = pubsub_v1.SubscriberClient()
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
