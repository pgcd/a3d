import hashlib

def tripcode(s):
    length = 13
    start = len(s)
    cons = 'bcdfghjlmnprstvxzbcdfgklmnyrstvw'
    vowels = "aeioue'"
    if s == '':
        import random
        s = ''.join([random.choice(cons + vowels) for _ in xrange(7)]) #@UnusedVariable
        length = random.randint(7, 11)
        

    p = hashlib.sha512(s * 7).digest()
    s = ''
    for e, i in enumerate(p):
        i = ord(i)
        _ = cons[i & 31]
        if i & 192 and e % 2:
            _ = _ * 2 
        s = s + _
        i = i / 32
        s = s + vowels[i % 7]
    
    return s[start:start + length]
    #return '%x' % hash(p)

class EndlessPage(object):
    def __init__(self, queryset_or_list, per_page, filter_field = 'pk'):
        self.per_page = per_page
        self.filter_field = filter_field
        self.queryset_or_list = queryset_or_list
        self.reverse = False #This only applies to the display order.
        
    def page(self, context, list_name = 'object_list', count_only = False, **kwargs):
        """
        This works but it's absolute crap. DO SOMETHING with the whole up/down thing.
        """
        result = {}
        more_down = None
        more_up = None
        start = context['request'].GET.get('start', kwargs.get('start', None))

        if start == 'last': #We want to select the last per_page items
            qs = self.queryset_or_list.order_by(self.filter_field).reverse()
            if count_only:
                return qs.count()
            else:
                qs = qs[0:self.per_page + 1]
            object_list = list(qs)
            object_list.reverse()
            if len(object_list) > self.per_page:
                more_down = getattr(object_list.pop(0), self.filter_field)
            result['items_left'] = 0 #Sensible approach as long as we use items_left
        elif not bool(start):
            qs = self.queryset_or_list
            if count_only:
                return qs.count()
            else:
                qs = qs[0:self.per_page + 1]
            object_list = list(qs)
            if len(object_list) > self.per_page:
                more_up = getattr(object_list.pop(), self.filter_field)
            start = 0
        else:
            try:
                start = int(start)
                if start < 0: #We're trying to retrieve the last per_page items up to :start
                    self.queryset_or_list = self.queryset_or_list.filter(**{"%s__lte" % self.filter_field: abs(start)}) #IGNORE:W0142
                    qs = self.queryset_or_list.order_by(self.filter_field).reverse()
                    if count_only:
                        return qs.count()
                    else:
                        qs = qs[0:self.per_page + 1]
                    object_list = list(qs)
                    object_list.reverse()
                    if len(object_list) > self.per_page:
                        more_down = getattr(object_list.pop(0), self.filter_field)
                    more_up = abs(start) + 1
                else: # Regular :start, so we're using it as lower bound
                    self.queryset_or_list = self.queryset_or_list.filter(**{"%s__gte" % self.filter_field: start}) #IGNORE:W0142
                    qs = self.queryset_or_list
                    if count_only:
                        return qs.count()
                    else:
                        qs = qs[0:self.per_page + 1]

                    object_list = list(qs)
                    if len(object_list) > self.per_page:
                        more_up = getattr(object_list.pop(), self.filter_field)
                    more_down = start - 1 #since we use LTE above
            except (TypeError, ValueError): #Any possible wrong "start" means start should be 0 
                start = 0
                
        
        if more_down is not None: 
            #this means we might have _something_ before the requested items, so we return a "prev".
            if start == 'last' or not context['request'].GET.get('up', False): 
                result["more_down"] = more_down

        if more_up is not None:
            if start == 0 or not context['request'].GET.get('down', False): 
                result["more_up"] = more_up

#        if len(object_list) > self.per_page:
#            if start>=0:
#                result[list_name] = object_list[0:self.per_page]
#            else
#                result[list_name] = object_list[1:self.per_page+1]
#        else:
        try:
            result['first_item'] = getattr(object_list[0], self.filter_field, 0)
            result['last_item'] = getattr(object_list[-1], self.filter_field, 0)
        except IndexError:
            result['first_item'] = result['last_item'] = 0
        
        result[list_name] = object_list
        total = self.queryset_or_list.count()
        if not result.has_key('items_left'):
            result['items_left'] = max(total - self.per_page, 0)
        return result
