
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WatermarksAppConfig(AppConfig):

    name = 'watermarks'
    verbose_name = _('Watermarks')


default_app_config = 'watermarks.WatermarksAppConfig'
