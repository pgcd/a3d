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
    def __init__(self, queryset_or_list, per_page, filter_field = 'pk'):
        self.per_page = per_page
        self.filter_field = filter_field
        self.queryset_or_list = queryset_or_list
        self.reverse = False #This only applies to the display order.
    
    def page(self, context, list_name = 'object_list',
             count_only = False, **kwargs):
        """
        Retrieve an actual page (from start to start+per_page or per_page up to -start)
        """
        #TODO: Clean up code, move cases to own methods?
        result = {#Some defaults
                  'items_left':0,
                  'tip':0,
                  'more_low':None,
                  'more_high':None,
                  }
        start = context['request'].GET.get('start', kwargs.get('start', None))

        if start == 'last': #We want to select the last per_page items
            _qs = self.queryset_or_list.order_by(self.filter_field).reverse()
            result.update(_qs.aggregate(tip = Max(self.filter_field)))
            if count_only:
                return result
            else:
                _qs = _qs[0:self.per_page + 1]
            object_list = list(_qs)
            object_list.reverse()
            if len(object_list) > self.per_page:
                #start is "last", so there's nothing after this.
                object_list.pop(0)
                result["more_low"] = getattr(object_list[0], self.filter_field)
        elif not bool(start): #None or 0
            _qs = self.queryset_or_list
            result.update(_qs.aggregate(tip = Max(self.filter_field),
                                        items_left = Count('pk')))
            if count_only:
                return result
            else:
                _qs = _qs[0:self.per_page + 1]
            object_list = list(_qs)
            if len(object_list) > self.per_page:
                #Nothing before, but the last item can be used to get what's after
                object_list.pop()
                result["more_high"] = getattr(object_list[-1], self.filter_field)
            start = 0
        else:
            try:
                start = int(start)
                if start < 0:
                    #We're trying to retrieve the last per_page items up to @start
                    self.queryset_or_list = self.queryset_or_list.filter(**{"%s__lt" % self.filter_field: abs(start)}) #IGNORE:W0142
                    _qs = self.queryset_or_list.order_by(self.filter_field).reverse()
                    result.update(_qs.aggregate(tip = Max(self.filter_field)))
                    if count_only:
                        return result
                    else:
                        _qs = _qs[0:self.per_page + 1]
                    object_list = list(_qs)
                    object_list.reverse()
                    if len(object_list) > self.per_page:
                        object_list.pop(0)
                        result["more_low"] = getattr(object_list[0], self.filter_field)
                    #Try to use the top value for the result
                    try:
                        result["more_high"] = getattr(object_list[-1], self.filter_field, start - 1)
                    except IndexError:
                        pass
                else: # Regular :start, so we're using it as lower bound
                    self.queryset_or_list = self.queryset_or_list.filter(**{"%s__gt" % self.filter_field: start}) #IGNORE:W0142
                    _qs = self.queryset_or_list
                    result.update(_qs.aggregate(tip = Max(self.filter_field),
                                                items_left = Count('pk')))
                    if count_only:
                        return result
                    else:
                        _qs = _qs[0:self.per_page + 1]
                    object_list = list(_qs)
                    if len(object_list) > self.per_page:
                        object_list.pop()
                        result["more_high"] = getattr(object_list[-1], self.filter_field)
                    #Try to use the bottom value for the result
                    try:
                        result["more_low"] = getattr(object_list[0], self.filter_field, start + 1)
                    except IndexError:
                        pass
            except (TypeError, ValueError):
                #Any possible wrong "start" means start should be 0 
                start = 0
                
# this means we might have _something_ before the requested items, 
# so we return a "prev". Unless we are moving "up" (requesting 
# something that's after something)
# in which case we already know that there's something before this
        if context['request'].GET.get('discard_low', False): 
            result["more_low"] = None
        # same here 
        if context['request'].GET.get('discard_high', False): 
            result["more_high"] = None

        try:
            result['first_item'] = getattr(object_list[0], self.filter_field, 0)
            result['last_item'] = getattr(object_list[-1], self.filter_field, 0)
        except IndexError:
            result['first_item'] = result['last_item'] = 0
        #Please note that "tip" is different from first/last item,
        #in that it's the result of the not-limit'ed query

        result[list_name] = object_list
        result['items_left'] = max(result['items_left'] - self.per_page, 0) #FIXME:
        return result
