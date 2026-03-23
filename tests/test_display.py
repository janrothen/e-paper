import sys
import types
import unittest
from unittest.mock import MagicMock


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


if __name__ == "__main__":
    unittest.main()
