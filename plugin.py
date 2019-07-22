#!/usr/bin/env python
"""
Eastron SDM72D-Modbus Smart Meter Three Phase Electrical System. The Python plugin for Domoticz
Author: MFxMF
Modified by: bbossink
Requirements: 
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip3 install minimalmodbus)
    2.Communication module Modbus USB to RS485 converter module
"""
"""
<plugin key="SDM72D" name="Eastron SDM72D-Modbus" version="1.0.0" author="MFxMF">
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
            Domoticz.Device(Name="Total kWh", Unit=4,TypeName="Usage",Used=0).Create()
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
            Devices[1].Update(0,str(Volts_L1))
            Devices[2].Update(0,str(Volts_L2))
            Devices[3].Update(0,str(Volts_L3))
            Devices[4].Update(0,str(Current_L1)+";"+str(Current_L2)+";"+str(Current_L3))
            Devices[5].Update(0,str(Active_Power_L1))
            Devices[6].Update(0,str(Active_Power_L2))
            Devices[7].Update(0,str(Active_Power_L3))
            Devices[8].Update(0,str(Apparent_Power_L1))
            Devices[9].Update(0,str(Apparent_Power_L2))
            
            Devices[10].Update(0,str(Apparent_Power_L3))
            Devices[11].Update(0,str(Active_Power_L1)+";"+str(Active_Power_L1))
            Devices[12].Update(0,str(Active_Power_L2)+";"+str(Active_Power_L2))
            Devices[13].Update(0,str(Active_Power_L3)+";"+str(Active_Power_L3))
            Devices[14].Update(0,str(Reactive_Power_L1))
            Devices[15].Update(0,str(Reactive_Power_L2))
            Devices[16].Update(0,str(Reactive_Power_L3))
            Devices[17].Update(0,str(Power_Factor_L1))
            Devices[18].Update(0,str(Power_Factor_L2))
            Devices[19].Update(0,str(Power_Factor_L3))
            Devices[20].Update(0,str(Phase_Angle_L1))
            Devices[21].Update(0,str(Phase_Angle_L2))
            Devices[22].Update(0,str(Phase_Angle_L3))
            Devices[23].Update(0,str(Average_line_to_neutral_volts))
            Devices[24].Update(0,str(Average_line_current))
            Devices[25].Update(0,str(Sum_of_line_current))
            Devices[26].Update(0,str(Total_System_Active_Power))
            Devices[27].Update(0,str(Total_System_Apparent_Power))
            Devices[28].Update(0,str(Total_System_Reactive_Power))
            Devices[29].Update(0,str(Total_System_Power_Factor))
            Devices[30].Update(0,str(Total_System_Phase_Angle))
            Devices[31].Update(0,str(Frequency_Of_Supply_Voltages))
            Devices[32].Update(0,str(Import_Wh_since_last_reset*1000))
            Devices[33].Update(0,str(Export_Wh_since_last_reset*1000))
            Devices[34].Update(0,str(Import_VArh_since_last_reset))
            Devices[35].Update(0,str(Export_VArh_since_last_reset))
            Devices[36].Update(0,str(VAh_since_last_reset))
            Devices[37].Update(0,str(Ah_since_last_reset))
            Devices[38].Update(0,str(Total_system_power_demand))
            Devices[39].Update(0,str(Maximum_total_system_power_demand))
            Devices[40].Update(0,str(Total_system_VA_demand))
            Devices[41].Update(0,str(Maximum_total_system_VA_demand))
            Devices[42].Update(0,str(Neutral_current_demand))
            Devices[43].Update(0,str(Maximum_neutral_current_demand))
            Devices[44].Update(0,str(Line_1_to_Line_2_volts))
            Devices[45].Update(0,str(Line_2_to_Line_3_volts))
            Devices[46].Update(0,str(Line_3_to_Line_1_volts))
            Devices[47].Update(0,str(Average_line_to_line_volts))
            Devices[48].Update(0,str(Neutral_current))
            Devices[49].Update(0,str(Phase_1_LN_volts_THD))
            Devices[50].Update(0,str(Phase_2_LN_volts_THD))
            Devices[51].Update(0,str(Phase_3_LN_volts_THD))
            Devices[52].Update(0,str(Phase_1_Current_THD))
            Devices[53].Update(0,str(Phase_2_Current_THD))
            Devices[54].Update(0,str(Phase_3_Current_THD))
            Devices[55].Update(0,str(Average_line_to_neutral_volts_THD))
            Devices[56].Update(0,str(Average_line_current_THD))
            Devices[57].Update(0,str(Total_system_power_factor))
            Devices[58].Update(0,str(Phase_1_current_demand))
            Devices[59].Update(0,str(Phase_2_current_demand))
            Devices[60].Update(0,str(Phase_3_current_demand))
            Devices[61].Update(0,str(Maximum_phase_1_current_demand))
            Devices[62].Update(0,str(Maximum_phase_2_current_demand))
            Devices[63].Update(0,str(Maximum_phase_3_current_demand))
            Devices[64].Update(0,str(Line_1_to_line_2_volts_THD))
            Devices[65].Update(0,str(Line_2_to_line_3_volts_THD))
            Devices[66].Update(0,str(Line_3_to_line_1_volts_THD))
            Devices[67].Update(0,str(Average_line_to_line_volts_THD))
            Devices[68].Update(0,str(Total_kwh*1000))
            Devices[69].Update(0,str(Total_kvarh))
            Devices[70].Update(0,str(L1_import_kwh*1000))
            Devices[71].Update(0,str(L2_import_kwh*1000))
            Devices[72].Update(0,str(L3_import_kwh*1000))
            Devices[73].Update(0,str(L1_export_kwh*1000))
            Devices[74].Update(0,str(L2_export_kwh*1000))
            Devices[75].Update(0,str(L3_export_kwh*1000))
            Devices[76].Update(0,str(L1_total_kwh*1000))
            Devices[77].Update(0,str(L2_total_kwh*1000))
            Devices[78].Update(0,str(L3_total_kwh*1000))
            Devices[79].Update(0,str(L1_import_kvarh))
            Devices[80].Update(0,str(L2_import_kvarh))
            Devices[81].Update(0,str(L3_import_kvarh))
            Devices[82].Update(0,str(L1_export_kvarh))
            Devices[83].Update(0,str(L2_export_kvarh))
            Devices[84].Update(0,str(L3_export_kvarh))
            Devices[85].Update(0,str(L1_total_kvarh))
            Devices[86].Update(0,str(L2_total_kvarh))
            Devices[87].Update(0,str(L3_total_kvarh))
            Devices[88].Update(0,str(Total_System_Active_Power)+";"+str(Total_System_Active_Power))


            if Parameters["Mode6"] == 'Debug':
                Domoticz.Log("Eastron SDM630 Modbus Data")
                Domoticz.Log('Voltage L1: {0:.3f} V'.format(Volts_L1))
                Domoticz.Log('Voltage L2: {0:.3f} V'.format(Volts_L2))
                Domoticz.Log('Voltage L3: {0:.3f} V'.format(Volts_L3))
                Domoticz.Log('Current L1: {0:.3f} A'.format(Current_L1))
                Domoticz.Log('Current L2: {0:.3f} A'.format(Current_L2))
                Domoticz.Log('Current L3: {0:.3f} A'.format(Current_L3))
                Domoticz.Log('Active power L1: {0:.3f} W'.format(Active_Power_L1))
                Domoticz.Log('Active power L2: {0:.3f} W'.format(Active_Power_L2))
                Domoticz.Log('Active power L3: {0:.3f} W'.format(Active_Power_L3))
                Domoticz.Log('Apparent power L1: {0:.3f} VA'.format(Apparent_Power_L1))
                Domoticz.Log('Apparent power L2: {0:.3f} VA'.format(Apparent_Power_L2))
                Domoticz.Log('Apparent power L3: {0:.3f} VA'.format(Apparent_Power_L3))
                Domoticz.Log('Reactive power L1: {0:.3f} VAr'.format(Reactive_Power_L1))
                Domoticz.Log('Reactive power L2: {0:.3f} VAr'.format(Reactive_Power_L2))
                Domoticz.Log('Reactive power L3: {0:.3f} VAr'.format(Reactive_Power_L3))
                Domoticz.Log('Power factor L1: {0:.3f}'.format(Power_Factor_L1))
                Domoticz.Log('Power factor L2: {0:.3f}'.format(Power_Factor_L2))
                Domoticz.Log('Power factor L3: {0:.3f}'.format(Power_Factor_L3))
                Domoticz.Log('Phase angle L1: {0:.3f} Degree'.format(Phase_Angle_L1))
                Domoticz.Log('Phase angle L2: {0:.3f} Degree'.format(Phase_Angle_L2))
                Domoticz.Log('Phase angle L3: {0:.3f} Degree'.format(Phase_Angle_L3))
                Domoticz.Log('Average line to neutral volts: {0:.3f} V'.format(Average_line_to_neutral_volts))
                Domoticz.Log('Average line current: {0:.3f} A'.format(Average_line_current))
                Domoticz.Log('Sum of line current: {0:.3f} A'.format(Sum_of_line_current))
                Domoticz.Log('Total system power: {0:.3f} W'.format(Total_System_Active_Power))
                Domoticz.Log('Total system apparent power: {0:.3f} VA'.format(Total_System_Apparent_Power))
                Domoticz.Log('Total system reactive  power: {0:.3f} VA'.format(Total_System_Reactive_Power))
                Domoticz.Log('Total system power factor: {0:.3f} PF'.format(Total_System_Power_Factor))
                Domoticz.Log('Total system phase angle: {0:.3f} Degree'.format(Total_System_Phase_Angle))
                Domoticz.Log('Frequency of supply voltages: {0:.3f} Hz'.format(Total_System_Phase_Angle))
                Domoticz.Log('Import Wh since last reset: {0:.3f} kWh'.format(Import_Wh_since_last_reset))
                Domoticz.Log('Export Wh since last reset: {0:.3f} kWh'.format(Export_Wh_since_last_reset))
                Domoticz.Log('Import VArh since last reset: {0:.3f} kVArh'.format(Import_VArh_since_last_reset))
                Domoticz.Log('Export VArh since last reset: {0:.3f} kVArh'.format(Export_VArh_since_last_reset))
                Domoticz.Log('VAh since last reset: {0:.3f} kVAh'.format(VAh_since_last_reset))
                Domoticz.Log('Ah since last reset: {0:.3f} Vh'.format(Ah_since_last_reset))
                Domoticz.Log('Total system power demand: {0:.3f} W'.format(Total_system_power_demand))
                Domoticz.Log('Maximum total system power_demand: {0:.3f} VA'.format(Maximum_total_system_power_demand))
                Domoticz.Log('Total system VA demand: {0:.3f} VA'.format(Total_system_VA_demand))
                Domoticz.Log('Maximum total system VA demand: {0:.3f} VA'.format(Maximum_total_system_VA_demand))
                Domoticz.Log('Neutral current demand: {0:.3f} A'.format(Neutral_current_demand))
                Domoticz.Log('Maximum neutral current demand: {0:.3f} A'.format(Maximum_neutral_current_demand))
                Domoticz.Log('Line 1 to Line 2 volts: {0:.3f} V'.format(Line_1_to_Line_2_volts))
                Domoticz.Log('Line 2 to Line 3 volts: {0:.3f} V'.format(Line_2_to_Line_3_volts))
                Domoticz.Log('Line 3 to Line 1 volts: {0:.3f} V'.format(Line_3_to_Line_1_volts))
                Domoticz.Log('Average line to line volts: {0:.3f} V'.format(Average_line_to_line_volts))
                Domoticz.Log('Neutral current: {0:.3f} A'.format(Neutral_current))
                Domoticz.Log('Phase 1 L/N volts THD: {0:.3f} %'.format(Phase_1_LN_volts_THD))
                Domoticz.Log('Phase 2 L/N volts THD: {0:.3f} %'.format(Phase_2_LN_volts_THD))
                Domoticz.Log('Phase 3 L/N volts THD: {0:.3f} %'.format(Phase_3_LN_volts_THD))
                Domoticz.Log('Phase 1 Current THD: {0:.3f} %'.format(Phase_1_Current_THD))
                Domoticz.Log('Phase 2 Current THD: {0:.3f} %'.format(Phase_2_Current_THD))
                Domoticz.Log('Phase 3 Current THD: {0:.3f} %'.format(Phase_3_Current_THD))
                Domoticz.Log('Average line to neutral volts THD: {0:.3f} %'.format(Average_line_to_neutral_volts_THD))
                Domoticz.Log('Average line current THD: {0:.3f} %' .format(Average_line_current_THD))
                Domoticz.Log('Total system power factor: {0:.3f} Degree'.format(Total_system_power_factor))
                Domoticz.Log('Phase 1 current demand: {0:.3f} A'.format(Phase_1_current_demand))
                Domoticz.Log('Phase 2 current demand: {0:.3f} A'.format(Phase_2_current_demand))
                Domoticz.Log('Phase 3 current demand: {0:.3f} A'.format(Phase_3_current_demand))
                Domoticz.Log('Maximum phase 1 current demand: {0:.3f} A'.format(Maximum_phase_1_current_demand))
                Domoticz.Log('Maximum phase 2 current demand: {0:.3f} A'.format(Maximum_phase_2_current_demand))
                Domoticz.Log('Maximum phase 3 current demand: {0:.3f} A'.format(Maximum_phase_3_current_demand))
                Domoticz.Log('Line 1 to line 2 volts THD: {0:.3f} %'.format(Line_1_to_line_2_volts_THD))
                Domoticz.Log('Line 2 to line 3 volts THD: {0:.3f} %'.format(Line_2_to_line_3_volts_THD))
                Domoticz.Log('Line 3 to line 1 volts THD: {0:.3f} %'.format(Line_3_to_line_1_volts_THD))
                Domoticz.Log('Average line to line volts THD: {0:.3f} %'.format(Average_line_to_line_volts_THD))
                Domoticz.Log('Total kWh: {0:.3f} kWh'.format(Total_kwh))
                Domoticz.Log('Total kVArh: {0:.3f} kWh'.format(Total_kvarh))
                Domoticz.Log('L1 import kWh: {0:.3f} kWh'.format(L1_import_kwh))
                Domoticz.Log('L2 import kWh: {0:.3f} kWh'.format(L2_import_kwh))
                Domoticz.Log('L3 import kWh: {0:.3f} kWh'.format(L3_import_kwh))
                Domoticz.Log('L1 export kWh: {0:.3f} kWh'.format(L1_export_kwh))
                Domoticz.Log('L2 export kWh: {0:.3f} kWh'.format(L2_export_kwh))
                Domoticz.Log('L3 export kWh: {0:.3f} kWh'.format(L3_export_kwh))
                Domoticz.Log('L1 total kWh: {0:.3f} kWh'.format(L1_total_kwh))
                Domoticz.Log('L2 total kWh: {0:.3f} kWh'.format(L2_total_kwh))
                Domoticz.Log('L3 total kWh: {0:.3f} kWh'.format(L3_total_kwh))
                Domoticz.Log('L1 import kVArh: {0:.3f} kVArh'.format(L1_import_kvarh))
                Domoticz.Log('L2 import kVArh: {0:.3f} kVArh'.format(L2_import_kvarh))
                Domoticz.Log('L3 import kVArh: {0:.3f} kVArh'.format(L3_import_kvarh))
                Domoticz.Log('L1 export kVArh: {0:.3f} kVArh'.format(L1_export_kvarh))
                Domoticz.Log('L2 export kVArh: {0:.3f} kVArh'.format(L2_export_kvarh))
                Domoticz.Log('L3 export kVArh: {0:.3f} kVArh'.format(L3_export_kvarh))
                Domoticz.Log('L1 total kvarh: {0:.3f} kVArh'.format(L1_total_kvarh))
                Domoticz.Log('L2 total kvarh: {0:.3f} kVArh'.format(L2_total_kvarh))
                Domoticz.Log('L3 total kvarh: {0:.3f} kVArh'.format(L3_total_kvarh))

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
