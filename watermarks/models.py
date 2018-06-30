
import os

from PIL import ImageFont
from imagekit.processors import ResizeToFit
from imagekit.lib import Image, ImageDraw, ImageColor, ImageEnhance

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Watermark(models.Model):

    name = models.CharField(_('Name'), max_length=255, unique=True)

    position_x = models.CharField(
        _('Position X'), max_length=255, default='center')

    position_y = models.CharField(
        _('Position Y'), max_length=255, default='center')

    opacity = models.FloatField(_('Opacity'), default=1)

    repeat = models.BooleanField(_('Repeat'), default=False)

    scale = models.BooleanField(_('Scale'), default=False)

    def _get_watermark(self):
        raise NotImplementedError

    def _process_coordinates(self, img_size, wm_size):
        """
        Given the dimensions of the image and the watermark as (x,y) tuples and a
        location specification, return the coordinates where the watermark should
        be placed according to the specification in a (x,y) tuple.
        Specification can use pixels, percentage (provided as a string, such as
        "30%"), or keywords such as top, bottom, center, left and right.
        """

        sh, sv = self.position_x, self.position_y

        if isinstance(sh, str) and '%' in sh:
            sh = int(img_size[0] * float(sh.rstrip("%")) / 100)

        if isinstance(sh, int) and sh < 0:
            sh = img_size[0] - wm_size[0] + sh

        if sh == 'left':
            sh = 0
        elif sh == 'center':
            sh = (img_size[0] - wm_size[0]) / 2
        elif sh == 'right':
            sh = img_size[0] - wm_size[0]

        if isinstance(sv, str) and '%' in sv:
            sv = int(img_size[1] * float(sv.rstrip("%")) / 100)

        if isinstance(sv, int) and sv < 0:
            sv = img_size[1] - wm_size[1] + sv

        if sv == 'top':
            sv = 0
        elif sv == 'center':
            sv = (img_size[1] - wm_size[1]) / 2
        elif sv == 'bottom':
            sv = img_size[1] - wm_size[1]

        return int(sh), int(sv)

    def process(self, img_path):

        src_img = Image.open(img_path)

        wm = self._get_watermark()
        wm_size = list(wm.size)

        if self.scale:
            wm = ResizeToFit(src_img.size[0], src_img.size[1], True).process(wm)
            wm_size = wm.size

        # # prepare image for overlaying (ensure alpha channel)
        # if src_img.mode != 'RGBA':
        #     src_img = src_img.convert('RGBA')

        # create a layer to place the watermark
        layer = Image.new('RGBA', src_img.size, (0, 0, 0, 0))
        coordinates = self._process_coordinates(src_img.size, wm_size)

        if self.repeat:
            sx = coordinates[0] % wm_size[0] - wm_size[0]
            sy = coordinates[1] % wm_size[1] - wm_size[1]
            for x in range(sx, src_img.size[0], wm_size[0]):
                for y in range(sy, src_img.size[1], wm_size[1]):
                    layer.paste(wm, (x, y))
        else:
            layer.paste(wm, coordinates)

        if self.opacity < 1:
            alpha = layer.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity)
            layer.putalpha(alpha)

        # merge watermark layer
        dst_img = Image.composite(layer, src_img, layer)

        os.remove(img_path)

        dst_img.save(img_path)

    @classmethod
    def get(cls, name):
        return cls.objects.get(name=name)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class WatermarkImage(Watermark):

    image = models.ImageField(_('Image'), blank=False, upload_to='watermarks')

    def _get_watermark(self):
        return Image.open(self.image.path)

    class Meta:
        verbose_name = _('Watermark image')
        verbose_name_plural = _('Watermark images')


class WatermarkText(Watermark):

    text = models.CharField(_('Text'), max_length=255, blank=False, null=False)

    font_file = models.FileField(
        _('Font file'), blank=True, upload_to='watermarks')

    font_size = models.IntegerField(_('Font size'), blank=False, default=16)

    font_color = models.CharField(
        _('Font color'), max_length=10, blank=False, default='black')

    @property
    def _font(self):

        if not self.font_file:
            return ImageFont.load_default()

        font_path = self.font_file.path

        if font_path.endswith(".pil"):
            # bitmap font (size doesn't matter)
            return ImageFont.load(font_path)

        # true type font (size matters)
        return ImageFont.truetype(font_path, self.font_size)

    @property
    def _text_color(self):
        return ImageColor.getrgb(self.font_color)

    def _get_watermark(self):
        watermark = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark, "RGBA")
        draw.text((0, 0), self.text, font=self._font, fill=self._text_color)
        return watermark

    class Meta:
        verbose_name = _('Watermark text')
        verbose_name_plural = _('Watermark texts')
