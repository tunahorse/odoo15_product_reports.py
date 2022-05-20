# odoo15_product_reports.py
Get a simple report of all your product data by location. 


# Odoo ERP Reporting  

Odoo is a great piece of open source ERP software. When you see just how much it can do, it really is an amazing tool. 

However its reporting features, are often not ideal out of the box. And while you could spend hours building a custom Odoo report, (that you will need to change in a few months) I have found it much easier to create my own with python!

I will building a python3 script to generate reports for all products at all locations. 

I will cover the following. You can find a repo with my code at the end. 

###### How to set up for local Odoo data scraping
###### How to scrape products and locations
###### How to spin up excel reports on demand


# Getting set up


You will need all the usual's for logging into Odoo, as well as some extra if you are hosting locally. We will also be using pandas.


```
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

```


# Getting our product and location data. 

Now we are ready to start data scraping! In this case I will be keeping it simple, I just want all my products, no extra filtering. You could add extra's here ex. I want all products, that are varation or created by a user. 

Once I have all my product ID's, now I want to search ALL of my locations that actaully have product so in this case I want 
```
 ['on_hand', '=', True]]])
```

Get your data

```
all_products = models.execute_kw(db, uid, password, 'product.product', 'search',
                                 [[['type', '=', 'product']]])


on_hand_data = models.execute_kw(db, uid, password,
                                 'stock.quant', 'search_read',
                                 [[['product_id', '=', all_products], ['on_hand', '=', True]]])


```


# Putting it all together

Now we are ready to start data scraping! In this case I will be keeping it simple, I just want all my products, no extra filtering. You could add extra's here ex. I want all products, that are varation or created by a user. 

Okay you have your data ready to go! Now what? 

Now we run a for loop for everything on hand for each product. Hint: I have found for most reports this is all it boils down to: Filtering for loops

We will use the search read method to get ALL of our data for each product. 
```
search_read
```

The we are going to build 3 list, and let pandas handle the data framing.  

```
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





```


That is it! Check out clean and simple report!

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/abpp4tny8xs0lj5yxabl.png)
 
 



