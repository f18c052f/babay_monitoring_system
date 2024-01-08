from google.cloud import storage

KEY_PATH_STORAGE = "./sa_gcs-upload.json"


class StorageClient:
    @staticmethod
    def upload_file(
        bucket_name: str, source_file_name: str, destination_blob_name: str
    ):
        """Google Cloud Storageにファイルをアップロードする関数"""

        # サービスアカウントキーファイルを指定してクライアントを初期化
        storage_client = storage.Client.from_service_account_json(KEY_PATH_STORAGE)

        # バケットを指定
        bucket = storage_client.bucket(bucket_name)

        # バケット内のファイル（blob）を指定
        blob = bucket.blob(destination_blob_name)

        # ファイルをアップロード
        blob.upload_from_filename(source_file_name)

        print(f"Complete uploading {source_file_name} to {bucket_name}")
