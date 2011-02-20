import hashlib
from django.db.models import Count, Max, Min

def tripcode(res):
    length = 13
    start = len(res)
    cons = 'bcdfghjlmnprstvxzbcdfgklmnyrstvw'
    vowels = "aeioue'"
    if res == '':
        import random
        res = ''.join([random.choice(cons + vowels) for _ in xrange(7)])
        length = random.randint(7, 11)
        

    digest = hashlib.sha512(res * 7).digest()
    res = ''
    for idx, i in enumerate(digest):
        i = ord(i)
        _ = cons[i & 31]
        if i & 192 and idx % 2:
            _ = _ * 2 
        res = res + _
        i = i / 32
        res = res + vowels[i % 7]
    
    return res[start:start + length]
    #return '%x' % hash(p)

class EndlessPage(object):#IGNORE:R0903
    '''
    Paginate endlessly (ie. without page numbers) a queryset or list 
    '''
    def __init__(self, queryset, per_page = 30, filter_field = 'pk'):
        self.per_page = per_page
        self.filter_field = filter_field
        self.queryset = queryset
        self.result = {#Some defaults
                  'items_left':0,
                  'tip':0,
                  'has_prev':None,
                  'has_next':None,
                  }
        self.object_list = []
    
    def _get_last_page(self):
        '''
        Get the last per_page items for the current queryset.
         
        @param stats_only:
        '''
        self.object_list = list(self.queryset[0:self.per_page + 1])
        if len(self.object_list) > 0: 
            self.result['tip'] = getattr(self.object_list[0], self.filter_field)
        if len(self.object_list) > self.per_page:
            #start is "last", so there's nothing after this.
            self.object_list.pop()
            self.result["has_prev"] = getattr(self.object_list[0], self.filter_field)


    
    def _get_first_page(self):
        '''
        Get the first per_page items of the current queryset
        @param stats_only:
        '''
        self.object_list = list(self.queryset[0:self.per_page + 1])
        if len(self.object_list) > self.per_page:
            #Nothing before, but the last item can be used to get what's after
            self.object_list.pop()
            self.result["has_next"] = getattr(self.object_list[-1], self.filter_field)
        if len(self.object_list) > 0:
            _ = max(self.object_list, key=lambda x: getattr(x,self.filter_field))
            self.get_stats(start=getattr(_,self.filter_field))

    
    def _get_page_after(self, start):
        self.object_list = list(self.queryset[0:self.per_page + 1])
        if len(self.object_list) > self.per_page:
            self.object_list.pop()
            self.result["has_next"] = getattr(self.object_list[-1], self.filter_field)
        #Try to use the bottom value for the result
        try:
            self.result["has_prev"] = getattr(self.object_list[0], self.filter_field, start + 1)
        except IndexError:
            pass
        if len(self.object_list) > 0:
            self.get_stats(start=getattr(self.object_list[-1], self.filter_field))

    
    def _get_page_before(self, start):
        self.object_list = list(self.queryset[0:self.per_page + 1])
        if len(self.object_list) > self.per_page:
            self.object_list.pop(0)
            self.result["has_prev"] = getattr(self.object_list[0],
                                              self.filter_field)
        #Try to use the top value for the result
        try:
            self.result["has_next"] = getattr(self.object_list[-1],
                                              self.filter_field, start - 1)
        except IndexError:
            pass
        #self.get_stats(start=start)

    
    def get_stats(self, request = None, start = None, filt = '%s__gt'):
        '''
        
        @param request:
        @param start:
        @param filt:
        '''
        if request is not None:
            start = request.GET.get('start', 0)
        self.result.update(self.queryset.filter(#IGNORE:W0142
                                    **{filt % self.filter_field: start}
                                ).aggregate(
                                    tip = Max(self.filter_field),
#                                    bottom = Min(self.filter_field),
                                    items_left = Count('pk')))
        #if we don't have anything above @start, we return start as the tip
        if self.result['tip'] is None:
            self.result['tip'] = start
        return self.result

    
    def page(self, request = None, list_name = 'object_list',
             start = None):
        '''
        
        @param request:
        @param list_name:
        @param stats_only:
        @param start:
        '''
        if request is not None:
            start = request.GET.get('start', None)

        if start == 'last': #We want to select the last per_page items
            self.queryset = self.queryset.reverse()
            self._get_last_page()
        else:
            try:
                start = int(start)
                if start < 0:
                    #We're trying to retrieve the last per_page items up to @start
                    self.queryset = self.queryset.filter(**{"%s__lt" % self.filter_field: abs(start)}) #IGNORE:W0142
                    self.queryset = self.queryset.reverse()
                    self._get_page_before(start)
                elif start > 0: # Regular :start, so we're using it as lower bound
                    if request is not None and request.GET.has_key('inclusive'):
                        self.queryset = self.queryset.filter(**{"%s__gte" % self.filter_field: start}) #IGNORE:W0142
                    else:
                        self.queryset = self.queryset.filter(**{"%s__gt" % self.filter_field: start}) #IGNORE:W0142
                    self._get_page_after(start)
                else:
                    self._get_first_page()
            except (TypeError, ValueError):
                #Any possible wrong "start" means start should be 0 
                self._get_first_page()
                
# this means we might have _something_ before the requested items, 
# so we return a "prev". Unless we are moving "up" (requesting 
# something that's after something)
# in which case we already know that there's something before this

        if request is not None and request.GET.get('discard_low', False): 
            self.result["has_prev"] = None
        # same here 
        if request is not None and request.GET.get('discard_high', False): 
            self.result["has_next"] = None

        try:
            self.result['first_item'] = getattr(self.object_list[0], self.filter_field, 0)
            self.result['last_item'] = getattr(self.object_list[-1], self.filter_field, 0)
        except IndexError:
            self.result['first_item'] = self.result['last_item'] = 0
        #Please note that "tip" is different from first/last item,
        #in that it's the result of the not-limit'ed query

        self.result[list_name] = self.object_list
        return self.result
