#!/usr/bin/env python
"""
Eastron SDM72D-Modbus Smart Meter Three Phase Electrical System. The Python plugin for Domoticz
Original author: MFxMF
Modified by: bbossink
Requirements: 
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip3 install minimalmodbus)
    2.Communication module Modbus USB to RS485 converter module
"""
"""
<plugin key="SDM72D" name="Eastron SDM72D-Modbus" version="1.0.0" author="bbossink">
    <params>
        <param field="SerialPort" label="Modbus Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600"  />
        <param field="Mode2" label="Device ID" width="40px" required="true" default="1" />
        <param field="Mode3" label="Reading Interval min." width="40px" required="true" default="1" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>

"""

import minimalmodbus
import serial
import Domoticz


class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        self.rs485 = "" 
        return

    def onStart(self):
        self.rs485 = minimalmodbus.Instrument(Parameters["SerialPort"], int(Parameters["Mode2"]))
        self.rs485.serial.baudrate = Parameters["Mode1"]
        self.rs485.serial.bytesize = 8
        self.rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.rs485.serial.stopbits = 1
        self.rs485.serial.timeout = 1
        self.rs485.debug = False
                          

        self.rs485.mode = minimalmodbus.MODE_RTU
        devicecreated = []
        Domoticz.Log("Eastron SDM72D Modbus plugin start")
        self.runInterval = int(Parameters["Mode3"]) * 1 
       
        if 1 not in Devices:
            Domoticz.Device(Name="Total System Power", Unit=1,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"} 
        if 2 not in Devices:
            Domoticz.Device(Name="Import Wh since last reset", Unit=2,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"}
        if 3 not in Devices:
            Domoticz.Device(Name="Export Wh since last reset", Unit=3,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 4 not in Devices:
            Domoticz.Device(Name="Total kWh", Unit=4,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"}
        if 5 not in Devices:
            Domoticz.Device(Name="Settable total kWh", Unit=5,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"}
        if 6 not in Devices:
            Domoticz.Device(Name="Settable import kWh", Unit=6,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"}
        if 7 not in Devices:
            Domoticz.Device(Name="Settable export kWh", Unit=7,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"}
        if 8 not in Devices:
            Domoticz.Device(Name="Import power", Unit=8,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"} 
        if 9 not in Devices:
            Domoticz.Device(Name="Export power", Unit=9,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"} 
               
    def onStop(self):
        Domoticz.Log("Eastron SDM72D Modbus plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;
        if self.runInterval <= 0:
            # Get data from SDM72D
            Total_System_Power = self.rs485.read_float(52, functioncode=4, numberOfRegisters=2)
            Import_Wh_since_last_reset = self.rs485.read_float(72, functioncode=4, numberOfRegisters=2)
            Export_Wh_since_last_reset = self.rs485.read_float(74, functioncode=4, numberOfRegisters=2)
            Total_kwh = self.rs485.read_float(342, functioncode=4, numberOfRegisters=2)
            Settable_total_kWh = self.rs485.read_float(384, functioncode=4, numberOfRegisters=2)
            Settable_import_kWh = self.rs485.read_float(388, functioncode=4, numberOfRegisters=2)
            Settable_export_kWh = self.rs485.read_float(390, functioncode=4, numberOfRegisters=2)
            Import_power = self.rs485.read_float(1280, functioncode=4, numberOfRegisters=2)
            Export_power = self.rs485.read_float(1282, functioncode=4, numberOfRegisters=2)
            
            #Update devices
            Devices[1].Update(0,str(Total_System_Power))
            Devices[2].Update(0,str(Import_Wh_since_last_reset*1000))
            Devices[3].Update(0,str(Export_Wh_since_last_reset*1000))
            Devices[4].Update(0,str(Total_kwh))
            Devices[5].Update(0,str(Settable_total_kWh))
            Devices[6].Update(0,str(Settable_import_kWh))
            Devices[7].Update(0,str(Settable_export_kWh))
            Devices[8].Update(0,str(Import_power))
            Devices[9].Update(0,str(Export_power))
            
            
            if Parameters["Mode6"] == 'Debug':
                Domoticz.Log("Eastron SDM72D Modbus Data")
                Domoticz.Log('Total system power: {0:.3f} W'.format(Total_System_Power))
                Domoticz.Log('Import Wh since last reset: {0:.3f} kWh'.format(Import_Wh_since_last_reset))
                Domoticz.Log('Export Wh since last reset: {0:.3f} kWh'.format(Export_Wh_since_last_reset))
                Domoticz.Log('Total kwh: {0:.3f} kWh'.format(Total_kwh))
                Domoticz.Log('Settable total kWh: {0:.3f} kWh'.format(Settable_total_kWh))
                Domoticz.Log('Settable import kWh: {0:.3f} kWh'.format(Settable_import_kWh))
                Domoticz.Log('Settable export kWh: {0:.3f} kWh'.format(Settable_export_kWh))
                Domoticz.Log('Import power: {0:.3f} kWh'.format(Import_power))
                Domoticz.Log('Export power: {0:.3f} kWh'.format(Export_power))
               
            self.runInterval = int(Parameters["Mode3"]) * 6


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
