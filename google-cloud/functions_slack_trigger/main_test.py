import pytest
from unittest.mock import Mock, patch
from main import slack_command


def test_slack_command_post_method():
    response = slack_command(Mock(method="GET"))
    assert response[0] == "Only POST requests are accepted"
    assert response[1] == 405


def test_slack_command_invalid_signature():
    with patch("main.verify_signature", return_value=False):
        response = slack_command(Mock(method="POST"))
    assert response[0] == "Invalid request"
    assert response[1] == 403


# TODO: fix test code
# @patch("main.pubsub_v1.PublisherClient")
# def test_slack_command_successful_publish(mock_pubsub):
#     with patch("main.verify_signature", return_value=True):
#         mock_request = Mock(method="POST", form={"text": "run"})
#         response = slack_command(mock_request)
#         mock_pubsub.assert_called_once()
#     assert json.loads(response[0].data.decode())["text"] == "部屋の状態を確認するね"
