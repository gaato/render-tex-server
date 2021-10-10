import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def help():
    return '/tex for math mode and /texp for text mode'

@app.route('/', methods=['POST'])
def render_tex():

    if request.json.get('code') is None:
        return None, 400
    if request.json.get('type') == 'png':
        if not request.json.get('plain'):
            r = subprocess.run(
                ['sudo', '-u', 'tex', '-i', 'python', '/home/tex/tex/tex.py'],
                input=request.json.get('code'),
                stdout=subprocess.PIPE,
                text=True,
            )
        else:
            r = subprocess.run(
                ['sudo', '-u', 'tex', '-i', 'python', '/home/tex/tex/tex.py', '-p'],
                input=request.json.get('code'),
                stdout=subprocess.PIPE,
                text=True,
            )
    elif request.json.get('type') == 'pdf':
        r = subprocess.run(
            ['sudo', '-u', 'tex', '-i', 'python', '/home/tex/tex/texpdf.py'],
            input=request.json.get('code'),
            stdout=subprocess.PIPE,
            text=True,
        )
    else:
        return None, 400
    if r.returncode == 0:
        result = {
            'status': 0,
            'result': r.stdout,
        }
    elif r.returncode == 1:
        result = {
            'status': 1,
            'error': r.stdout,
        }
    elif r.returncode == 2:
        result = {
            'status': 2,
        }
    else:
        return None, 500
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
