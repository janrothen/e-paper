import sys
import types
import unittest
from unittest.mock import MagicMock, patch


def _make_mock_epd2in13_module():
    """Return a fake epd2in13_V2 module so the ARM .so is never loaded."""
    mod = types.ModuleType("epaper.lib.epd2in13_V2")
    mock_epd_instance = MagicMock()
    mock_epd_instance.FULL_UPDATE = "FULL_UPDATE"
    mock_epd_instance.height = 250
    mock_epd_instance.width = 122
    mod.EPD = MagicMock(return_value=mock_epd_instance)
    return mod, mock_epd_instance


class TestPriceTickerStop(unittest.TestCase):
    def setUp(self):
        # Stub out the driver modules before display.py is imported
        fake_mod, self.mock_epd = _make_mock_epd2in13_module()
        sys.modules.setdefault("epaper.lib.epdconfig", MagicMock())
        sys.modules["epaper.lib.epd2in13_V2"] = fake_mod

        # Remove cached display module so our stubs take effect
        sys.modules.pop("epaper.display", None)

        from epaper.display import PriceTicker
        self.ticker = PriceTicker(price_client=MagicMock(), price_extractor=MagicMock())

    def test_stop_only_shuts_down_hardware_once(self):
        self.ticker.stop()
        self.ticker.stop()  # second call must be a no-op

        self.assertEqual(self.mock_epd.sleep.call_count, 1)

    def test_stop_sets_running_false(self):
        self.assertTrue(self.ticker._running)
        self.ticker.stop()
        self.assertFalse(self.ticker._running)


class TestPriceTickerRefreshTiming(unittest.TestCase):
    def setUp(self):
        fake_mod, self.mock_epd = _make_mock_epd2in13_module()
        sys.modules.setdefault("epaper.lib.epdconfig", MagicMock())
        sys.modules["epaper.lib.epd2in13_V2"] = fake_mod
        sys.modules.pop("epaper.display", None)

        from epaper.display import PriceTicker, PRICE_REFRESH_INTERVAL
        self.PriceTicker = PriceTicker
        self.PRICE_REFRESH_INTERVAL = PRICE_REFRESH_INTERVAL

    def _run_one_iteration(self, monotonic_values, ticker):
        """Pump _display_price for one iteration then stop the ticker."""
        iter_values = iter(monotonic_values)
        with patch("epaper.display.time.monotonic", side_effect=iter_values), \
             patch("epaper.display.time.sleep", side_effect=lambda _: ticker.stop()), \
             patch("epaper.display.ImageFont.truetype", return_value=MagicMock()), \
             patch("epaper.display.Image.new", return_value=MagicMock()), \
             patch("epaper.display.ImageDraw.Draw", return_value=MagicMock()):
            ticker._display_price()

    def test_first_iteration_always_refreshes(self):
        """last_refresh starts at 0.0 so the first check always triggers."""
        ticker = self.PriceTicker(price_client=MagicMock(), price_extractor=MagicMock())
        # monotonic() returns a large value — well past the interval from 0.0
        self._run_one_iteration([9999.0, 9999.0], ticker)
        self.mock_epd.display.assert_called_once()

    def test_no_refresh_within_interval(self):
        """If less than PRICE_REFRESH_INTERVAL seconds have passed, skip the refresh."""
        ticker = self.PriceTicker(price_client=MagicMock(), price_extractor=MagicMock())
        # First iteration refreshes and records last_refresh = t1
        # Second iteration checks at t1 + (interval - 1): should NOT refresh again
        t1 = 9999.0
        t2 = t1 + self.PRICE_REFRESH_INTERVAL - 1

        call_count = 0

        def stop_on_second_sleep(_):
            nonlocal call_count
            call_count += 1
            if call_count >= 2:
                ticker.stop()

        with patch("epaper.display.time.monotonic", side_effect=[t1, t1, t2]), \
             patch("epaper.display.time.sleep", side_effect=stop_on_second_sleep), \
             patch("epaper.display.ImageFont.truetype", return_value=MagicMock()), \
             patch("epaper.display.Image.new", return_value=MagicMock()), \
             patch("epaper.display.ImageDraw.Draw", return_value=MagicMock()):
            ticker._display_price()

        # display should have been called exactly once (the first refresh)
        self.assertEqual(self.mock_epd.display.call_count, 1)


if __name__ == "__main__":
    unittest.main()
