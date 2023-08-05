# python-rest-client

# Get started

1. Create an account on https://testnet.delta.exchange/signup

2. Install the package:

```
pip install delta-rest-client
```

3. Follow the below snippet to trade on testnet:

```python
from delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size

delta_client = DeltaRestClient(
  base_url='https://testnet-api.delta.exchange',
  username='',
  password=''
)
product_id = 2
product = delta_client.get_product(product_id)
settling_asset = product['settling_asset']

order = create_order_format(7078.5, 10, "buy", product_id)
delta_client.create_order(order) # will create order on testnet

order1 = create_order_format(7078.5, 10, "buy", product_id)
order2 = create_order_format(7078.5, 10, "sell", product_id)
orders = [order1, order2]
delta_client.batch_create(product_id, orders)
delta_client.get_orders()
delta_client.get_L2_orders(product_id)
delta_client.get_ticker(product_id)
delta_client.get_wallet(settling_asset)
```

4. Verify your orders on https://testnet.delta.exchange

Same steps can used for production trading.

5. Production url is https://trade.delta.exchange/
6. Production base_url is https://api.delta.exchange
