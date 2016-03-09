import flask
import os
import shutil
import sys

import config
import exporter
import form_helper
conf = config.config

app = flask.current_app
request = flask.request

custom = flask.Blueprint('custom', 'custom', static_url_path='/static/custom', static_folder=os.path.join('..', 'web'))
app.register_blueprint(custom)

CSV_FILENAME = conf.get('computer_name')+"_scouting_data.csv"

@app.route('/')
def root():
    return flask.redirect(flask.url_for('form'))

@app.route('/test')
def test():
    return '1'

@app.route('/form', methods=('GET', 'POST'))
def form():
    if not conf.get('computer_name', ''):
        return flask.redirect('/config')
    f = form_helper.load_form(os.path.join(os.getcwd(), '..', 'web', 'fields.py'))()
    if f.validate_on_submit():
    	# this will save data entered on the form to a new line in the csv file
    	# Ex: Red1_scouting_data.csv (if running on computer Red1)
        fieldnames = []
        for field in f:
            if field.type != "CSRFTokenField":
                fieldnames.append(field.name)
        exporter.save_data(fieldnames, f.data, os.path.join(os.getcwd(),'..', CSV_FILENAME))
        return flask.redirect('/form')
    return flask.render_template('form.html', form=f)

@app.route('/config', methods=('GET', 'POST'))
def config_page():
    f = config.ConfigForm()
    if f.validate_on_submit():
        for field in f:
            if field.type != "CSRFTokenField":
                conf.set(field.name, f.data[field.name])
        conf.save()
        return flask.redirect('/form')
    return flask.render_template('config_form.html', form=f)

def get_export_path():
    path = conf.get('export_path', '')
    if not path:
        path = {'darwin': '/Volumes/SCOUTING', 'win32': 'E:\\'}.get(sys.platform, '')
    return path

@app.route('/export')
def export_page():
    return flask.render_template('export.html', default_path=get_export_path())

@app.route('/export/<command>')
def export_handler(command):
    def path_ok(path):
        return os.path.isdir(path) and not os.path.exists(os.path.join(path, CSV_FILENAME))
    path = os.path.expanduser(request.args.get('path', get_export_path()))
    if command == 'check_path':
        ok = path_ok(path)
        if ok:
            conf.set('export_path', path)
            conf.save()
        return flask.jsonify(ok=ok)
    elif command == 'do_export':
        if not path_ok(path):
            return flask.jsonify(ok=False, error="Invalid path: %s" % path)
        try:
            shutil.copyfile(os.path.join(os.getcwd(),'..', CSV_FILENAME),
                os.path.join(path, CSV_FILENAME))
            return flask.jsonify(ok=True)
        except Exception as e:
            return flask.jsonify(ok=False, error=str(e))
    else:
        flask.abort(404)
