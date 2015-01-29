#!/bin/sh

# URL for the 2816x2112 pixel original Dock_Vancouver.JPG
FILE_URL="https://upload.wikimedia.org/wikipedia/commons/f/fe/Dock_Vancouver.JPG"
BASENAME="photo"

wget -nc -q -O ${BASENAME}-orig.jpeg ${FILE_URL}
convert -resize 50% ${BASENAME}-orig.jpeg ${BASENAME}.png

for Q in 10 30 50 70 90; do
  gm convert -quality ${Q} ${BASENAME}.png ${BASENAME}-q${Q}.jpeg
  gm convert -crop 180x40+500+685 ${BASENAME}-q${Q}.jpeg ${BASENAME}-q${Q}-crop.png
done

python jpeg_svg.py
