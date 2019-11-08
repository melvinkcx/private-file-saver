pyinstaller --onefile \
  --windowed \
  --hidden-import configparser \
  --add-data './view/dist:./view/dist' \
  --add-data './config.template.yml:./config.yml' \
  --icon icon.ico \
  main.py
