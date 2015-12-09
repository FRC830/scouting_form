import sys

import bottle
from bottle import post, redirect, request, route, static_file, view

@route('/')
def callback():
    redirect('/form')

@route('/test')
def callback():
    return '1'

@route('/form')
@view('form')
def callback():
    return dict()

@post('/form/save')
def callback():
    f = request.forms
    data = {}
    for k in f:
        data[k] = f.get(k)
    print('Saving data')
    with open('_log.txt', 'a') as f:
        try:
            f.write(str(data))
            f.write('\n\n')
        except: # ugly
            pass
    redirect('/form')

@route('/static/<path:path>')
def callback(path):
    return static_file(path, 'static')

def main(args, adapter):
    app = bottle.app()
    app.run(host=args.host, port=args.port, debug=args.debug, server=adapter,
        reloader=args.reload, quiet=True)
