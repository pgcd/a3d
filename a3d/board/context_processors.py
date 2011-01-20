'''
Created on 02/mag/2010

@author: pgcd
'''
import settings
def base_template(request):
    media_url = settings.MEDIA_URL
    template_name = "base.html" #TODO: SET THIS IN SETTINGS
    if request.is_ajax():
        template_name = "base_ajax.html"
    return {'base_template':template_name, 'media_url': media_url}

def personal_settings(request):
    s = settings.A3D_BASE_SETTINGS
    if request.user.is_authenticated():
        userattrs = dict((i, ';'.join(v)) for i, v in request.user.get_profile().extended_attributes.items())
        s.update(dict((d, int(v) if v.isdigit() else v) for d, v in userattrs.items()))
    return {'personal_settings':s}
