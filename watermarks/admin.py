
from django.contrib import admin

from watermarks.models import WatermarkImage, WatermarkText


class WatermarkAdmin(admin.ModelAdmin):

    list_display = [
        'name', 'position_x', 'position_y', 'opacity', 'scale', 'repeat']


admin.site.register(WatermarkImage, WatermarkAdmin)
admin.site.register(WatermarkText, WatermarkAdmin)
