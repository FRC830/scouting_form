# Customized versions of WTForms fields
import wtforms.widgets as widgets
from wtforms.fields import *
from wtforms.fields.html5 import *

class CustomClassMixin(widgets.Input):
    custom_classes = []
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = ' '.join([c] + self.custom_classes)
        return super(CustomClassMixin, self).__call__(field, **kwargs)

def custom_widget(widget_class, classes):
    class widget(widget_class, CustomClassMixin):
        custom_classes = list(classes)
    return widget()

class IntegerInput(widgets.html5.NumberInput, CustomClassMixin):
    custom_classes = ['form-control']
    def __call__(self, field, **kwargs):
        html = super(IntegerInput, self).__call__(field, **kwargs)
        return widgets.HTMLString('<span class="input-group">') + html + widgets.HTMLString('</span>')

class IntegerField(IntegerField):
    widget = IntegerInput()
