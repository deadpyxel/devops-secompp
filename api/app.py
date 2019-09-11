import urllib.request, json
import os
from flask import Flask, jsonify, abort
from flask import request
from github import Github

app = Flask(__name__)

DEBUG = os.getenv('DEBUG', True)
TOKEN = os.getenv('API_TOKEN')

g = Github(TOKEN)


@app.route('/')
def get_repos():
    r = []

    try:
        args = request.args
        n = int(args['n'])
    except (ValueError, LookupError) as e:
        abort(
            jsonify(error="No integer provided for argument 'n' in the URL",
                    message=f"{e}"))

    repositories = g.search_repositories(query='language:python')[:n]

    for repo in repositories:
        with urllib.request.urlopen(repo.url) as url:
            data = json.loads(url.read().decode())
        r.append(data)

    return jsonify({'repos': r})


if __name__ == '__main__':
    app.run(debug=DEBUG)