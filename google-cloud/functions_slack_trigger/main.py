import os
from flask import jsonify
import functions_framework
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from slack_sdk.signature import SignatureVerifier

# Publisherクライアントを初期化
KEY_PATH = "./sa_slack-integration-service.json"
publisher = pubsub_v1.publisher.Client.from_service_account_file(KEY_PATH)
topic_path = publisher.topic_path(os.environ["GCP_PROJECT"], os.environ["PUBSUB_TOPIC"])


def verify_signature(request):
    request.get_data()
    verifier = SignatureVerifier(os.environ["SLACK_SECRET"])

    return verifier.is_valid_request(request.data, request.headers)


@functions_framework.http
def slack_command(request):
    if request.method != "POST":
        return "Only POST requests are accepted", 405

    # Slackの署名検証
    if not verify_signature(request):
        return "Invalid request", 403

    # Slashコマンドからのデータ取得
    data = request.form
    command_text = data.get("text", "run")

    # Pub/SubにPublish
    publisher.publish(topic_path, data=command_text.encode("utf-8"))
    return jsonify({"response_type": "in_channel", "text": "部屋の状態を確認するね"})
