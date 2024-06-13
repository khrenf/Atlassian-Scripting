# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import json
from dotenv import load_dotenv
import os
from Jira_add_comment import add_comment

load_dotenv()
bitbucket_key = os.getenv('BITBUCKET_KEY')

url = "https://api.bitbucket.org/2.0/repositories/kobyrenfert292/first/commits"

headers = {
  "Accept": "application/json",
  "Authorization": f"Bearer {bitbucket_key}"
}

response = requests.request(
   "GET",
   url,
   headers=headers
)

# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
projects = {'TEST'}

data = response.json()
for commit in data['values']:
    author = commit['author']['user']['display_name']
    date = commit['date']
    message = commit['message']
    commit_url = commit['links']['html']['href']
    
    # print(f"Author: {author}")
    # print(f"Date: {date}")
    # print(f"Message: {message}")
    # print(f"URL: {commit_url}")
    # print("-" * 40)

    message = message.split() #split by spaces
    issue = ''
    for word in message:
        parts = word.split('-')
        for index, part in enumerate(parts):
            if part.upper() in projects:
                try: #check for first part of issue
                    issue = part.upper() + '-' + parts[index + 1]
                    add_comment(issue, f"updated by: {author} on {date}")
                except: #indicates the second part is not valid, so not a correct issue
                    continue 
                