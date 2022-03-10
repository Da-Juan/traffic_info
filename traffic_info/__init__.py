"""traffic_info module."""
import datetime
import logging
import os
import sys

import configargparse

from selenium.common.exceptions import WebDriverException

from workalendar.registry import registry

from .__version__ import __version__
from .core import Location, MapScreenshot, SMTPServer, send_email
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


def parse_args() -> configargparse.Namespace:
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
        "-s",
        "--smtp_server",
        type=str,
        default="localhost",
        help="SMTP server’s address.",
    )
    parser.add_argument(
        "-p", "--smtp_port", type=int, default=25, help="SMTP server’s port."
    )
    parser.add_argument("-S", "--smtp_use_ssl", action="store_true", help="Use SMTPS.")
    parser.add_argument("-u", "--smtp_login", type=str, help="SMTP server’s login.")
    parser.add_argument(
        "-w", "--smtp_password", type=str, help="SMTP server’s password."
    )
    parser.add_argument(
        "-W", "--screenshot_width", type=int, help="Screenshot’s width."
    )
    parser.add_argument(
        "-H", "--screenshot_height", type=int, help="Screenshot’s height."
    )
    parser.add_argument(
        "-C",
        "--country_code",
        type=str,
        help="Country code(ISO 3166-1/ISO 3166-2) to avoid notifications on holidays.",
    )

    return parser.parse_args()


def run() -> None:
    """Run traffic info from command line."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    options = parse_args()
    if options.country_code:
        calendar_class = registry.get(options.country_code.upper())
        if not calendar_class:
            logger.error("Invalid country code")
            sys.exit(1)
        calendar = calendar_class()
        if calendar.is_holiday(datetime.datetime.now()):
            # Enjoy your holiday! :)
            sys.exit()

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
    smtp_server = SMTPServer(
        options.smtp_server,
        options.smtp_port,
        options.smtp_use_ssl,
        options.smtp_login,
        options.smtp_password,
    )
    send_email(
        options.email_from,
        options.email_to,
        location,
        screenshot,
        smtp_server,
    )


__all__ = ["__version__", "Location", "MapScreenshot", "run", "send_email"]
