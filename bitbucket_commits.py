# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import json
from dotenv import load_dotenv
import os
from Jira_add_comment import add_comment

load_dotenv()
bitbucket_key = os.getenv('BITBUCKET_KEY')
def get_commit_info(commit):

  url = f"https://api.bitbucket.org/2.0/repositories/kobyrenfert292/first/commit/{commit}"
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

  author = data['author']['user']['display_name']
  date = data['date']
  message = data['message']
  commit_url = data['links']['html']['href']

  message_split = message.split()
  for word in message_split:
    parts = word.split('-')
    for index, part in enumerate(parts):
        if part.upper() in projects:
            try: #check for first part of issue
                issue = part.upper() + '-' + parts[index + 1]
                add_comment(issue, f"Commit ({commit}) by: {author} on {date}  :: {message}")
            except: #indicates the second part is not valid, so not a correct issue
                continue 
    
    
get_commit_info("5f0f293")
                