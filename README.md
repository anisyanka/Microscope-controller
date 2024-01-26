# Modbus TCP/RTU Converter

## Quick start
**1.** По дефолту плата RPI при загрузке пытается подключиться к следующей wi-fi сети:
```
SSID: anisyanka
PASS: CAh)z3iH
```
Чтобы настроить свою сеть и подключить RPI к wi-fi необходимо времено поднять точку доступа с вышеуказанными параметрами,
дождаться пока плата подключиться к ней и узнать IP-адрес (например, на роутере).
Затем залогиниться по SSH на плату и ввести следующие команды:
```
nmcli device wifi connect YOUR-SSID password "YOUR-PASSWORD"
nmcli device set wlan0 autoconnect yes
sudo reboot
```
После этого RPI всегда будет подключаться к вашей сети автоматически.

**2.** Как только плата стала "онлайн", на ней автоматически запускается systemd-сервис, реализующий основную логику преобразования протоколов Modbus.
Сервис называется `modbus_converter`.
Все полезные скрипты, исполняемый файл сервиса и конфиги лежат в каталоге `/home/pi/.modbus_converter` (обратите внимание, что в названии есть точка).

Главный конфигурационный файл, который должен редактировать пользователь  - это `/home/pi/.modbus_converter/modbus_converter.conf`
Дефолтный конфиг выглядит так:
```
{
    "uart_device": "/dev/ttyAMA5",
    "uart_baud": 9600,
    "uart_parity": N, <--- N=none, E=even, O=odd
    "uart_data_bit": 8,
    "uart_stop_bit": 1,

    "modbus_port": 1502,
    "modbus_number_of_tcp_connections": 1,
    "modbus_connected_microcontroller_slave_addr": 1,
    "modbus_camera_slave_addr": 2,
    "modbus_loss_connection_timeout_ms": 1000
}

```
`modbus_port` - порт, на котором modbus_converter сервис откроет TCP соединение. Этот порт нужно использовать в программе Modbus Poll или в любой другой программе, которая будет присоединяться к сервису.

`modbus_number_of_tcp_connections` - количество возможных TCP соединений. Это для будущего использования. На данный момент поддерживается только одно соединение. Если изменить этот параметр, то сервис выдаст в лог информацию о том, что это пока не поддерживается и всё равно будет создавать только одно соединение.

`modbus_connected_microcontroller_slave_addr` - slave-адресс нижестоящего микроконтроллера. Впринципе можно установить какой
угодно, так как любые присланные данные будут переданы уст-ву  `uart_device`, но важно, чтобы это значение не совпадало
c slave-адресом камеры.

`modbus_camera_slave_addr` - slave-адрес, на который будет реагировать камера.

`modbus_loss_connection_timeout_ms` - время (в мили-секундах) ожидания ответа от нижестоящего микроконтроллера. Если в течении
этого промежутка времени нет ответа от уст-ва  `uart_device`,  то сервис просто начинает заново ожидать указаний по TCP. Если при этом использовался Modbus Poll, то он покажет ошибку Timeout.

**Если какой-то либо из параметров был изменён, то необходимо перезапустить сервис, чтобы настройки вступили в силу.** См.ниже.

**3.** Какмера будет реагировать на тот адрес slave-устройства, что указали в конфиг-файле.
Команды для всех остальных адресов будут пересылаться нижестоящему микроконтроллеру.
На данный момент камера поддерживает только одну команду (один Modbus function code) - `MODBUS_FC_WRITE_SINGLE_REGISTER=0x06`
Это команда на запись аналогового вывода.
Была выбрана именно эта камонда, так как в будущем можно сделать, чтобы 16-битные регистры Modbus отвечали за настройки камеры.
Например, настройка зума, баланса белого и тд.

На данный момент поддерживается только один регистр у этой команды - `CAMERA_API_LAUNCH_VIDEO_REG_ADDR=0x01`
Этот регистр отвечает за состояние видеопотока.
Значения этого регистра могут быть следующие:
```
#define CAMERA_API_LAUNCH_VIDEO_4K_VALUE    0x00
#define CAMERA_API_LAUNCH_VIDEO_1080P_VALUE 0x01
#define CAMERA_API_LAUNCH_VIDEO_STOP        0x02
```

Примеры Modbus команд для камеры:
```
0x02 0x06 0x00 0x01 0x00 0x00 <crc16> - запустить 4к видео стрим.
0x02 0x06 0x00 0x01 0x00 0x01 <crc16> - запустить 1080p видео стрим.
0x02 0x06 0x00 0x01 0x00 0x02 <crc16> - запустить 1080p видео стрим.
```

Если камера получила неподдерживаемые значения fucntion code, регистра или значений регистров, то конвертер вернёт соответствующие ошибки
вышестоящей программе, приславшей неверную команду.


## Полезные команды сервиса `modbus_converter`
```
- Манипуляции с запуском сервиса
service modbus_converter status
service modbus_converter start
service modbus_converter stop
service modbus_converter restart

- Тоже самое, но через systemctl
sudo systemctl status modbus_converter
sudo systemctl start modbus_converter
sudo systemctl stop modbus_converter
sudo systemctl restart modbus_converter

- Просмотр логов сервиса в режиме tail -f, показав последние 50 строк лога
sudo journalctl -a -f -n 50 -u modbus_converter # 

- Просмотр логов сервиса с момента последней загрузки системы
sudo journalctl -b -u modbus_converter
```

## Какие пины UART доступны для использования на RPI4:
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

* /dev/ttyAMA5 - UART5. <--- дефолт
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
$ pinctrl
```
либо
```
$ raspi-gpio get
```
Обе команды выводят информацию о текущих настройках пина. В этом случае в выводе каоманд GPIO-N - это номер gpio на процессоре. **НЕ** на 40-ко пиновой гребёнке.
