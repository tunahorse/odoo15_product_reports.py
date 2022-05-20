# !/usr/bin/env python3

import pandas as pd
import xmlrpc.client
import ssl

# Begin Login to Odoo#

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

url = "http://localhost:8069"
db = "test"
username = "test@gmail.com"
password = "test"

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# End login to odoo


# Begin get raw odoo data

all_products = models.execute_kw(db, uid, password, 'product.product', 'search',
                                 [[['type', '=', 'product']]])


on_hand_data = models.execute_kw(db, uid, password,
                                 'stock.quant', 'search_read',
                                 [[['product_id', '=', all_products], ['on_hand', '=', True]]])

#End get raw odoo data


# Begin Odoo data framing

product = []
locations = []
quantity = []

for i in on_hand_data:

    product.append(i['product_id'][1])
    quantity.append(i['quantity'])
    locations.append(i['location_id'][1])

df = pd.DataFrame()

df['Product'] = product
df['Locations'] = locations
df['quantity'] = quantity


 # Converting to excel
df.to_excel('data.xlsx', index=False)

# End Odoo data framing

