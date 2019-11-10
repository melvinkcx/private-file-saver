echo "Don't forget to install dependencies into System (not virtualenv, etc)" && \
rm -r dist build main.spec && \
pyinstaller --onefile \
  --noconsole \
  --hidden-import configparser \
  --add-data './view/dist:./view/dist' \
  --icon ./icon.ico \
  --log-level DEBUG \
  main.py && \
mv ./dist/main.app/Contents/MacOS/main ./dist/main.app/Contents/MacOS/pfs && \
echo 'APPL????' > ./dist/main.app/Contents/PkgInfo && \
echo '#!/bin/bash
DIR=$(cd "$(dirname "$0")"; pwd)
open $DIR/pfs' > ./dist/main.app/Contents/MacOS/main && \
chmod +x ./dist/main.app/Contents/MacOS/main
