import json
import sys
from typing import Optional, Dict

import requests


class SlackBotApi:
    def __init__(self, webhook: str) -> None:
        self._webhook = webhook

    @staticmethod
    def msg_color(msg_type: str) -> str:
        color = {
            "MAJOR":   "#FF0000",
            "ERROR":   "#FF0000",
            "MINOR":   "#D1C432",
            "INFO":    "#32D132",
            "DEFAULT": "#FFFFFF"
        }
        return color[msg_type]

    def send_message(self, message: str) -> Dict:
        try:
            msg_type = message.split()[0].strip(":*")
        except IndexError:
            msg_type = "DEFAULT"
        data = {
            "username": "Chain status",
            "icon_emoji": ":cudos:",
            "attachments": [
                {
                    "color": self.msg_color(msg_type),
                    "fields": [
                        {
                            "value": message,
                            "short": "false",
                        }
                    ]
                }
            ]
        }
        byte_length = str(sys.getsizeof(data))
        headers = {'Content-Type': "application/json",
                   'Content-Length': byte_length}
        return requests.post(self._webhook, data=json.dumps(data), headers=headers)

    def test_connection(self) -> bool:
        data = {
            "username": "Connection ping from Cosmos Panic",
            "icon_emoji": ":information_source:",
            "attachments": [
                {
                    "fields": [
                        {
                        }
                    ]
                }
            ]
        }
        byte_length = str(sys.getsizeof(data))
        headers = {'Content-Type': "application/json",
                   'Content-Length': byte_length}
        response = requests.post(
            self._webhook, data=json.dumps(data), headers=headers)
        return response.status_code == 200
