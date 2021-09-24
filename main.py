import os
import subprocess

from flask import Flask, jsonify

app = Flask(__name__)
here = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def help():
    return '/tex for math mode and /texp for text mode'

@app.route('/tex/<s>', methods=['GET'])
def render_tex(s=None):

    r = subprocess.run(
        ['sudo', '-u', 'tex', '-i', 'python', f'{here}/tex/tex.py'],
        input=s,
        stdout=subprocess.PIPE,
        text=True,
    )
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

@app.route('/texp/<s>', methods=['GET'])
def render_texp(s=None):

    r = subprocess.run(
        ['sudo', '-u', 'tex', '-i', 'python', f'{here}/tex/tex.py', '-p'],
        input=s,
        stdout=subprocess.PIPE,
        text=True,
    )
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


@app.route('/texpdf/<s>', methods=['GET'])
def render_texpdf(s=None):

    r = subprocess.run(
        ['sudo', '-u', 'tex', '-i', 'python', f'{here}/tex/texpdf.py'],
        input=s,
        stdout=subprocess.PIPE,
        text=True,
    )
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
    app.run(host='localhost', port=80)
