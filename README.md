## MP-Shop

**Installation**
```
pip install django-mp-shop
```

### shop.currencies

**Installation**

Add currencies to settings.py:

```
from shop.currencies.constants import CURRENCY_UAH, CURRENCY_EUR, CURRENCY_USD

INSTALLED_APPS = [
	...,
	'shop.currencies'
]

CURRENCIES = (
    (CURRENCY_UAH, _('UAH')),
    (CURRENCY_USD, _('USD')),
    (CURRENCY_EUR, _('EUR')),
)
```

**Convert price**

```
from shop.currencies.models import ExchangeRate

# returns: 2700.0
ExchangeRate.convert(100, CURRENCY_USD, CURRENCY_UAH)

# returns: 2700.00
ExchangeRate.convert(100, CURRENCY_USD, CURRENCY_UAH, format_price=True)

# returns: 2700.00 UAH
ExchangeRate.convert(100, CURRENCY_USD, CURRENCY_UAH, printable=True)
```

**Get exchange rates**

```
from shop.currencies.models import ExchangeRate

# returns: {2: 27.10, 3: 29.00}
ExchangeRate.get_exchange_rates()
```

**Save default currency to session**

Add currencies to urls.py:

```
urlpatterns = [
    url(r'^currencies/', include('shop.currencies.urls', namespace='currencies')),
]
```

To get currency form, use 'get_currency_form' template tag:

```
{% load currencies %}

{% get_currency_form as form %}

<form method="post" action="{% url 'currencies:set-currency' %}?next={{ request.get_full_path }}">
	{% csrf_token %}
	
	{{ form }}
	
	<button type="submit">Change currency</button>
</form>
```

Get default currency from session:

```
from shop.currencies.settings import CURRENCY_SESSION_KEY

currency = request.session[CURRENCY_SESSION_KEY]
```
