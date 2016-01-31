import flask
app = flask.current_app

@app.route('/static/<path:path>')
def static_(path):
    return static_file(path, 'static')

@app.route('/test')
def test():
    return '1'
