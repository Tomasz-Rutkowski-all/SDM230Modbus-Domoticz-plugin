# SDM230-Modbus NO TESTING
SDM230-Modbus 3-fase power meter with RS485 Port modbus RTU plugin for domoticz

Original code bij MFxMF for the SDM630-M power meter https://github.com/MFxMF/SDM630-Modbus
Original code by bbossink for the SDM72-D-M power mether https://github.com/remcovanvugt/SDM120Modbus-Domoticz-plugin

Installation: <br>
cd ~/domoticz/plugins<br>
git clone https://github.com/Tomasz-Rutkowski-all/SDM230Modbus-Domoticz-plugin <br>
<br>
Configuration: <br>
Select "Eastron SDM120-Modbus" in Hardware configuration screen<br>
If needed modify some parameters and click add<br>
Hint: Set reading interval to 0 if you want updates per "heartbeat" of the system (aprox 10s in my case)<br>
<br>
9 new devices will be automatically added. Go to devices tab, there you can find them<br>
Don't forget to restart your Domoticz server<br>
Tested on domoticz 4.10717
<br><br><br>
Used python modules: <br>
pyserial -> https://pythonhosted.org/pyserial/ <br>
minimalmodbus -> http://minimalmodbus.readthedocs.io<br>
