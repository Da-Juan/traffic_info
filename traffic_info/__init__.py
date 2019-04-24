"""traffic_info module."""
import logging
import os
import sys

import configargparse

from selenium.common.exceptions import WebDriverException

from .__version__ import __version__
from .core import Location, MapScreenshot, send_email
from .exceptions import NotExecutableError, WebdriverNotFoundError
from .utils import get_chromedriver_path


def check_webdriver_path(webdriver: str = None) -> str:
    """
    Check if the webdriver exist and is executable.

    Args:
        webdriver: The webdriver's path.

    Returns:
        The verified path.

    """
    if webdriver is None:
        webdriver = get_chromedriver_path()
        if webdriver is None:
            raise WebdriverNotFoundError(webdriver)
    if not os.path.isfile(webdriver):
        raise WebdriverNotFoundError(webdriver)
    if not os.access(webdriver, os.X_OK):
        raise NotExecutableError(webdriver)
    return webdriver


def parse_args() -> None:
    """Parse command-line arguments."""
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

    return parser.parse_args()


def run() -> None:
    """Run traffic info from command line."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    options = parse_args()

    location_keys = ["latitude", "longitude", "zoom"]
    screenshot_keys = ["api_key", "webdriver_path", "width", "height"]

    location_params = {
        k: v for k, v in vars(options).items() if v is not None and k in location_keys
    }
    screenshot_params = {
        k: v for k, v in vars(options).items() if v is not None and k in screenshot_keys
    }
    try:
        screenshot_params["webdriver_path"] = check_webdriver_path(
            options.webdriver_path
        )
    except (NotExecutableError, WebdriverNotFoundError) as exc:
        logger.error(exc.msg)
        sys.exit(1)

    location = Location(**location_params)
    screenshot = MapScreenshot(**screenshot_params)
    try:
        screenshot.take(location)
    except WebDriverException as exc:
        logger.error(exc.msg)
        sys.exit(1)
    send_email(options.email_from, options.email_to, location, screenshot)


__all__ = ["__version__", "Location", "MapScreenshot", "run", "send_email"]
