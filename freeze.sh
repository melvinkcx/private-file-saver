cd view && \
yarn build && \
cd .. && \
rm -rf build dist main.spec && \
pyinstaller --onefile \
  --windowed \
  --hidden-import configparser \
  --add-data './view/dist:./view/dist' \
  --icon './icon.ico' \
  --clean \
  main.py
