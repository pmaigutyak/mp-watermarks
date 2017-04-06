## Django-Watermarks

**Installation**
```
pip install django-watermarks
```

Add watermarks to INSTALLED_APPS of settings.py:

```
INSTALLED_APPS = [
    ...,
    'imagekit',
    'watermarks'
]
```

**Image processing**

```
from watermarks.models import WatermarkImage

watermark = WatermarkImage.get('example')
watermark.process('example.jpg')
```
