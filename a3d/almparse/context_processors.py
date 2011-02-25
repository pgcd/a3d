'''
Created on 14/giu/2010

@author: pgcd
'''
from almparse.models import Macro
def available_macros(request):
    s = [{'name':m.name,'content_required':bool(m.regex_match), 'desc':m.description} for m in Macro.objects.all()] #TODO: Filter by user/perm/group whatever
    return {'alm_available_macros':s}
