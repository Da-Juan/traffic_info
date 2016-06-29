# Traffic Info
This script sends an email containing a map of the area of your choice with traffic informations.

## Requirements
To generate the screenshot we need webkit2png: https://github.com/adamn/python-webkit2png

We also need some libraries and tools:

```
apt-get install bsd-mailx libqtwebkit4 python-qt4 sharutils xvfb
```

Finally we need a SMTP server configured on the machine.

## Usage
Edit **traffic_info.sh** and set the variables:
* `MAILTO`: the recipient email address
* `MAILFROM`: the sender email address
* `LATITUDE`: the latitude of the area you want infos
* `LONGITUDE`: the longitude of the area
* `ZOOM`: the zoom level

If you want to customize the email message, edit **mail_content**.

Finally run **traffic_info.sh** manually or run it from a cron.

## License
All code is licensed under the [GPL version 3](http://www.gnu.org/licenses/gpl.html)
