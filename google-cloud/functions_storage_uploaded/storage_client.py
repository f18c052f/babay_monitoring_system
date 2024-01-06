import json
from google.cloud import storage


class StorageClient:
    def __init__(self, event):
        self.file_name = event["name"]
        bucket_name = event["bucket"]

        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self.blob = self.bucket.blob(self.file_name)

    def get_image_data(self) -> bytes:
        return self.blob.download_as_bytes()

    def get_message_data(self) -> (float, float):
        """@return (temperature, humidity)"""
        json_data = json.loads(self.blob.download_as_text())
        temp = json_data.get("temperature")
        hum = json_data.get("humidity")

        return (temp, hum)
