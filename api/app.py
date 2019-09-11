from flask import Flask, jsonify, abort
import urllib.request, json
from flask import request

app = Flask(__name__)

from github import Github
g = Github("d6c9b24658480460bbdd78125c99b766b43648ff")


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
    app.run(debug=True)