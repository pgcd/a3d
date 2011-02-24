from django import forms

class CssPreviewWidget(forms.Textarea):
    def __init__(self, attrs = None, sampletext = 'Sample'):
        self.sampletext = sampletext
        super(CssPreviewWidget, self).__init__(attrs)        

    def render(self, name, value, attrs = None):
        widget = super(CssPreviewWidget, self).render(name, value, attrs)
        return '%s<span id="%s_sample" style="%s">%s</span>' % (widget, name, value, self.sampletext)
