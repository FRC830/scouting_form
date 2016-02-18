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
    if f.validate_on_submit():#Form data is valid
    	#this will save data entered on the form to a new line in the csv file
    	#Ex: Red1_scouting_data.csv (if running on computer Red1)
        fieldnames = []
        for field in f:
            if field.name != "csrf_token":
                fieldnames.append(field.name)
        exporter.save_data(fieldnames, f.data, os.path.join(os.getcwd(),'..', os.environ['COMPUTERNAME']+"_scouting_data.csv"))
        return flask.redirect('/form')
    return flask.render_template('form.html', form=f)
 
