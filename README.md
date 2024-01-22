# Modbus TCP/RTU Converter

## Пины UART на RPI4:
https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3-pizerow-pi4-or-later-models/107780#107780

В образе включены 3 разных uart, которые можно использовать для подключения к ним uart от нижестоящего микроконтроллера.
Здесь пины - это номер пина на 40-ко пиновой гребёнке.
```
* /dev/ttyAMA3 - UART3.
  PIN7 - TX
  PIN29 - RX

* /dev/ttyAMA4 - UART4.
  PIN24 - TX
  PIN21 - RX

* /dev/ttyAMA5 - UART5.
  PIN32 - TX
  PIN33 - RX
```
Для этого в device tree были добавлены overlays. Они включены с помощью записи следующих строк в файл `/boot/config.txt`
```
enable_uart=1
dtoverlay=uart3
dtoverlay=uart4
dtoverlay=uart5
```
PS: Они загружаются во время boot-time, поэтому команда `dtoverlay -l` не покажет их.

Также в образе включен bootlog uart. Можно подсоединить к гребенке на PIN8(tx0) и на PIN10(rx0)
uart-usb преобразватель и пользоваться этой консолью без подключения платы к wifi и без управления через SSH.

Посмотреть текущую конфигурацию пинов можно с помощью следующих команд:
```
* pinctrl

* raspi-gpio get
```
Обе команды выводят информацию о текущих настройках пина. В этом случае GPIO<N> - это номер gpio на процессоре. **Не** на 40-ко пиновой гребёнке.
q
## Systemd-сервис
Программа 'modbus_converter' запускается автоматически как только произошло подключение к сети.
Работает как systemd-сервис.

Команды, чтобы посмотреть статус сервиса:
```
1. Манипуляции с запуском сервиса
service modbus_converter status
service modbus_converter start
service modbus_converter stop
service modbus_converter restart

2. Тоже самое, но через systemctl
sudo systemctl status modbus_converter
sudo systemctl start modbus_converter
sudo systemctl stop modbus_converter
sudo systemctl restart modbus_converter

3. Просмотр логов сервиса
sudo journalctl -a -f -n 50 -u modbus_converter # в режиме tail -f, показав последние 50 строк лога
sudo journalctl -b -u modbus_converter # с момента последней загрузки системы
```


## Конфигурация программы modbus_converter