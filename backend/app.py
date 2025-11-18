import flask
import os

MAGIC_WORD = "WipeAllDataNow"

app = flask.Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    try:
        state = open('status.txt', 'r').read()
        return flask.jsonify({'status': f'{state} devices started to wipe'}), 200
    except:
        return flask.jsonify({'status': 'no command issued'}), 200

@app.route('/command', methods=['GET'])
def command():
    try:
        fp = open('status.txt', 'r+')
        state = int(fp.read())
        fp.seek(0)
        state += 1
        fp.write(str(state))
        fp.close()
        return MAGIC_WORD, 200
    except:
        return "", 200
    
@app.route('/wipe_now', methods=['GET'])
def wipe_now():
    if os.path.exists('status.txt'):
        # already started, do nothing
        pass
    else:
        open('status.txt', 'w').write('0')
    # redirect to status page
    return flask.redirect('/status')

@app.route('/reset', methods=['GET'])
def reset():
    try:
        os.remove('status.txt')
        return flask.jsonify({'reset': True}), 200
    except:
        return flask.jsonify({'reset': False}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)