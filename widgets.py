# Customized versions of WTForms fields
# Note that all of the Field classes defined in this file render labels as well,
# while default Field classes do not
import wtforms.widgets as widgets
from wtforms.fields import *
from wtforms.fields.html5 import *
from wtforms.widgets import *

class CustomClassMixin(widgets.Input):
    custom_classes = []
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = ' '.join([c] + self.custom_classes)
        return super(CustomClassMixin, self).__call__(field, **kwargs)

# def custom_widget(widget_class, classes):
#     class widget(widget_class, CustomClassMixin):
#         custom_classes = list(classes)
#     return widget()

class _BootstrapGridDefaults:
    # This class is just used to give default attributes to BootstrapGridFieldMixin objects
    col_xs = 12
    col_sm = 6
    col_md = 4
    col_lg = None
    label_col_xs = 4
    label_col_sm = 4
    label_col_md = 5
    label_col_lg = None

class IntegerInput(widgets.html5.NumberInput, CustomClassMixin):
    custom_classes = ['form-control']
    def __call__(self, field, **kwargs):
        html = super(IntegerInput, self).__call__(field, **kwargs)
        return HTMLString('<span class="input-group">') + html + HTMLString('</span>')

class BootstrapGridField(Field, _BootstrapGridDefaults):
    def __init__(self, *args, **kwargs):
        # Copy col_* and label_col_* keyword arguments to the corresponding
        # attributes of this instance
        for k, v in list(kwargs.items()):
            if hasattr(_BootstrapGridDefaults, k):
                setattr(self, k, v)
                del kwargs[k]
        super(BootstrapGridField, self).__init__(*args, **kwargs)

    def __call__(self, **kwargs):
        classes = []
        label_classes = []
        for attr in dir(_BootstrapGridDefaults):
            name = attr.split('_')[-1]
            value = getattr(self, attr)
            if attr.startswith('col_') and value is not None:
                classes.append('col-%s-%i' % (name, value))
            if attr.startswith('label_col_') and value is not None:
                label_classes.append('col-%s-%i' % (name, value))

        html = super(BootstrapGridField, self).__call__(**kwargs)
        return self.generate_html(html, classes, label_classes)

    def generate_html(self, html, classes, label_classes):
        return (HTMLString('<div class="%s">' % ' '.join(classes)) +
                HTMLString('<div class="form-field">') +
                    self.label(class_ = ' '.join(label_classes)) +
                    html +
                HTMLString('</div>') +
            HTMLString('</div>'))

class IntegerField(IntegerField, BootstrapGridField):
    widget = IntegerInput()

class CheckboxButtonField(BooleanField, BootstrapGridField):
    def generate_html(self, html, classes, label_classes):
        classes.extend(['btn-group', 'checkbox-button-field'])
        return (HTMLString('<div class="%s" data-toggle="buttons">' % ' '.join(classes)) +
                HTMLString('<label class="btn btn-default">') +
                    html +
                    HTMLString(self.label.text) +
                HTMLString('</label>') +
            HTMLString('</div>'))
