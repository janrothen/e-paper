import json

class BitcoinPriceClientMock(object):
    
    def retrieve_data(self):
        with open('mock_data.json') as json_file:
            return json.load(json_file)