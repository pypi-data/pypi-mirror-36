# CubePay API library for Python 
A third-party cryptocurrency payment gateway. 

Make it easy for receiving cryptocurrency!

More information at https://cubepay.io.


## API Document

https://document.cubepay.io

## Installation
Python bindings, you should run:

    pip install cubepay

or

    pip install --udgrade cubepay

## Usage
**Initialization**
```
from cubepay.client import CubePayClient

cubepay = CubePayClient(CLIENT_ID, CLIENT_SECRET, URL)
```

**Get available cryptocurrencies**

You can use these currencies at payment API for receive/send coin.

```
response = cubepay.get_coin()
```

**Get available fiat currenies.**

You can only use these fiat currencies for your product's original list price. We'll convert value by exchange rate between currency of list price and currency of actual paid.

```
response = cubepay.get_fiat()
```

**Do Payment**

Render a page with these payment information:
 - Your shop information
 - Item name
 - Payable coin list and corresponding price.
     
```
response = cubepay.do_payment(source_coin_id, source_amount, item_name, merchant_transaction_id, other, return_url, ipn_url, send_coin_id, send_amount, receive_address)
```

**Init payment With specific coin**

Initial payment with specific coin. The payment will expire after 6 hours.
     
```
response = cubepay.do_payment_by_coin_id(coin_id, source_coin_id, source_amount, item_name, merchant_transaction_id, other, return_url, ipn_url, send_coin_id, send_amount, receive_address) print(result)
```

**Query payment information**

Query payment information by specific identity
     
```
response = cubepay.query_payment(cubepay_transaction_id, merchant_transaction_id)
```
