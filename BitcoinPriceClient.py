import logging

import json

from utils.Request import Request
from utils.config import config

SERVICE_ENDPOINT = config().get('bitcoin.price', 'service_endpoint')

class BitcoinPriceClient(object):
    
    def retrieve_data(self):
        try:
            request = Request()
            result = request.get(SERVICE_ENDPOINT)
            if result:
                return json.loads(result)
        except ConnectionError as e:
            msg = str(e)
            logging.error(msg)
