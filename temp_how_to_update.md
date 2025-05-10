# Что сделать на RPI4 для обновления?

```
Данный документ описывает что нужно проделать один конкретный раз, чтобы обновить микроскоп.
Текущее обновление сложное и большое, поэтому как было ранее (просто одной командой ./update.sh)  не получится.

Но все последующие разы можно будет выполнять обновления старой командой. А сейчас нужно залогиниться по ssh
на микроскоп и выполнить следующие команды.
```

1.
```
cd ~/Microscope-controller
make uninstall

cd
rm -rf .venv
```

2.
```
cd ~/Microscope-controller
git pull origin master
```

3.
```
mkdir -p /home/pi/.microscope/
python3 -m venv /home/pi/.microscope/.venv
. /home/pi/.microscope/.venv/bin/activate
pip install -r /home/pi/Microscope-controller/web_server/requirements.txt
deactivate
```

4.
```
make
make install
```
