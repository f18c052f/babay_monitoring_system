# Deploy
gcloud functions deploy process_file_upload \
    --runtime python39 \
    --trigger-resource YOUR_BUCKET_NAME \
    --trigger-event google.storage.object.finalize \
    --set-env-vars SLACK_WEBHOOK_URL=your_slack_webhook_url
