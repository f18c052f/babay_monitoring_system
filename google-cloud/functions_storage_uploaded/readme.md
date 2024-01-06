# Deploy

### Create Cloud Storage Bucket
米国リージョンは無料枠があるためus-east1に作成

### Add roles to Cloud Storage Service Agent
CloudEvent trigger作成時にCloud StorageのサービスエージェントにPub/Subのパブリッシュ権限を付与してある必要があります.<br>
[YOUR_PROJECT_ID]を自身の環境に合わせて設定してください.
```bash
$ PROJECT_ID=[YOUR_PROJECT_ID]
$ SERVICE_ACCOUNT="$(gcloud storage service-agent --project=${PROJECT_ID})"   
$ gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role='roles/pubsub.publisher'
```

### Deploy Cloud Functions
--regionは使用するCloud Storageバケットのリージョンに合わせてあります<br>
[YOUR_BUCKET_NAME],[YOUR_BOT_USER_OAUTH_TOKEN],[YOUR_SLACK_CHANNEL_ID]を自身の環境に合わせて設定してください

```bash
$ cd functions_storage_uploaded
$ gcloud functions deploy python-storage-function \
--gen2 \
--runtime=python39 \
--region=us-east1 \
--source=. \
--entry-point=process_file_upload \
--trigger-resource="[YOUR_BUCKET_NAME]" \
--trigger-event=google.storage.object.finalize \
--set-env-vars="SLACK_TOKEN=[YOUR_BOT_USER_OAUTH_TOKEN],SLACK_CHANNEL_ID=[YOUR_SLACK_CHANNEL_ID]"
```
<br>

※下記のようなエラーが発生する場合は必要なAPIが有効かされていない可能性がある.<br>

```bash
Invalid resource state for "": Permission denied while using the Eventarc Service Agent. If you recently started to use Eventarc, it may take a few minutes before all necessary permissions are propagated to the Service Agent. Otherwise, verify that it has Eventarc Service Agent role.
```

該当のAPIをgcloud services enableコマンドで有効化するか、少し時間をおいてから再度デプロイコマンドを実行する.

