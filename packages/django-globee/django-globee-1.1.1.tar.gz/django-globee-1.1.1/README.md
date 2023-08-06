# django-globee

[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/lovvskillz/django-globee/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/django-globee.svg)](https://badge.fury.io/py/django-globee)

django-globee is a Django app to integrate GloBee Payments.

Quick start
-----------

1. Add "globee" to your INSTALLED_APPS setting like this:
```python
    INSTALLED_APPS = [
        ...
        'globee',
    ]
```
2. Include the globee URLconf in your project urls.py like this:
```python
    path('globee/', include('globee.urls')),
```
    
3. Include your globee key and test or live env in your project settings.py
```python
    GLOBEE_AUTH_KEY = "YOUR GLOBEE X-AUTH-KEY"
    GLOBEE_TEST_MODE = True # or False
```


4. Run `python manage.py migrate` to create the globee models.


## example

### create GloBee payment

```python
from random import randint
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from globee.core import GlobeePayment

def my_payment_view(request):
    custom_payment_id = 'Your-custom-payment-id-%s' % randint(1, 9999999)
    payment_data = {
        'total': 10.50,
        'currency': 'USD',
        'custom_payment_id': custom_payment_id,
        'customer': {
            'name': request.user.username,
            'email': request.user.email
        },
        'success_url': request.build_absolute_uri(reverse('your-success-url')),
        'cancel_url': request.build_absolute_uri(reverse('your-cancel-url')),
        'ipn_url': request.build_absolute_uri(reverse('globee-ipn')),
    }
    payment = GlobeePayment(data=payment_data)
    # check required fields for globee payments
    if payment.check_required_fields():
        # create payment request
        if payment.create_request():
            # redirect to globee payment page
            return HttpResponseRedirect(payment.get_payment_url())
```

### get GloBee ipn signal

```python
from django.dispatch import receiver
from globee.models import PAYMENT_STATUS_GLOBEE_CONFIRMED
from globee.signals import globee_valid_ipn

@receiver(globee_valid_ipn)
def crypto_payment_ipn(sender, **kwargs):
    payment = sender
    
    # check if payment is confirmed or use any other payment status
    if payment.payment_status == PAYMENT_STATUS_GLOBEE_CONFIRMED:
        # get some payment infos
        amount = payment.total # payment amount
        currency = payment.currency # payment currency
        payment_id = payment.payment_id # payment id from GloBee
        custom_payment_id = payment.custom_payment_id # your custom payment id
        customer_email = payment.customer_email # customer email
        
        # Do more stuff
        # ...
        
```

if you don't trust the ipn response, you can also get the payment data from GloBee

```python
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from globee.models import PAYMENT_STATUS_GLOBEE_CONFIRMED
from globee.signals import globee_valid_ipn
from globee.core import GlobeePayment

@receiver(globee_valid_ipn)
def crypto_payment_ipn(sender, **kwargs):
    payment = sender
    globee_payment = GlobeePayment()
    
    try:
        # get the payment data from globee
        payment_data = globee_payment.get_payment_by_id(payment.payment_id)
        
        # check if payment is confirmed or use any other payment status
        if payment_data['status'] == PAYMENT_STATUS_GLOBEE_CONFIRMED:
            # get some payment infos
            amount = float(payment_data['total']) # payment amount
            currency = payment_data['currency'] # payment currency
            payment_id = payment_data['payment_id'] # payment id from GloBee
            custom_payment_id = payment_data['custom_payment_id'] # your custom payment id
            customer_email = payment_data['customer']['email'] # customer email
            
            # Do more stuff
            # ...
    except ValidationError as e:
        # payment not found or other error
        print(e)
```
