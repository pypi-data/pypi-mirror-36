from django.core.exceptions import ObjectDoesNotExist
from rest_framework import fields
import six

from . import conf


_IGNORE_INIT_RESET = conf.IGNORE_INIT_RESET
_REPR_NAME = conf.DRF_REPRESENTATION_NAME_NOT_ID


class LookupSerializerField(fields.ChoiceField):

    def __init__(self, model, **kwargs):
        self.model = model
        self._choices = None
        super(LookupSerializerField, self).__init__([], **kwargs)
        if not _IGNORE_INIT_RESET:
            self._reset_choices()

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return None
        self._reset_choices()
        try:
            return self.model.objects.get(id=self.choice_strings_to_values[six.text_type(data)])
        except (KeyError, ObjectDoesNotExist):
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        if value is None:
            return value
        return super(LookupSerializerField, self).to_representation(value.name if _REPR_NAME else value.id)

    def iter_options(self):
        '''
        Helper method for use with templates rendering select widgets.
        '''
        self._reset_choices()
        return super(LookupSerializerField, self).iter_options()

    def _reset_choices(self):
        self._choices = None
        self._set_choices(self._get_choices())

    def _get_choices(self):
        if self._choices is None or len(self._choices) == 0:
            self._choices = [(i.id, i) for i in self.model.objects.all()]
        return self._choices


class LookupTableItemSerializerField(object):

    def __init__(self, *args, **kwargs):
        raise Exception('this class is no longer supported; see Betas.md for upgrade information')
