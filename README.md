# Traffic Info

Tired of being "suprised" by traffic when you leave your workplace?

This little tool sends you an email containing a map of the area of your choice with traffic informations.

![Traffic info screenshot](https://github.com/Da-Juan/traffic_info/blob/master/docs/_static/images/email_screenshot.png)

Written in Python 3.6 it relies on the following:
* [ChromeDriver](http://chromedriver.chromium.org/)
* [ConfigArgParse](https://github.com/bw2/ConfigArgParse)
* [Jinja2](http://jinja.pocoo.org/) template engine
* [Selenium](https://github.com/SeleniumHQ/Selenium) WebDriver
* [Workalendar](https://pypi.org/project/workalendar/)
* [Google Maps](https://maps.google.com)

This project's source code is available on [Github](https://github.com/Da-Juan/traffic_info).

## User's Guide

### Requirements

ChromeDriver is used to take the screenshot so you need to install [Chromium](https://www.chromium.org/) or [Google Chrome](https://www.google.com/chrome/).
Then, to install ChromeDriver you can use the provided script `bin/install_chromedriver.sh`.

Next you'll need a SMTP server to send the email notifications.

Optionally, you'll need a Google Maps Javascript API key if you have an intensive use of traffic-info.
Refer to [Google Maps Platform documentation](https://developers.google.com/maps/documentation/javascript/get-api-key).

### Install

#### Install from source

Create a Python3 virtualenv then run `setup.py`:

```text
python3 -m venv venv
source venv/bin/activate
python3 setup.py install
```

### Usage

You can run the script from the command line or in a cron to get the traffic infos each day just before leaving your work place.

#### Basic usage

Four parameters are required to run the script:
* the latitude of the center point of the map
* the longitude of the center point of the map
* the email sender’s address
* and the email recipient’s address.

```text
traffic-info -l 43.6037834 -L 1.4402123 -f traffic-info@example.com -t user@example.com
```

#### Command line reference

```text
usage: traffic-info [-h] [-c CONFIG_FILE] [-d WEBDRIVER_PATH] [-k API_KEY] -l LATITUDE -L LONGITUDE [-z ZOOM] -f
                    EMAIL_FROM -t EMAIL_TO [-s SMTP_SERVER] [-p SMTP_PORT] [-S] [-u SMTP_LOGIN] [-w SMTP_PASSWORD]
                    [-W SCREENSHOT_WIDTH] [-H SCREENSHOT_HEIGHT] [-C COUNTRY_CODE]

options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Config file path.
  -d WEBDRIVER_PATH, --webdriver_path WEBDRIVER_PATH
                        ChromeDriver's path.
  -k API_KEY, --api_key API_KEY
                        Google Maps Javascript API key.
  -l LATITUDE, --latitude LATITUDE
                        Latitude of the center point of the map.
  -L LONGITUDE, --longitude LONGITUDE
                        Longitude of the center point of the map.
  -z ZOOM, --zoom ZOOM  Google Maps zoom level.
  -f EMAIL_FROM, --email_from EMAIL_FROM
                        Email sender’s address.
  -t EMAIL_TO, --email_to EMAIL_TO
                        Email recipient’s address.
  -s SMTP_SERVER, --smtp_server SMTP_SERVER
                        SMTP server’s address.
  -p SMTP_PORT, --smtp_port SMTP_PORT
                        SMTP server’s port.
  -S, --smtp_use_ssl    Use SMTPS.
  -u SMTP_LOGIN, --smtp_login SMTP_LOGIN
                        SMTP server’s login.
  -w SMTP_PASSWORD, --smtp_password SMTP_PASSWORD
                        SMTP server’s password.
  -W SCREENSHOT_WIDTH, --screenshot_width SCREENSHOT_WIDTH
                        Screenshot’s width.
  -H SCREENSHOT_HEIGHT, --screenshot_height SCREENSHOT_HEIGHT
                        Screenshot’s height.
  -C COUNTRY_CODE, --country_code COUNTRY_CODE
                        Country code(ISO 3166-1/ISO 3166-2) to avoid notifications on holidays.
```

#### Systemd units

The `systemd` directory provides units examples if you want to run this tool on a schedule.
