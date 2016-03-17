import flask
import os
import shutil
import sys
import time

import config
import exporter
import form_helper
import util
conf = config.config

app = flask.current_app
request = flask.request

custom = flask.Blueprint('custom', 'custom', static_url_path='/static/custom', static_folder=os.path.join('..', 'web'))
app.register_blueprint(custom)

def csv_filename():
    return conf.get('computer_name', '')+"_scouting_data.csv"
def csv_path():
    return util.abspath('..',csv_filename())

@app.route('/')
def root():
    return flask.redirect(flask.url_for('form'))

@app.route('/test')
def test():
    return '1'

@app.route('/form', methods=('GET', 'POST'))
def form():
    if not conf.get('computer_name', ''):
        return flask.redirect(flask.url_for('config_form', return_to='/form'))
    f = form_helper.load_form(os.path.join(os.getcwd(), '..', 'web', 'fields.py'))()
    if f.validate_on_submit():
    	# this will save data entered on the form to a new line in the csv file
    	# Ex: Red1_scouting_data.csv (if running on computer Red1)
        fieldnames = []
        for field in f:
            if field.type != "CSRFTokenField":
                fieldnames.append(field.name)
        exporter.save_data(fieldnames, f.data, csv_path())
        return flask.redirect('/form')
    return flask.render_template('form.html', form=f, conf=conf)

@app.route('/config', methods=('GET', 'POST'))
def config_form(return_to=None):
    return_to = return_to or request.args.get('return_to', None)
    f = config.ConfigForm()
    success = False
    if f.validate_on_submit():
        for field in f:
            if field.type != "CSRFTokenField":
                conf.set(field.name, f.data[field.name])
        conf.save()
        if return_to:
            return flask.redirect(return_to)
        else:
            success = True
    return flask.render_template('config_form.html', form=f, success=success)

def get_export_path():
    path = conf.get('export_path', '')
    if not path:
        path = {'darwin': '/Volumes/SCOUTING', 'win32': 'E:\\'}.get(sys.platform, '')
    return path

@app.route('/export')
def export_form():
    return flask.render_template('export.html', default_path=get_export_path())

@app.route('/export/<command>')
def export_handler(command):
    def path_ok(path):
        return os.path.isdir(path) and not os.path.exists(os.path.join(path, csv_filename()))
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
            shutil.copyfile(csv_path(), os.path.join(path, csv_filename()))
            shutil.move(csv_path(), util.abspath('backups', '%s-%s' % (csv_filename(), time.strftime('%d-%b-%Y-%H-%M-%S-%p'))))
            return flask.jsonify(ok=True)
        except Exception as e:
            return flask.jsonify(ok=False, error=str(e))
    else:
        flask.abort(404)

@app.route('/stats')
def stats():
    lines = 0
    if os.path.isfile(csv_path()):
        with open(csv_path()) as f:
            lines = max(0, len(f.readlines()) - 1)
    return flask.jsonify(
        lines=lines
    )
