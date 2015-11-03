import inspect
import os
import string

_formatter = string.Formatter()

for singleton in ('left', 'right', 'center', 'top', 'bottom', 'middle'):
    globals()[singleton] = object()

class Field(object):
    raw_html = '''<div class="form-field {python_css_class_names} {css_class_names}" id="field-{id}">{html}</div>'''

    def __getitem__(self, k):
        return getattr(self, k, '{%s}' % k)

    @classmethod
    def can_create(cls):
        return type(cls) is type and \
                cls is not Field and \
                issubclass(cls, Field) and \
                hasattr(cls, 'title')

    @classmethod
    def class_id(cls):
        if cls.can_create():
            return cls.__name__
        else:
            raise AttributeError("Cannot create field of type %s" % cls.__name__)

    @property
    def id(self):
        return self.__class__.class_id()

    @property
    def css_class_names(self):
        return ' '.join(getattr(self, 'css_classes', []))

    @property
    def python_css_class_names(self):
        return ' '.join(list(map(lambda cls: 'py-%s' % cls.__name__.lower(),
            filter(lambda cls: issubclass(cls, Field), inspect.getmro(self.__class__)))))

    def format(self, s):
        return _formatter.vformat(s, (), self)

    def get_html(self):
        return self.format(Field.raw_html)


class TextField(Field):
    label_position = left
    input_type = 'text'
    @property
    def html(self):
        parts = [
            self.format('<label for="{id}" class="col-xs-4 control-label">{title}</label>'),
            self.format('<div class="col-xs-8"><input id="{id}" name="{id}" type="{input_type}" class="form-control"/></div>')
        ]
        if self.label_position == right:
            parts = parts[::-1]
        return '\n'.join(parts)

class NumberField(TextField):
    input_type = 'number'


class FormRenderer(object):
    def __init__(self, fields_path):
        self.fields = {}
        env = {}
        for k, v in globals().items():
            if not k.startswith('_'):
                env[k] = v
        with open(fields_path) as f:
            exec(f.read(), env, env)
        for k, v in env.items():
            if type(v) is type and issubclass(v, Field) and v.can_create():
                self.fields[k] = v()

    def field_html(self, field_id):
        # TODO: find out if SimpleTemplate actually supports functions
        # that generate template output and make this do that properly
        stdout = None
        for ref in inspect.stack():
            stdout = ref[0].f_locals.get('stdout', None)
            if stdout is not None:
                break
        if stdout is None:
            raise IOError("Couldn't find stdout")
        stdout.append(self.fields[field_id].get_html())

_renderer = FormRenderer(os.path.join(os.getcwd(), '..', 'web', 'fields.py'))
render_field = _renderer.field_html

