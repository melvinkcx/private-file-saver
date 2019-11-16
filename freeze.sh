cd view && \
  yarn build && \
  cd .. && \
pyinstaller --onefile \
  --windowed \
  --hidden-import configparser \
  --add-data './view/dist:./view/dist' \
  --icon icon.ico \
  main.py
