"""Trafficinfo module."""
import logging
import os.path
import shutil
import smtplib
import tempfile
import time
from email.message import EmailMessage
from email.utils import make_msgid
from typing import Any, Dict, Optional

from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.options import Options

from .utils import render_template

DIR = os.path.dirname(os.path.abspath(__file__))
CHROMEDRIVER_PATH = "%s/bin/chromedriver" % DIR

Context = Dict[str, Any]


class Location:  # pylint: disable-msg=R0903
    """
    Location class.

    Args:
        latitude: Latitude of the center point of the map to make the screenshot.
        longitude: Longitude of the center point of the map.
        zoom: Google Maps zoom level, default 16.

    """

    def __init__(self, latitude: float, longitude: float, zoom: int = 16) -> None:
        """Initialize a Location object with the given options."""
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom


class MapScreenshot:
    """
    MapScreenshot class.

    Args:
        webdriver_path: The path to the webdriver to use.
        api_key: Google Maps Javascript API key to take screenshots.
        width: Screenshot's width, default 1280.
        height: Screenshot's height, default 720.
        output_dir: The path to save the screenshot,
        if not specified a temporary directory will be created.

    """

    _template_dir = os.path.join(DIR, "templates")

    def __init__(
        self,
        webdriver_path: str,
        api_key: Optional[str] = None,
        width: int = 1280,
        height: int = 720,
        output_dir: Optional[str] = None,
    ) -> None:
        """Initialize a MapScreenshot object with the given options."""
        self._tmpdir = tempfile.mkdtemp()
        self.webdriver_path = webdriver_path
        self.api_key = api_key
        self.width = width
        self.height = height
        self.output_dir = output_dir if output_dir is not None else self._tmpdir
        self.path = os.path.join(self.output_dir, "map.png")

    def take(self, location: Location) -> str:
        """
        Take a screenshot using chrome webdriver.

        Args:
            location: The location of the map's center point.

        Returns:
            The screenshot's full path.

        """
        context: Context = {
            "key": self.api_key,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "zoom": location.zoom,
        }
        map_html = os.path.join(self._tmpdir, "map.html")
        render_template(os.path.join(self._template_dir, "map.j2"), context, map_html)

        options = Options()  # type: ignore
        options.set_headless(headless=True)
        driver = webdriver.Chrome(
            executable_path=self.webdriver_path, chrome_options=options
        )
        driver.set_window_size(self.width, self.height)
        driver.get("file://%s" % map_html)
        time.sleep(5)
        driver.save_screenshot(self.path)
        driver.quit()
        return self.path

    def __del__(self) -> None:
        """Cleanup temporary files."""
        if os.path.isdir(self._tmpdir):
            shutil.rmtree(self._tmpdir)


def send_email(
    email_from: str,
    email_to: str,
    location: Location,
    screenshot: MapScreenshot,
    template: Optional[str] = None,
) -> None:
    """
    Send the traffic info email.

    Args:
        email_from: Email sender's address.
        email_to: Email recipient's address.
        location: The map's location.
        screenshot: The map's screenshot.
        template: The path to the email's Jinja2 template,
        templates/email.j2 if not specified.

    """
    if template is None:
        template = os.path.join(DIR, "templates", "email.j2")
    logger = logging.getLogger(__name__)
    map_cid = make_msgid()
    context: Context = {
        "url": f"https://www.google.fr/maps/@{location.latitude},"
        f"{location.longitude},{location.zoom}z/data=!5m1!1e1",
        "width": screenshot.width,
        "height": screenshot.height,
        "map_cid": map_cid[1:-1],
    }
    content = f"""
    Today's traffic conditions.
    {context["url"]}
    Have a safe trip back home!
    """
    html = render_template(template, context)
    email = EmailMessage()
    email["Subject"] = "Traffic info"
    email["From"] = f"Traffic info <{email_from}>"
    email["To"] = email_to
    email.set_content(content)
    email.add_alternative(html, subtype="html")
    with open(screenshot.path, "rb") as img:
        # type: ignore
        email.get_payload()[1].add_related(img.read(), "image", "png", cid=map_cid)

    try:
        with smtplib.SMTP("localhost") as smtp:
            smtp.send_message(email)
    except ConnectionRefusedError as exception:
        logger.error("Unable to send email(%s)", exception)
