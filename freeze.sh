pyinstaller --onefile \
  --windowed \
  --hidden-import configparser \
  --add-data './view/dist:./view/dist' \
  main.py
#  --icon icon.ico \
#  --add-data './config.template.yml:./config.yml' \
