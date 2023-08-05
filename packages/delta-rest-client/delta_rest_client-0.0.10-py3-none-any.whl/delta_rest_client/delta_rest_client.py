import requests
import time
import datetime
from decimal import Decimal
from .version import __version__ as version

agent = requests.Session()


class DeltaRestClient:

    def __init__(self, base_url, username=None, password=None, token=None):
        self.base_url = base_url
        if token:
            agent.headers.update(
                {'Authorization': 'Bearer %s' % token, 'User-Agent': 'delta-rest-client: %s' % version})
        else:
            self.username = username
            self.password = password
            self.authenticate()

    # Check if payload and query are working
    def request(self, method, path, payload=None, query=None):
        url = '%s/%s' % (self.base_url, path)

        def agent_request():
            return agent.request(
                method, url, json=payload, params=query, timeout=(3, 27)
            )

        res = agent_request()

        if res.status_code == 401:
            if self.username and self.password:
                self.authenticate()
                res = agent_request()

        res.raise_for_status()
        return res

    def authenticate(self):
        response = self.request(
            'POST', 'login', {'email': self.username, 'password': self.password})
        token = str(response.json()['token'])
        agent.headers.update(
            {'Authorization': 'Bearer %s' % token, 'User-Agent': 'rest-client'})

    def get_username(self):
        return self.username

    def get_product(self, product_id):
        response = self.request("GET", "products")
        response = response.json()
        products = list(
            filter(lambda x: x['id'] == product_id, response))
        return products[0] if len(products) > 0 else None

    def batch_create(self, product_id, orders):
        response = self.request(
            "POST",
            "orders/batch",
            {'product_id': product_id, 'orders': orders})
        return response

    def create_order(self, order):
        response = self.request('POST', "orders", order)
        return response.json()

    def batch_cancel(self, product_id, orders):
        response = self.request(
            "DELETE",
            "orders/batch",
            {'product_id': product_id, 'orders': orders})
        return response.json()

    def get_orders(self, query=None):
        response = self.request(
            "GET",
            "orders",
            query=query)
        return response.json()

    def get_L2_orders(self, product_id):
        response = self.request("GET", "orderbook/%s/l2" % product_id)
        return response.json()

    def get_ticker(self, product_id):
        l2_orderbook = self.get_L2_orders(product_id)
        best_sell_price = Decimal(l2_orderbook['sell_book'][0]['price']) if len(
            l2_orderbook['sell_book']) > 0 else Decimal('inf')
        best_buy_price = Decimal(l2_orderbook['buy_book'][0]['price']) if len(
            l2_orderbook['buy_book']) > 0 else 0
        return (best_buy_price, best_sell_price)

    def get_wallet(self, asset):
        response = self.request("GET", "wallet/balance", query = { 'asset_id' : asset['id'] })
        return response.json()

    def get_price_history(self, symbol, duration=5, resolution=1):
        if duration/resolution >= 500:
            raise Exception('Too many Data points')

        current_timestamp = time.mktime(datetime.datetime.today().timetuple())
        last_timestamp = current_timestamp - duration*60
        query = {
            'symbol': symbol,
            'from': last_timestamp,
            'to': current_timestamp,
            'resolution': resolution
        }

        response = self.request("GET", "chart/history", query=query)
        return response.json()

    def get_marked_price(self, product_id):
        response = self.request(
            "GET",
            "orderbook/%s/l2" % product_id)
        response = response.json()
        return float(response['mark_price'])

    def get_leverage(self):
        raise Exception('Method not implemented')

    def close_position(self, product_id):
        response = self.request(
            "GET",
            "positions")
        response = response.json()
        current_position = list(
            filter(lambda x: x['product']['id'] == product_id, response))

        if len(current_position) > 0:
            size = current_position[0]['size']
            if size > 0:
                order = {
                    'product_id': product_id,
                    'size': size,
                    'side': 'sell',
                    'order_type': 'market_order'
                }
            else:
                order = {
                    'product_id': product_id,
                    'size': abs(size),
                    'side': 'buy',
                    'order_type': 'market_order'
                }
            self.create_order(order=order)
        return

    def get_position(self, product_id):
        response = self.request(
            "GET",
            "positions")
        response = response.json()
        if response:
            current_position = list(
                filter(lambda x: x['product']['id'] == product_id, response))
            return current_position[0] if len(current_position) > 0 else None
        else:
            return None

    def set_leverage(self, product_id, leverage):
        response = self.request(
            "POST",
            "orders/leverage",
            {
                'product_id': product_id,
                'leverage':  leverage
            })
        return response.json()


def create_order_format(price, size, side, product_id, post_only=False):
    order = {
        'product_id': product_id,
        'limit_price': str(price),
        'size': size,
        'side': side,
        'order_type': 'limit_order',
        'post_only': post_only
    }

    return order


def cancel_order_format(x):
    order = {
        'id': x['id'],
        'product_id': x['product']['id']
    }
    return order


def round_by_tick_size(price, tick_size, floor_or_ceil=None):
    remainder = price % tick_size
    if remainder == 0:
        return price
    if floor_or_ceil == None:
        floor_or_ceil = 'ceil' if (remainder >= tick_size / 2) else 'floor'
    if floor_or_ceil == 'ceil':
        return price - remainder + tick_size
    else:
        return price - remainder
