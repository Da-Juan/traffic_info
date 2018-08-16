"""traffic_info module."""
import logging
import sys

import configargparse

from .core import Location, MapScreenshot, send_email
from .__version__ import __version__
from .utils import get_chromedriver_path


def run() -> None:
    """Run traffic info from command line."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    parser = configargparse.ArgParser()
    parser.add_argument(
        "-c", "--config-file", is_config_file=True, help="Config file path."
    )
    parser.add_argument("-d", "--webdriver_path", help="ChromeDriver's path.")
    parser.add_argument("-k", "--api_key", help="Google Maps Javascript API key.")
    parser.add_argument(
        "-l",
        "--latitude",
        required=True,
        type=float,
        help="Latitude of the center point of the map.",
    )
    parser.add_argument(
        "-L",
        "--longitude",
        required=True,
        type=float,
        help="Longitude of the center point of the map.",
    )
    parser.add_argument("-z", "--zoom", type=int, help="Google Maps zoom level.")
    parser.add_argument(
        "-f", "--email_from", required=True, help="Email sender’s address."
    )
    parser.add_argument(
        "-t", "--email_to", required=True, help="Email recipient’s address."
    )
    parser.add_argument(
        "-W", "--screenshot_width", type=int, help="Screenshot’s width."
    )
    parser.add_argument(
        "-H", "--screenshot_height", type=int, help="Screenshot’s height."
    )
    options = parser.parse_args()

    location_keys = ["latitude", "longitude", "zoom"]
    screenshot_keys = ["api_key", "webdriver_path", "width", "height"]

    location_params = {
        k: v for k, v in vars(options).items() if v is not None and k in location_keys
    }
    screenshot_params = {
        k: v for k, v in vars(options).items() if v is not None and k in screenshot_keys
    }
    if not options.webdriver_path:
        webdriver_path = get_chromedriver_path()
        if webdriver_path is None:
            logger.error(
                "Unable to find chrome driver, "
                "please provide ChromeDriver's path using --webdriver."
            )
            sys.exit(1)
        screenshot_params["webdriver_path"] = webdriver_path

    location = Location(**location_params)
    screenshot = MapScreenshot(**screenshot_params)
    screenshot.take(location)
    send_email(options.email_from, options.email_to, location, screenshot)


__all__ = ["__version__", "Location", "MapScreenshot", "run", "send_email"]
