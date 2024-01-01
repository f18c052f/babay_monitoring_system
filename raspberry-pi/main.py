import base64
import json
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import os

# .env ファイルから環境変数を読み込む
load_dotenv()
project_id = os.getenv("PROJECT_ID")
subscription_name = os.getenv("SUBSCRIPTION_NAME")
publish_topic_name = os.getenv("PUBLISH_TOPIC_NAME")

# サブスクライバーとパブリッシャークライアントの初期化
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)
publish_topic_path = publisher.topic_path(project_id, publish_topic_name)


def read_sensor_data():
    # センサーから温度と湿度を取得する処理
    # この部分はセンサーに応じて実装してください
    # 例:
    # temperature = get_temperature()
    # humidity = get_humidity()
    # return temperature, humidity

    # テストデータ
    return 25.5, 40.0


def encode_image(image_path):
    # 画像をBase64エンコードする
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def publish_message(temperature, humidity, encoded_image):
    # JSON形式でメッセージを作成
    message = {
        "temperature": temperature,
        "humidity": humidity,
        "image_data": encoded_image,
    }
    message_json = json.dumps(message)

    # メッセージを別のトピックにPublish
    publisher.publish(publish_topic_path, data=message_json.encode("utf-8"))


def callback(message):
    print(f"Received message: {message}")
    message.ack()

    # センサーデータと画像データの取得
    temperature, humidity = read_sensor_data()
    encoded_image = encode_image("path/to/your/image.jpg")

    # 別のトピックにメッセージをPublish
    publish_message(temperature, humidity, encoded_image)


# サブスクリプションのリッスン開始
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

# スクリプトが終了しないように待機
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
