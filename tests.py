#!/usr/bin/env python3

from BitcoinPriceClientMock import BitcoinPriceClientMock as BitcoinPriceClient
from PriceExtractor import PriceExtractor

def test_price_extractor_USD(data):
    extractor = PriceExtractor('USD', '$')
    actual = extractor.formatted_price_from_data(data)
    expected = '$35.3k'
    assert_equals(expected, actual)

def test_price_extractor_CHF(data):
    extractor = PriceExtractor('CHF', 'CHF')
    actual = extractor.formatted_price_from_data(data)
    expected = 'CHF32.5k'
    assert_equals(expected, actual)

def assert_equals(expected, actual):
    if expected != actual:
        raise Exception('assertion failed', expected, actual)

def run_tests():
    client = BitcoinPriceClient()
    data = client.retrieve_data()

    test_price_extractor_USD(data)
    test_price_extractor_CHF(data)

    print('complete')

if __name__ == '__main__':
    run_tests()