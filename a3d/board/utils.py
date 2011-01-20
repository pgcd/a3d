#def render_to_ajax_response(template_name, *args, **kwargs):
#    if kwargs["context_instance"]["request"].is_ajax():
#        template_name=template_name.replace('.html','_ajax.html')
#    return render_to_response(template_name, *args, **kwargs)

from django.conf import settings
import hashlib
import sys

def tripcode(s):
    length = 9
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

def __deprecated__get_setting(request, setting_name, default = None):
    """
    @param setting_name: lowercase name of the required setting value 
    """
    #cached_settings = self.extended_attributes.select_related().all().values_list('key__name','value')
    #print cached_settings
    if request.user.is_authenticated():
        try:
            setting = getattr(request.user.get_profile(), setting_name)
#            print "1: %s %s"%(setting_name, setting)
        except AttributeError:
            try:
                setting = request.user.get_profile().extended_attributes.get(key__name = setting_name).value
#                print "2: %s %s"%(setting_name, setting)
            except:
                setting = getattr(settings, setting_name.upper(), default)
#                print "3: %s %s"%(setting_name, setting)
    else:
        setting = getattr(settings, setting_name.upper(), default)
#        print "4: %s %s"%(setting_name, setting)
    #setting = cached_settings.get(setting_name, self.__dict__.get(setting_name, settings.__dict__.get(setting_name, None)))
    return setting


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
            qs = self.queryset_or_list.order_by(self.filter_field).reverse()[0:self.per_page + 1]
            if count_only:
                return qs.count()
            object_list = list(qs)
            object_list.reverse()
            if len(object_list) > self.per_page:
                more_down = getattr(object_list.pop(0), self.filter_field)
            result['items_left'] = 0 #Sensible approach as long as we use items_left
        elif not bool(start):
            qs = self.queryset_or_list[0:self.per_page + 1]
            if count_only:
                return qs.count()
            object_list = list(qs)
            if len(object_list) > self.per_page:
                more_up = getattr(object_list.pop(), self.filter_field)
            start = 0
        else:
            try:
                start = int(start)
                if start < 0: #We're trying to retrieve the last per_page items up to :start
                    self.queryset_or_list = self.queryset_or_list.filter(**{"%s__lte" % self.filter_field: abs(start)})
                    qs = self.queryset_or_list.order_by(self.filter_field).reverse()[0:self.per_page + 1]
                    if count_only:
                        return qs.count()
                    object_list = list(qs)
                    object_list.reverse()
                    if len(object_list) > self.per_page:
                        more_down = getattr(object_list.pop(0), self.filter_field)
                    more_up = abs(start) + 1
                else: # Regular :start, so we're using it as lower bound
                    self.queryset_or_list = self.queryset_or_list.filter(**{"%s__gte" % self.filter_field: start})
                    qs = self.queryset_or_list[0:self.per_page + 1]
                    if count_only:
                        return qs.count()

                    object_list = list(qs)
                    if len(object_list) > self.per_page:
                        more_up = getattr(object_list.pop(), self.filter_field)
                    more_down = start - 1 #since we use LTE above
            except:
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
            result['items_left'] = max(total - self.per_page, 0) #FIXME: Temporary approach?
        return result
