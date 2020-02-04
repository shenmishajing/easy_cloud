from flask import Flask
from flask import request, redirect

app = Flask(__name__)


@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code = 301)


if __name__ == '__main__':
    app.run('127.0.0.1', threaded = True, debug = False, port = 8080)
