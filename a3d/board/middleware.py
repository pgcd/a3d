'''
Created on 20/mag/2010

@author: pgcd
'''
import re
from operator import add
from time import time
from django.db import connection
import datetime

class StatsMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # turn on debugging in db backend to capture time
        from django.conf import settings

        debug = settings.DEBUG
        settings.DEBUG = True
        # get number of db queries before we do anything
        n = len(connection.queries) #@UndefinedVariable
        # time the view
        start = time()
        response = view_func(request, *view_args, **view_kwargs)
        totTime = time() - start
        # compute the db time for the queries just run
        queries = len(connection.queries) - n #@UndefinedVariable
        if queries:
            dbTime = reduce(add, [float(q['time']) 
                                  for q in connection.queries[n:]]) #@UndefinedVariable
        else:
            dbTime = 0.0
        # and backout python time
        pyTime = totTime - dbTime
        # restore debugging setting again
        settings.DEBUG = debug
        stats = {
            'totTime': totTime,
            'pyTime': pyTime,
            'dbTime': dbTime,
            'queries': queries,
            }

        # replace the comment if found            
        if response and response.content:
            s = response.content
            regexp = re.compile(r'(?P<cmt><!--\s*STATS:(?P<fmt>.*?)-->)')
            match = regexp.search(s)
            if match:
                s = s[:match.start('cmt')] + \
                    match.group('fmt') % stats + \
                    s[match.end('cmt'):]
                response.content = s

        return response


class CurrentUserPageMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):#IGNORE:W0613
        u = request.user
        if u.is_anonymous():
            return
        p = u.get_profile()
        p.last_page_url = request.path
        p.last_page_time = datetime.datetime.now()
        p.save()
        return
        
