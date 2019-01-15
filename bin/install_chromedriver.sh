#!/bin/bash

PREFIX="/usr/local/bin"

usage (){
	echo "$0 [-p PREFIX]"
	echo ""
	echo "optional arguments:"
	echo "  -p PREFIX, --prefix PREFIX"
	echo "                        The directory to install chromedriver."
	echo "                        ($PREFIX if unspecified)"
}

case "$(uname -s)" in
	"Linux")
		OS="linux"
		;;
	"Darwin")
		OS="mac"
		;;
	*)
		echo "Unsupported operating system."
		exit 1
		;;
esac

while (( "$#" )); do
	case "$1" in
		-h | --help)
			usage
			exit 0
			;;
		-p | --prefix)
			PREFIX=$2
			shift 2
			;;
		*)
			echo -e "Invalid argument: $1\n"
			usage
			exit 1
			;;
	esac
done

if [ ! -d "$PREFIX" ]; then
	echo "Invalid prefix: $PREFIX"
	exit 1
fi

LATEST_RELEASE_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
if command -v curl &> /dev/null; then
	LATEST_RELEASE="$(curl -s "$LATEST_RELEASE_URL")"
else
	LATEST_RELEASE="$(wget -q -O - "$LATEST_RELEASE_URL")"
fi
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/"$LATEST_RELEASE"/chromedriver_"$OS"64.zip
sudo unzip /tmp/chromedriver.zip -d "$PREFIX"
