# LerdgeX Klipper
 Заметки по установке и настройке Klipper на плате LerdgeX

# Компиляция прошивки

Последнии версии Klipper не собираются по инструкции от Lerdge, чтобы прошивка собралась надо вручную кое-что изменить.

Что изменить в файле ~/klipper/src/stm32/Kconfig

найти:
```
bool "64KiB bootloader" if MACH_STM32F103 || MACH_STM32F446 || MACH_STM32F401
```
изменить на:
```
bool "64KiB bootloader" if MACH_STM32F103 || MACH_STM32F446 || MACH_STM32F401 || MACH_STM32F407
```

найти:
```
default 0x20000 if MACH_STM32F4x5 || MACH_STM32F446
```
изменить на:
```
default 0x1FFF0 if MACH_STM32F4x5 || MACH_STM32F446
```

Дальше выставляем следующее в __make menuconfig__

![](/images/stm32_config.png)

После компиляции прошивки ее надо зашифровать, для этого можно использовать утилиту от Lerdge, или что проще - использовать скрипт на Python:

```
cd ~
wget https://raw.githubusercontent.com/trambouter/LerdgeX_klipper/main/crypt_lerdgeX.py
python3 crypt_lerdgeX.py
```

На выходе получим файл __Lerdge_X_firmware_force.bin__ , закидываем его на microSD карту, предварительно создав там такую структуру каталогов (Lerdge_X_system\Firmware\)

![](/images/folder_flash.png)

Вставляем карточку, запускаем плату - пойдет процесс прошивки, после окончания - выключаем плату и вынимаем карточку. Если карточку не вынуть - то каждый раз при запуске платы будет запускаться процесс прошивки.

Данный способ также подходит для K и Z плат, надо только соотвественно переименовать имя папки и имя прошивки (например: Lerdge_K_system\Firmware\Lerdge_K_firmware_force.bin)

# Подключение к одноплатному компьютеру

Для подключения к RaspberryPi или OrangePi удобно использовать разьем к которому подключается плата WiFi, т.е. без использования USB.

На изображении указаны пины UART, для подключения одноплатного ПК, т.е. RX подключаем к пину RX одноплатника, соотвественно TX подключаем к пину TX.

Активация режима UART на разных одноплатниках и дистрибутивах может быть различна, посмотрите документацию по одноплатнику  и дистрибутиву.

![](/images/Ext_rxtx.png)

# Распиновка разьема расширения

Ниже дана распиновка разьема расширения, эти пины можно использовать для подключения дополнительной перефирии.
Пины PA9 и PA10 использовать не получится, т.к. они используются для обменна данных по UART.

![](/images/LerdgeX_extension.png)

# Подключение драйверов TMC2209 для работы по UART

TMC2209 умеют работать в режиме подключения по одному проводу, при этом каждому драйверу задается адрес, максимальное число драйверов на одной линии 4.

Для начала установим адреса перемычками MS1 и MS2, перемычки MS3 должны быть отключены! 
__ADR__ - это какой адрес получит драйвер.

||MS1|MS2|ADR|
|---|---|---|---|
|X|OFF|OFF|0|
|Y|ON|OFF|1|
|Z|OFF|ON|2|
|E|ON|ON|3|

Далее соединяем все пины RX на драйверах и подключаем к выводу __PC2__ на разьеме расширения (возможно использовать любой другой пин).

![](/images/uart_schematic.png)

Остается добавить только секцию настройки драйверов в конфиг Klipper:

```
[tmc2209 stepper_x]
uart_pin: PC2
run_current: 0.800
stealthchop_threshold: 999999
uart_address: 0
interpolate: False

[tmc2209 stepper_y]
uart_pin: PC2
run_current: 0.800
stealthchop_threshold: 999999
uart_address: 1
interpolate: False

[tmc2209 stepper_z]
uart_pin: PC2
run_current: 0.800
stealthchop_threshold: 999999
uart_address: 2
interpolate: False

[tmc2209 extruder]
uart_pin: PC2
run_current: 0.400
stealthchop_threshold: 999999
uart_address: 3
interpolate: False
```

#### Настройка sensorless homing
Для настройки sensorless homing потребуется соединить выводы DIAG драйверов с входами концевиков X и Y на плате.

![](/images/sensorless_homing.png)

Далее правим конфиг:
+ для начала надо удалить или закомментировать пины которые использовались для концевиков ранее (PB12,PB13)
```
#endstop_pin: ^!PB12
#endstop_pin: ^!PB13 
```

+ в секции __[stepper_x]__ добавим
```
endstop_pin: tmc2209_stepper_x:virtual_endstop
homing_retract_dist: 0
```

+ в секции __[stepper_y]__ добавим
```
endstop_pin: tmc2209_stepper_y:virtual_endstop
homing_retract_dist: 0
```
+ в секции __[tmc2209 stepper_x]__ добавим
```
diag_pin: ^PB12
driver_SGTHRS: 90
```
+ в секции __[tmc2209 stepper_y]__ добавим
```
diag_pin: ^PB13
driver_SGTHRS: 90
```
Информацию по настройке чуствительности driver_SGTHRS смотрите в официальной документации по Klipper


# Подключение дисплея Lerdge к одноплатному пк

Информация о подключении и драйвер для linux доступны в репозитории [https://github.com/trambouter/fb_st7796s_lerdge](https://github.com/trambouter/fb_st7796s_lerdge)

# Распиновка платы LerdgeX

[Lerdge X Pin Map](https://github.com/trambouter/LerdgeX_klipper/raw/main/Lerdge%20X%20Pin%20Map.pdf)
