# RetailCRM API v5 wrapper

# Installation

Install using `pip`...

    pip install retail-crm api

Or

    git clone https://github.com/bzdvdn/retailcrm-api.git

    python3 setup.py

# Usage

```python
from retail import  RetailAPI
api = RetailAPI("https://shop123.retailcrm.ru", "<token>") # init retail api

orders = api.orders() # return full paginated rusults from /api/v5/orders endpoint
orders_history = api.orders.history() # return full paginated rusults from /api/v5/orders/history endpoint

# add order or another object
import json
json_params = {"firstName": "Test", "lastName": "Test"}
data = {"site": "shop-ru", "order": json.dumps(json_params)}
new_order = api.orders.create(params=data) # creating new order


# update order ot another object
import json
json_params = {"firstName": "UpdatedName", "lastName": "UpdatedLastName"}
data = {"site": "shop-ru", "order": json.dumps(json_params)}
update_order = api.orders.edit(object_id="<id>", params=data)

```

# TODO
* full documentation(all retail methods)
* examples
* async version
* tests