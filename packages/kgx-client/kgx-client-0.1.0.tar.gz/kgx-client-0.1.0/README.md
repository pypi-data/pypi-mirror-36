

Django-Oscar Settings


```python
# settings.py

KGX = {
    # required
    'CREDENTIALS': ('my_user', 'my_p@$$w0rd'),
    
    # optional -- default False
    'SANDBOX_MODE': False,
    
    # weight attribute code
    # this is necessary to calculate
    # shipping costs -- this field
    # **must** be a float and will
    # be assumed in kilograms
    'WEIGHT_ATTR_CODE': 'berat',
    
    # default weight to assume
    # if your products do not have a shipping
    # weight.  This will default to 1
    'DEFAULT_WEIGHT_KGS': 1,
    
    # ignore the shipping address from the partner
    # use the following address for all shipments
    'OVERRIDE_SHIPPING_ADDRESS': {
        '12345'
    }
}
```