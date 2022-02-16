
import os

from imagekit.processors import ResizeToFit
from imagekit.lib import Image, ImageEnhance

from django.conf import settings


WATERMARKS = getattr(settings, 'WATERMARKS', {})


def _get_coordinates(position_x, position_y, img_size, wm_size):

    sh, sv = position_x, position_y

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


def insert_watermark(key, img_path):

    try:
        params = WATERMARKS[key]
    except KeyError:
        pass

    src_img = Image.open(img_path)

    wm = Image.open(os.path.join(settings.STATIC_ROOT, params['file']))
    wm_size = list(wm.size)

    if params.get('scale'):
        wm = ResizeToFit(src_img.size[0], src_img.size[1], True).process(wm)
        wm_size = wm.size

    layer = Image.new('RGBA', src_img.size, (0, 0, 0, 0))

    coordinates = _get_coordinates(
        params['position_x'],
        params['position_y'],
        src_img.size,
        wm_size
    )

    if params.get('repeat'):
        sx = coordinates[0] % wm_size[0] - wm_size[0]
        sy = coordinates[1] % wm_size[1] - wm_size[1]
        for x in range(sx, src_img.size[0], wm_size[0]):
            for y in range(sy, src_img.size[1], wm_size[1]):
                layer.paste(wm, (x, y))
    else:
        layer.paste(wm, coordinates)

    opacity = params.get('opacity', 1)

    if opacity < 1:
        alpha = layer.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        layer.putalpha(alpha)

    dst_img = Image.composite(layer, src_img, layer)

    os.remove(img_path)

    dst_img.save(img_path)
