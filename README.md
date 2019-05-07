# Traffic Info

Tired of being "suprised" by traffic when you leave your workplace?

This little tool sends you an email containing a map of the area of your choice with traffic informations.

![Traffic info screenshot](https://github.com/Da-Juan/traffic_info/blob/master/docs/_static/images/email_screenshot.png)

Written in Python 3.6 it relies on the following:
* [ChromeDriver](http://chromedriver.chromium.org/)
* [ConfigArgParse](https://github.com/bw2/ConfigArgParse)
* [Jinja2](http://jinja.pocoo.org/) template engine
* [Selenium](https://github.com/SeleniumHQ/Selenium) WebDriver
* [Google Maps](https://maps.google.com)

This project's source code is available on [Github](https://github.com/Da-Juan/traffic_info).

## User's Guide

### Requirements

ChromeDriver is used to take the screenshot so you need to install [Chromium](https://www.chromium.org/) or [Google Chrome](https://www.google.com/chrome/).
Then, to install ChromeDriver you can use the provided script `bin/install_chromedriver.sh`.

Next you'll need a SMTP server configured on the machine to send the email notifications.

Optionally, you'll need a Google Maps Javascript API key if you have an intensive use of traffic-info.
Refer to [Google Maps Platform documentation](https://developers.google.com/maps/documentation/javascript/get-api-key).

### Install

#### Install from source

Create a Python3 virtualenv then run `setup.py`:

```text
python3 -m virtualenv -p python3 venv
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
usage: traffic-info [-h] [-c CONFIG_FILE] [-d WEBDRIVER_PATH] [-k API_KEY] -l
                    LATITUDE -L LONGITUDE [-z ZOOM] -f EMAIL_FROM -t EMAIL_TO
                    [-W SCREENSHOT_WIDTH] [-H SCREENSHOT_HEIGHT]

Args that start with '--' (eg. -d) can also be set in a config file (specified
via -c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for
details, see syntax at https://goo.gl/R74nmi). If an arg is specified in more
than one place, then commandline values override config file values which
override defaults.

optional arguments:
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
  -W SCREENSHOT_WIDTH, --screenshot_width SCREENSHOT_WIDTH
                        Screenshot’s width.
  -H SCREENSHOT_HEIGHT, --screenshot_height SCREENSHOT_HEIGHT
                        Screenshot’s height.
```
