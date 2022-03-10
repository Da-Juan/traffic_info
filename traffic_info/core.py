"""Trafficinfo module."""
import logging
import os.path
import shutil
import smtplib
import tempfile
import time
from dataclasses import dataclass
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from typing import Any, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .utils import render_template

DIR = os.path.dirname(os.path.abspath(__file__))
CHROMEDRIVER_PATH = f"{DIR}/bin/chromedriver"

Context = Dict[str, Any]


@dataclass
class Location:
    """
    Location class.

    Args:
        latitude: Latitude of the center point of the map to make the screenshot.
        longitude: Longitude of the center point of the map.
        zoom: Google Maps zoom level, default 16.

    """

    latitude: float
    longitude: float
    zoom: int


class SMTPServer:
    """SMTPServer class."""

    def __init__(
        self,
        server: str = "localhost",
        port: int = 25,
        use_ssl: bool = False,
        login: str = None,
        password: str = None,
    ) -> None:
        """Initialize a SMTPServer object with the given options."""
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.login = login
        self.password = password
        self._smtp = None

    def __del__(self) -> None:
        """Cleanup stmp object."""
        if self._smtp is not None:
            self._smtp.quit()

    def connect(self) -> None:
        """Start SMTP connection."""
        if self.use_ssl:
            self._smtp = smtplib.SMTP_SSL(self.server, self.port)
        else:
            self._smtp = smtplib.SMTP(self.server, self.port)
        if self.login is not None and self.password is not None:
            self._smtp.login(self.login, self.password)

    def send_message(self, email: EmailMessage) -> None:
        """Send email message."""
        self._smtp.send_message(email)


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

    _template_dir: str = os.path.join(DIR, "templates")

    def __init__(
        self,
        webdriver_path: str,
        api_key: str = None,
        width: int = 1280,
        height: int = 720,
        output_dir: str = None,
    ) -> None:
        """Initialize a MapScreenshot object with the given options."""
        self._tmpdir: str = tempfile.mkdtemp()
        self.webdriver_path: str = webdriver_path
        self.api_key: str = api_key
        self.width: int = width
        self.height: int = height
        self.output_dir = output_dir if output_dir is not None else self._tmpdir
        self.path: str = None

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

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(
            executable_path=self.webdriver_path, chrome_options=options
        )
        driver.set_window_size(self.width, self.height)
        driver.get(f"file://{map_html}")
        time.sleep(5)
        self.path = os.path.join(self.output_dir, "map.png")
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
    smtp_server: SMTPServer,
    template: str = None,
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
    email["From"] = Address("Traffic info", addr_spec=email_from)
    email["To"] = email_to
    email.set_content(content)
    email.add_alternative(html, subtype="html")
    with open(screenshot.path, "rb") as img:
        email.get_payload()[1].add_related(img.read(), "image", "png", cid=map_cid)

    try:
        smtp_server.connect()
    except (ConnectionRefusedError, smtplib.SMTPAuthenticationError) as exception:
        logger.error("Unable to connect to SMTP server(%s)", exception)

    try:
        smtp_server.send_message(email)
    except smtplib.SMTPException as exception:
        logger.error("Unable to send email(%s)", exception)
