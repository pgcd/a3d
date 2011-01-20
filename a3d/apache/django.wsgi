import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../..')
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
os.environ['DJANGO_SETTINGS_MODULE']='a3d.settings'
import django.core.handlers.wsgi
def application(environ, start_response):
#    return debug(environ, start_response)
#    environ['SCRIPT_NAME']+='fake' 
    subapp=django.core.handlers.wsgi.WSGIHandler()
    return subapp(environ, start_response)

def debug(environ, start_response):
#import os
#
#def application(environ, start_response):
    import cStringIO
    headers=[]
    headers.append(('Content-Type', 'text/plain'))
    write=start_response('200 OK', headers)

    input=environ['wsgi.input']
    output=cStringIO.StringIO()

    keys=environ.keys()
    keys.sort()
    for key in keys:
        print>>output, '%s: %s'%(key, repr(environ[key]))
    print>>output

    output.write(input.read(int(environ.get('CONTENT_LENGTH', '0'))))

    return [output.getvalue()]




from a3d import monitor 
monitor.start(interval=1.0)
#monitor.track(os.path.join(os.path.dirname(__file__), 'site.cf'))
