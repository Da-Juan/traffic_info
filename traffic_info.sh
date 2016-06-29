#!/bin/bash

# This program is free software: you can redistribute it and/or modify        
# it under the terms of the GNU General Public License as published by        
# the Free Software Foundation, either version 3 of the License, or           
# (at your option) any later version.                                         
#                                                                             
# This program is distributed in the hope that it will be useful,             
# but WITHOUT ANY WARRANTY; without even the implied warranty of              
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               
# GNU General Public License for more details.                                
#                                                                             
# You should have received a copy of the GNU General Public License           
# along with this program.  If not, see <http://www.gnu.org/licenses/>        

MAILTO=""
MAILFROM=""
LATITUDE=
LONGITUDE=
ZOOM=16

SCRIPT_DIR=$(dirname $0)
MAP_FILE="${SCRIPT_DIR}/map.html"
MAIL_CONTENT="${SCRIPT_DIR}/mail_content"
LOG_FILE="${SCRIPT_DIR}/webkit2png.log"

TEMP_DIR=$(mktemp -d)

#xvfb-run -a webkit2png --geometry=1280 720 --output=${TEMP_DIR}/map.png --wait=5 --feature=javascript --log=${LOG_FILE} file://${MAP_FILE}
sed -e "s|%%LAT%%|${LATITUDE}|" -e "s|%%LNG%%|${LONGITUDE}|" -e "s|%%ZOOM%%|${ZOOM}|" ${MAP_FILE} > ${TEMP_DIR}/map.html
xvfb-run -a webkit2png --geometry=1280 720 --output=${TEMP_DIR}/map.png --wait=5 --feature=javascript --log=${LOG_FILE} file://${TEMP_DIR}/map.html
#cp ${MAIL_CONTENT} ${TEMP_DIR}/mail
MAP_URL="https://www.google.fr/maps/@${LATITUDE},${LONGITUDE},${ZOOM}z/data=!5m1!1e1"
sed -e "s|%%MAP_URL%%|${MAP_URL}|" ${MAIL_CONTENT} > ${TEMP_DIR}/mail
uuencode -m ${TEMP_DIR}/map.png map.png >> ${TEMP_DIR}/mail
#cat ${TEMP_DIR}/mail | mailx -s "Traffic info" -a "Content-Type: multipart/related; boundary="boundary-example"; type="text/html"" -r ${MAILFROM} ${MAILTO}
cat ${TEMP_DIR}/mail | mailx -s "Traffic info" -a "Content-Type: multipart/related; boundary="traffic-info"; type="text/html"" -r ${MAILFROM} ${MAILTO}

rm -r ${TEMP_DIR}
