# Deploy

### Create Pub/Sub Topic and Subscriber
```bash
$ gcloud pubsub topics create [TOPIC_NAME]
$ gcloud pubsub subscriptions create [SUBSCRIBER_NAME] --topic=[TOPIC_NAME]
```
[TOPIC_NAME],[SUBSCRIBER_NAME],[TOPIC_NAME]をご自身の環境に合わせて設定してください.

### Create Service Account
```bash
$ gcloud iam service-accounts create [SERVICE_ACCOUNT_NAME] 
$ gcloud projects add-iam-policy-binding [PROJECT_ID] --member="serviceAccount:[SERVICE_ACCOUNT_NAME]@[PROJECT_ID].iam.gserviceaccount.com" --role="[ROLE]"
$ gcloud iam service-accounts keys create [FILE_NAME].json --iam-account [SERVICE_ACCOUNT_NAME]@[PROJECT_ID].iam.gserviceaccount.com
```
[SERVICE_ACCOUNT_NAME],[PROJECT_ID],[FILE_NAME],[SERVICE_ACCOUNT_NAME]をご自身の環境に合わせて設定してください.<br><br>
作成したサービスアカウントキーファイルをfunction_slack_triggerディレクトリ配下に置いてください.<br>
main.pyのKEY_PATHを[FILE_NAME]（＝サービスアカウントキーファイル）に設定してください.


### Set Slack Slash Command
[ドキュメント](https://cloud.google.com/functions/docs/tutorials/slack?hl=ja#functions-clone-sample-repository-python)参照

### Deploy Function
```bash
$ cd function_slack_trigger
$ gcloud functions deploy python-slack-function \
--gen2 \
--runtime=python39 \
--region=asia-northeast1 \
--source=. \
--entry-point=slack_command \
--trigger-http \
--set-env-vars "GCP_PROJECT=[YOUR_PROJECT_ID],SLACK_SECRET=[YOUR_SLACK_SECRET],PUBSUB_TOPIC=[YOUR_TOPIC]" \
--allow-unauthenticated
```
[YOUR_PROJECT_ID],[YOUR_SLACK_SECRET],[YOUR_TOPIC]をご自身の環境に合わせて設定してください.