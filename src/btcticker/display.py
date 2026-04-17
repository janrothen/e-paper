import os
import sys
from pathlib import Path

from PIL import Image

_PKG_DIR = Path(__file__).parent
_LIB_DIR = _PKG_DIR / "lib"


def _load_epd_driver():
    """Import the Waveshare epd2in13_V2 driver.

    Prefers the `waveshare_epd` pip package when available. Falls back to
    the vendored copy under `lib/`, which requires two workarounds:

    1. The vendored `epd2in13_V2.py` imports `epdconfig` as a bare sibling,
       so `lib/` must be on sys.path for that import to resolve.
    2. On Linux 6.6+ (Debian Trixie) the BCM gpiomem driver was renamed
       from `gpiomem-bcm2835` to `rpi-gpiomem`. The vendored `epdconfig.py`
       uses the old name for platform detection and would otherwise fall
       through to a JetsonNano code path. We patch `os.path.exists` for
       the duration of the fallback import to redirect the stale lookup,
       and restore it immediately afterwards.
    """
    if _LIB_DIR.exists():
        sys.path.insert(0, str(_LIB_DIR))

    try:
        from waveshare_epd import epd2in13_V2

        return epd2in13_V2
    except ModuleNotFoundError:
        pass

    real_exists = os.path.exists

    def patched_exists(path: str) -> bool:
        if path == "/sys/bus/platform/drivers/gpiomem-bcm2835":
            return real_exists("/sys/bus/platform/drivers/rpi-gpiomem")
        return real_exists(path)

    os.path.exists = patched_exists
    try:
        from btcticker.lib import epd2in13_V2

        return epd2in13_V2
    finally:
        os.path.exists = real_exists


_epd_driver = _load_epd_driver()


class Display:
    """Hardware abstraction over the Waveshare epd2in13_V2 e-paper display.

    Handles initialisation, image rendering, and power management.
    The display is used in landscape orientation: physical width (250px)
    maps to EPD.height, physical height (122px) maps to EPD.width.
    """

    def __init__(self) -> None:
        self._epd = _epd_driver.EPD()
        self.width = self._epd.height  # 250 pixels
        self.height = self._epd.width  # 122 pixels

    def open(self) -> None:
        """Initialize the hardware and clear the screen to a known state."""
        self.init()
        self.clear()

    def init(self) -> None:
        self._epd.init(self._epd.FULL_UPDATE)

    def clear(self) -> None:
        self._epd.Clear(0xFF)

    def show(self, image: Image.Image) -> None:
        self._epd.display(self._epd.getbuffer(image))

    def sleep(self) -> None:
        self._epd.sleep()
