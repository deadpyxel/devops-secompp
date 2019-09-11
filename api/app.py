import urllib.request, json
import os
from flask import Flask, jsonify, abort
from flask import request
from github import Github

app = Flask(__name__)

DEBUG = os.getenv('DEBUG', True)
TOKEN = os.getenv('API_TOKEN')
HOST = os.getenv('HOST', '127.0.0.1')
PORT = os.getenv('PORT', 5000)

g = Github(TOKEN)


@app.route('/')
def get_repos():
    r = []

    try:
        args = request.args
        n = int(args['n'])
        l = args['l']
    except (ValueError, LookupError) as e:
        abort(
            jsonify(error="You need to provide \'n\' and \'l\' argument",
                    message=f"{e}"))

    repositories = g.search_repositories(query=f'language:{l}')[:n]

    try:
        for repo in repositories:
            with urllib.request.urlopen(repo.url) as url:
                data = json.loads(url.read().decode())
            r.append(data)
        return jsonify({'repos': r, 'status': 'ok'})
    except IndexError as e:
        return jsonify({'repos': r, 'status': 'ko'})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
