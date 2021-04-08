
class WatermarksSettings(object):

    @property
    def INSTALLED_APPS(self):
        apps = super().INSTALLED_APPS + ['watermarks']

        if 'imagekit' not in apps:
            apps.append('imagekit')

        return apps


default = WatermarksSettings
