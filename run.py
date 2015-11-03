import os, subprocess, sys, threading, time, webbrowser
if sys.version[0] == '2':
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

import util
util.logging_init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
def abspath(*parts):
    return os.path.join(os.getcwd(), *parts)

def add_submodule(name, check_file='.travis.yml'):
    sys.path.append(abspath('depends', name))
    if not os.path.exists(abspath('depends', name, check_file)):
        print('Warning: submodules not initialized properly')
        try:
            err = subprocess.call(['git', 'submodule', 'update', '--init'])
            assert not err, 'git error'
        except Exception as e:
            print('Failed to update submodules: %s' % e)
            sys.exit(1)

add_submodule('bottle')
add_submodule('waitress')
import bottle, waitress
bottle.TEMPLATE_PATH.extend([abspath('..', 'web'), abspath('web')])

class WaitressAdapter(bottle.WaitressServer):
    def run(self, handler):
        open_page()
        waitress.serve(handler, host=self.host, port=self.port, threads=6)

def server_running():
    try:
        c = urlopen('http://localhost:8000/test').read()
        if c == '1' or c == b'1':
            return True
    except Exception:
        pass
    return False

def open_page():
    if '--no-open' in sys.argv:
        return
    webbrowser.open('http://localhost:8000')

if server_running():
    print('Server already running')
    open_page()
else:
    print('Starting server')
    import web.server
    web.server.main('0.0.0.0', 8000, WaitressAdapter)
