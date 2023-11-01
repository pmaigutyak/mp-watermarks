### Watermarks

* add `django-watermarks` to `requirements.txt`
* add `watermarks` to `INSTALLED_APPS`
* add images using example:
```
WATERMARKS = {
    'product': {
        'opacity': 0.6,
        'position_x': 'center',
        'position_y': 'bottom',
        'file': 'product-watermark.png'
    }
}
```
* use `watermarks.utils.insert_watermark` method to process image
```
from watermarks.utils import insert_watermark
 
try:
    insert_watermark('product', instance.file.path)
except Exception as e:
    pass
```
