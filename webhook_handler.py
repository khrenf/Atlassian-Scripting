from flask import Flask, request, abort
from Jira_add_comment import add_comment

app = Flask(__name__)


projects = {'TEST'} 

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        
        data = request.json

        comment_data = data.get('comment', {})
        author = comment_data.get('user', {}).get('display_name')
        date = comment_data.get('created_on')
        message = comment_data.get('content', {}).get('raw')
        commit_url = comment_data.get('commit', {}).get('links', {}).get('html', {}).get('href')

        # print(f"Author: {author}")
        # print(f"Date: {date}")
        # print(f"Message: {message}")
        # print(f"Commit URL: {commit_url}")

        message_split = message.split()
        for word in message_split:
            parts = word.split('-')
            for index, part in enumerate(parts):
                if part.upper() in projects:
                    try: #check for first part of issue
                        issue = part.upper() + '-' + parts[index + 1]
                        add_comment(issue, f"Commit ({commit_url}) by: {author} on {date}  :: {message}")
                    except: #indicates the second part is not valid, so not a correct issue
                        continue 

        return 'sucess', 200
    else:
        abort(400)

if __name__ =='__main__':
    app.run()