import os
import exporter
import flask
import form_helper
app = flask.current_app

custom = flask.Blueprint('custom', 'custom', static_url_path='/static/custom', static_folder=os.path.join('..', 'web'))
app.register_blueprint(custom)

@app.route('/')
def root():
    return flask.redirect(flask.url_for('form'))

@app.route('/test')
def test():
    return '1'

@app.route('/form', methods=('GET', 'POST'))
def form():
    f = form_helper.load_form(os.path.join(os.getcwd(), '..', 'web', 'fields.py'))()
    if f.validate_on_submit():
        print(f.data)
        exporter.save_data(f.data, os.path.join(os.getcwd(), '..', 'test.csv'))
        return flask.redirect('/form')
    return flask.render_template('form.html', form=f)
