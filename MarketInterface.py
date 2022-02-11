import logging
import requests

URL = "https://api.warframe.market/v1"


class MarketInterface:

    def __init__(self):
        pass

    def get_price(self, item):
        logging.debug("Getting the price of {item}".format(item=item))
        market = self.query_market(item)
        if market.status_code == 200:
            market = market.json()['payload']['orders']
            ingame_orders = self.get_ingame_orders(market)
            order_price_and_quantities = self.extract_plat_and_quantity_from_order(ingame_orders)
            avg_price = self.get_average_price(item, order_price_and_quantities)
            return avg_price

    def query_market(self, item):
        item = str.lower(item)
        item = str.replace(item, ' ', '_')
        get_text = '/items/{item}/orders'.format(item=item)
        full_url = URL + get_text
        headers = {'accept': 'application/json', 'Platform': 'pc'}
        logging.debug("Sending request to {url} along with {headers}".format(url=full_url, headers=headers))
        market = requests.get(url=full_url, headers=headers)
        logging.debug("Received {data}".format(data=market.status_code))
        return market

    def get_ingame_orders(self, market):
        ingame_orders = []
        for order in market:
            if order["user"]["status"] == "ingame" and order["order_type"] == "sell":
                ingame_orders.append(order)
        return ingame_orders

    def extract_plat_and_quantity_from_order(self, ingame_orders):
        order_price_and_quantities = []
        for order in ingame_orders:
            order_price_and_quantities.append((order['platinum'], order['quantity']))
        return order_price_and_quantities

    def get_average_price(self, item, order_price_and_quantities):
        sum_plat = 0
        sum_quantity = 0
        for pair in order_price_and_quantities:
            price, quantity = pair
            sum_plat += price * quantity
            sum_quantity += quantity
        average_price = sum_plat / sum_quantity
        logging.debug("{item}: Average Price: {price}".format(item=item, price=average_price))
        return average_price