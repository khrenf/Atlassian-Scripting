import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv
import os

load_dotenv()
jira_key = os.getenv('JIRA_KEY')


def add_comment(issue, message):
    url = f"https://kobyrenfert29.atlassian.net/rest/api/2/issue/{issue}"
    auth = HTTPBasicAuth("kobyrenfert29@gmail.com", jira_key)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "update": {
            "comment": [
                {
                    "add": {
                        "body": message
                    }
                }
            ]
        }
    })

    response = requests.put(
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    print(f"Status Code: {response.status_code}")
    print(f"Reason: {response.reason}")

    if response.status_code != 204:  # 204 No Content is expected for successful updates without a response body
        try:
            response_data = response.json()
            print(json.dumps(response_data, sort_keys=True, indent=4, separators=(",", ": ")))
        except json.JSONDecodeError:
            print("Response content is not in JSON format")
