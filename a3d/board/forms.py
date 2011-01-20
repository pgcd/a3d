'''
Created on 07/apr/2010

@author: pgcd
'''
from django import forms 
from board.models import PostData
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
import time
import re
#import datetime

class PostDataForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput, required = False)
    title = forms.CharField(required = False, max_length = 255, widget = forms.widgets.TextInput(attrs = {'size':'60'}))

    def __init__(self, target_object = None, data = None, request = None, initial = None, **kwargs):
        self.target_object = target_object
        self.request = request
        if self.target_object is None:
            self.attach_to_target = "prepend"
        else: 
            self.attach_to_target = "append"

        if initial is None:
            initial = {}
        initial.update(self.generate_initial_data())
        super(PostDataForm, self).__init__(data = data, initial = initial, **kwargs)

    
    def generate_initial_data(self):
        timestamp = int(time.time())
        response_title = {}
        if self.target_object is not None:
            ct = ContentType.objects.get_for_model(self.target_object)._get_pk_val()
            obj = str(self.target_object._get_pk_val())
            try:
                original_title = self.target_object.title
                if original_title.startswith('@[%s]' % self.request.user.username):
                    response_title = {'title':'@[%s]' % self.target_object.username}
            except AttributeError:
                pass
        else:
            ct = ContentType.objects.get_by_natural_key("board", "post")._get_pk_val()
            obj = 0
        
        security_dict = {
            'content_type'  : ct,
            'object_id'     : obj,
            'timestamp'     : str(timestamp),
        }
        security_dict.update(response_title)
        return security_dict

    def clean(self):
        cleaned_data = self.cleaned_data
        title = re.sub(r'^(@?\[.+?\])+', '', cleaned_data.get("title").strip())
        body_markup = cleaned_data.get("body_markup", '').strip()
        if body_markup == '' and title == '':
                msg = _(u"Devi inserire almeno uno tra titolo e testo.")
                self._errors["title"] = self.error_class([msg])
                self._errors["body_markup"] = self.error_class([msg])
                del cleaned_data["title"]
                del cleaned_data["body_markup"]
        return cleaned_data
        
    class Meta:
        model = PostData
        fields = ['username', 'password', 'title', 'body_markup', 'content_type', 'object_id', 'wiki']
        widgets = {
            'body_markup': forms.widgets.Textarea(attrs = {'cols': '80', 'rows': '15'}),
            'content_type': forms.widgets.HiddenInput(),
            'object_id': forms.widgets.HiddenInput(),
        }


class PostDataEditForm(PostDataForm):
    class Meta(PostDataForm.Meta):
        fields = ['title', 'body_markup', 'content_type', 'object_id', ]
