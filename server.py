import os
import flask
import form_helper
app = flask.current_app

@app.route('/static/<path:path>')
def static_(path):
    return static_file(path, 'static')

@app.route('/test')
def test():
    return '1'

@app.route('/form', methods=('GET', 'POST'))
def form():
    f = form_helper.load_form(os.path.join(os.getcwd(), '..', 'web', 'fields.py'))()
    if f.validate_on_submit():
        print(f.data)
        return flask.redirect('/form')
    return flask.render_template('form.html', form=f)
