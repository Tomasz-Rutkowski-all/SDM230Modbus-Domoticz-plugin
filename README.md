# SDM72D-Modbus
SDM72D-Modbus 3-fase power meter with RS485 Port modbus RTU plugin for domoticz

Original code bij MFxMF for the SDM630-M power meter https://github.com/MFxMF/SDM630-Modbus

Installation: <br>
cd ~/domoticz/plugins<br>
git clone https://github.com/bbossink/SDM72D-Modbus-Domoticz-plugin <br>
<br><br>
Configuration: <br>
Select "Eastron SDM72-D-Modbus" in Hardware configuration screen<br>
If needed modify some parameters and click add<br>
9 new devices will be automatically added. Go to devices tab, there you can find them<br>
Don't forget to restart your Domoticz server<br>
<br><br>
Used python modules: <br>
pyserial -> https://pythonhosted.org/pyserial/ <br>
minimalmodbus -> http://minimalmodbus.readthedocs.io<br>
<br>
<br>
Tested on domoticz 4.10717

