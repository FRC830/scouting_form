import flask_wtf
import os
import wtforms.fields as fields
from wtforms.validators import DataRequired

try:
    import ConfigParser as configparser
    from ConfigParser import SafeConfigParser
except ImportError:
    import configparser
    from configparser import SafeConfigParser

_none = object()
class ConfigFile:
    _section = 'config'
    def __init__(self, path):
        self.path = path
        self.parser = SafeConfigParser()
        self.parser.read(path)

    def has(self, key):
        return self.parser.has_option(self._section, key)

    def get(self, key, default=_none):
        try:
            return self.parser.get(self._section, key)
        except configparser.Error:
            if default is _none:
                raise
            else:
                return default

    def set(self, key, value):
        if self._section not in self.parser.sections():
            self.parser.add_section(self._section)
        self.parser.set(self._section, key, value)

    def save(self):
        with open(self.path, 'w') as f:
            self.parser.write(f)

config = ConfigFile('config.txt')

class ConfigForm(flask_wtf.Form):
    computer_name = fields.StringField('Computer name',
        default=os.environ.get('COMPUTERNAME', None),
        validators=[DataRequired()])
