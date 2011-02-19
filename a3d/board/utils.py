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
    def __init__(self, queryset_or_list, per_page = 30, filter_field = 'pk'):
        self.per_page = per_page
        self.filter_field = filter_field
        self.queryset_or_list = queryset_or_list
        self.reverse = False #This only applies to the display order.
        self.result = {#Some defaults
                  'items_left':0,
                  'tip':0,
                  'more_low':None,
                  'more_high':None,
                  }
        self.object_list = []
    
    def get_last_page(self, count_only):
        '''
        Get the last per_page items for the current queryset.
         
        @param count_only:
        '''
        _qs = self.queryset_or_list.order_by(self.filter_field).reverse()
        self.result.update(_qs.aggregate(tip = Max(self.filter_field)))
        if count_only:
            return
        _qs = _qs[0:self.per_page + 1]
        self.object_list = list(_qs)
        self.object_list.reverse()
        if len(self.object_list) > self.per_page:
            #start is "last", so there's nothing after this.
            self.object_list.pop(0)
            self.result["more_low"] = getattr(self.object_list[0], self.filter_field)

    
    def get_first_page(self, count_only):
        '''
        Get the first per_page items of the current queryset
        @param count_only:
        '''
        _qs = self.queryset_or_list
        self.result.update(_qs.aggregate(tip = Max(self.filter_field),
                                    items_left = Count('pk')))
        if count_only:
            return
        _qs = _qs[0:self.per_page + 1]
        self.object_list = list(_qs)
        if len(self.object_list) > self.per_page:
            #Nothing before, but the last item can be used to get what's after
            self.object_list.pop()
            self.result["more_high"] = getattr(self.object_list[-1], self.filter_field)
        self.result['items_left'] = self.result['items_left'] - len(self.object_list)

    
    def get_page_after(self, start, count_only):
        self.queryset_or_list = self.queryset_or_list.filter(**{"%s__gt" % self.filter_field: start}) #IGNORE:W0142
        _qs = self.queryset_or_list
        self.result.update(_qs.aggregate(tip = Max(self.filter_field),
                                    items_left = Count('pk')))
        if count_only:
            return
        _qs = _qs[0:self.per_page + 1]
        self.object_list = list(_qs)
        if len(self.object_list) > self.per_page:
            self.object_list.pop()
            self.result["more_high"] = getattr(self.object_list[-1], self.filter_field)
        #Try to use the bottom value for the result
        try:
            self.result["more_low"] = getattr(self.object_list[0], self.filter_field, start + 1)
        except IndexError:
            pass
        self.result['items_left'] = self.result['items_left'] - len(self.object_list)

    
    def get_page_before(self, start, count_only):
        self.queryset_or_list = self.queryset_or_list.filter(**{"%s__lt" % self.filter_field: abs(start)}) #IGNORE:W0142
        _qs = self.queryset_or_list.order_by(self.filter_field).reverse()
        self.result.update(_qs.aggregate(tip = Max(self.filter_field)))
        if count_only:
            return
        _qs = _qs[0:self.per_page + 1]
        self.object_list = list(_qs)
        self.object_list.reverse()
        if len(self.object_list) > self.per_page:
            self.object_list.pop(0)
            self.result["more_low"] = getattr(self.object_list[0], self.filter_field)
        #Try to use the top value for the result
        try:
            self.result["more_high"] = getattr(self.object_list[-1], self.filter_field, start - 1)
        except IndexError:
            pass
    
    def page(self, context, list_name = 'object_list',
             count_only = False, **kwargs):
        """
        Retrieve an actual page (from start to start+per_page or per_page up to -start)
        """
        start = context['request'].GET.get('start', kwargs.get('start', None))

        if start == 'last': #We want to select the last per_page items
            self.get_last_page(count_only)
        else:
            try:
                start = int(start)
                if start < 0:
                    #We're trying to retrieve the last per_page items up to @start
                    self.get_page_before(start, count_only)
                elif start > 0: # Regular :start, so we're using it as lower bound
                    self.get_page_after(start, count_only)
            except (TypeError, ValueError):
                #Any possible wrong "start" means start should be 0 
                self.get_first_page(count_only)
        if count_only: #This is the best place to return if we don't have an object_list
            return self.result
                
# this means we might have _something_ before the requested items, 
# so we return a "prev". Unless we are moving "up" (requesting 
# something that's after something)
# in which case we already know that there's something before this
        if context['request'].GET.get('discard_low', False): 
            self.result["more_low"] = None
        # same here 
        if context['request'].GET.get('discard_high', False): 
            self.result["more_high"] = None

        try:
            self.result['first_item'] = getattr(self.object_list[0], self.filter_field, 0)
            self.result['last_item'] = getattr(self.object_list[-1], self.filter_field, 0)
        except IndexError:
            self.result['first_item'] = self.result['last_item'] = 0
        #Please note that "tip" is different from first/last item,
        #in that it's the result of the not-limit'ed query

        self.result[list_name] = self.object_list
        return self.result
