# Что сделать для обновления микроскопа?

```
Данный документ описывает что именно нужно проделать один раз, чтобы обновить микроскоп.
Текущее обновление сложное и большое, поэтому как было ранее (просто одной командой ./update.sh) не получится. Конкретно в этот раз нужно проделать описанные ниже шаги.

Но все последующие разы можно будет выполнять обновления старой командой. А сейчас нужно залогиниться по ssh
на микроскоп и выполнить следующие команды.
```

**BEWARE!!!**
```
Если вам важны ваши текущие значения конфигов микроскопа, то сохраните куда-нибудь себе
значения, которые вы в них прописали.

Речь про следующие конфиги:
/home/pi/.microscope/microscope_server.conf # конфиг сервера
/home/pi/.microscope/modbus_converter.conf # конфиг модбаса

После переустановки старый конфиг МОДБАСА можно просто положить вместо нового по указанному пути.

А конфиг СЕРВЕРА нужно править именно руками(если конечно вам это необходимо).
Подменить его на старый после переустановки, нельзя! Так как там появились новые поля.
Собственно поля FTP, которые вам тоже нужно туда вписать, указав данные вашего сервера.
А затем перезапустить сервис:
sudo systemctl restart microscope_server.service
```

## Обновление платы RPI4
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

5.
Далее нужно настроить ваш внешний FTP сервер.


## Запуск и настройка FTP сервера.
Если у вас FTP сервер уже установлен и настроен, то этот шаг можно пропустить.
НО в конфиге `/home/pi/.microscope/microscope_server.conf` укажите параметры вашего сервера.
ip, port, user и password для логина на сервер.
```
# Установка FTP-сервера vsftpd
sudo apt update
sudo apt install vsftpd
sudo systemctl status vsftpd
sudo systemctl enable vsftpd



# Настройка FTP-сервера на Ubuntu
sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.original
sudo vim /etc/vsftpd.conf

listen=YES
listen_ipv6=NO
local_enable=YES
write_enable=YES
local_umask=022
dirmessage_enable=YES
use_localtime=YES
connect_from_port_20=YES
pam_service_name=vsftpd
xferlog_enable=YES
xferlog_file=/var/log/xferlog 
xferlog_std_format=NOT
vsftpd_log_file=/var/log/vsftpd.log
log_ftp_protocol=YES
ssl_enable=NO   <-------- если НЕ используете SSL

sudo systemctl restart vsftpd



# Подключение защищенного соединения SSL/TLS (Если ssl_enable=YES)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/vsftpd.pem -out /etc/ssl/private/vsftpd.pem
sudo vim /etc/vsftpd.conf

rsa_cert_file=/etc/ssl/private/vsftpd.pem
rsa_private_key_file=/etc/ssl/private/vsftpd.pem

sudo systemctl restart vsftpd



# Создание FTP-пользователей и предоставление доступа
sudo vim /etc/vsftpd.userlist # Затем введите имена пользователей — в одной строке вводите одно имя.



# Создайте нового пользователя:
sudo useradd ftpuser
sudo passwd ftpuser
sudo usermod -aG sudo ftpuser
echo "ftpuser" | sudo tee -a /etc/vsftpd.userlist



# Настройка работы брандмауэра
sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
sudo ufw allow OpenSSH
sudo ufw allow 990/tcp
sudo ufw allow 40000:50000/tcp
sudo ufw disable
sudo ufw enable
sudo ufw status

sudo systemctl restart vsftpd
```

## Логика работы FTP со стороны RPI.
Также в конфиге `/home/pi/.microscope/microscope_server.conf` есть параметр
`ftp_video_file_duration_sec`. В него надо указать значение в **секундах** на какие 
временные отрезки нарезать видео поток и сохранять в файлы.

Например, 600. Значит сервер будет сохранять видео файлы с длиною записи в 10 минут.
Можно указать от 30 секунд. Верхняя граница по сути ограничена только размером вставленной флешки в устройство.
Так как сначала видео пишется локально на RPI в файл. Например, 10 минут, как в примере выше. А затем программа начинает писать НОВЫЙ файл. А в это время старый передаётся по FTP на ваш сервер.

По окончанию передачи переданный **только что**
файл **удаляется** с флешки PRI. Затем прошивка ждёт окончания новой записи в 10 минут (если в конфиге было 600).
Как только новый файл в 10 минут создался, прошивка начинает передавать этот новый файл. И так по кругу.

Данная логика работает тогда, когда кнопка FTP была
вкллючена в интерфейсе пользователя микроскопа. Текущий статус включена\выключена или ошибка - отображаются
под указанной кнопкой в интерфейсе.
Какие возможны статусы у этой кнопки:
 - FTP enabled. Это отображается ЗЕЛЕНЫМ цветом. Если всё так, то FTP сервер усмешно найден, логин в него прошёл тоже успешно и сама логика прошивки тоже успешно стартовала работу.
 - FTP disabled. Это отображается ЧЁРНЫМ цветом. Значит логика работы FTP отключена и сейчас существует только видео поток в браузер. На FTP сервер ничего не пишется.
 - FTP error. Это отображается КРАСНЫМ цветом. И рядом в скобках указан код ошибки. Это значит, что вы только что попытались включить FTP, то есть нажали на кнопку, и сервер попытался запустить всю вышеописанную логику и у него не получилось по каким-то причинам. Скорее всего неверные данные о FTP сервере в конфиге.
**Возможные коды ошибок**
```bash
# Существуют технически верные ip:port, но на них нет запущенного FTP сервера.
WRONG_IP_OR_PORT = 1,

# Указанные в конфиге пользователь и\или пароль неверны.
WRONG_USER_OR_PASS = 2,

# Значит совсем всё плохо. Нет сети, например. Или внутренняя ошибка сервера.
UNKNOWN_ERR = 3,

# Видео сохраняются в домашней директории пользователя.
# Конкретно в папке ~/Microscope_videos. Она создается при первом запуске и успешном коннекте.
# Данная ошибка говорит о том, что не получилось создать эту папку.
# Видимо неверные права доступа.
FAILED_TO_CREATE_ROOT_VIDEO_DIR_ON_SERV = 4,

# В конфиге указаны технически неверные ip:port.
# Например, если вместо ip:port указать пустоту, слова\буквы или адреса больше 255.
FTP_CONNECTION_TIMEOUT = 5
```
