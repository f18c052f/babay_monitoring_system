import pytest
from unittest.mock import Mock, patch
from main import slack_command


def test_slack_command_post_method():
    with pytest.raises(Exception) as e:
        slack_command(Mock(method="GET"))
    assert str(e.value) == "405 Method Not Allowed"


def test_slack_command_invalid_signature():
    with patch("your_module.verify_signature", return_value=False):
        response = slack_command(Mock(method="POST"))
    assert response[1] == 403


@patch("your_module.pubsub_v1.PublisherClient")
def test_slack_command_successful_publish(mock_pubsub):
    with patch("your_module.verify_signature", return_value=True):
        mock_request = Mock(method="POST", form={"text": "test message"})
        response = slack_command(mock_request)
        mock_pubsub.assert_called_once()
    assert json.loads(response[0].data.decode())["text"] == "部屋の状態を確認するね"
