"""
Library to control the FLIR AX-8 Thermal Camera using its Modbus interface

Written By : Sharath (IMRE Singapore)
Date       : 23-07-2021

"""

from pyModbusTCP.client import ModbusClient
from ax8_modbus_utils import parse_float, float_to_modbus, int_to_modbus
from ax8_modbus_regs import SPOTMETER_REGS

class Ax8ThermalCamera:

    def __init__(self, ip_address:str, verbose:bool = True):
        """        
        Parameters
        ----------
        ip_address : str
            IP Address of the AX8 Thermal Camera.
        verbose : bool, optional
            Verbose mode. The default is True.

        
        Returns
        -------
        None.

        """
        self.verbose = True
        # Initialize the modbus connection and try to read a register
        try:
            self.modbus = ModbusClient(host=ip_address, port=502, auto_open=True, auto_close=True)
            self.get_internal_camera_temperature()
        except Exception as ee:
            print("Unable to establish Modbus TCP! Error-", str(ee))
            raise ee
        # Port opened succesfully
        if self.verbose:
                print("Established Modbus TCP at", self.modbus.host())
        # Set default spotmeter parameters
        self.__default_params = {
                'reflected_temp': 298.0,
                'emissivity'    : 0.95,
                'distance'      : 0.5
            }
        self.spotmeter_params = {}
        self.set_spotmeter_parameters(self.__default_params)
                
    def get_internal_camera_temperature(self):
        """
        Fetch the internal camera temperature in Kelvin
        
        Returns
        -------
        cam_temp : float

        """
        self.modbus.unit_id(1)
        cam_temp = parse_float(self.modbus.read_holding_registers(reg_addr=1017, reg_nb=2))
        if self.verbose:
            print("Internal Camera Temperature", cam_temp)
        return cam_temp
    
    # Spotmeter operation
    def set_spotmeter_parameters(self, params:dict):
        """
        Set the temperature calculation parameters to be used when enabling a spotmeter.

        Parameters
        ----------
        params : dict
            Valid keys are 'reflected_temp' (float, unit is Kelvin), 'emissivity' (float, between 0.001 - 1.0), 'distance' (float, unit is metres, min 0.2).

        Returns
        -------
        None.

        """
        for key in params:
            if key in self.__default_params:
                self.spotmeter_params[key] = params[key]
        
    def enable_spotmeter(self, instances:list, use_local_params:bool = True):
        """
        Enable spotmeters with given instance IDs; the AX8 can have up to 5 individual spotmeters.

        To enable spotmeter 1 at (30, 40) and spotmeter 2 at (50, 20), use the following lines:
            cam = Ax8ThermalCamera(<ip_address>)
            cam.set_spotmeter_parameters(<parameters>)
            cam.enable_spotmeter(instances=[(1,30,40), (2,50,20)])
            cam.get_spotmeter_temps([1,2])
            cam.disable_spotmeter([1,2])
        
        Parameters
        ----------
        instances : list
            This is a list of tuples, with each element having the form (instance_id [int], spot_x_pos[int], spot_y_pos[int]). X pos is clamped between 2 and 78. Y pos is clamped between 2 and 58. The lower left corner is pixel (2,58).
        use_local_params : bool, optional
            Each spotmeter can use its own set of local parameters. If set to false, the global parameters will be used by the camera. The default is True.

        Returns
        -------
        None.

        """
        # Enables spotmeters with the given indices
        self.modbus.unit_id(SPOTMETER_REGS['UNIT_ID'])
        for (inst, spot_x, spot_y) in instances:
            base_reg_addr = (inst*4000)
            if use_local_params:
                self.modbus.write_multiple_registers(base_reg_addr + SPOTMETER_REGS['ENABLE_LOCAL_PARAMS'], [1, 1])
                self.modbus_write_multiple_registers(base_reg_addr + SPOTMETER_REGS['REFLECTED_TEMP'], float_to_modbus(self.spotmeter_params['reflected_temp']))
                self.modbus_write_multiple_registers(base_reg_addr + SPOTMETER_REGS['EMISSIVITY'], float_to_modbus(self.spotmeter_params['emissivity']))
                self.modbus_write_multiple_registers(base_reg_addr + SPOTMETER_REGS['DISTANCE'], float_to_modbus(self.spotmeter_params['distance']))
            self.modbus.write_multiple_registers(base_reg_addr + SPOTMETER_REGS['SPOT_X_POSITION'], int_to_modbus(spot_x))
            self.modbus.write_multiple_registers(base_reg_addr + SPOTMETER_REGS['SPOT_Y_POSITION'], int_to_modbus(spot_x))
            self.modbus.write_multiple_registers(base_reg_addr + SPOTMETER_REGS['ENABLE_SPOTMETER'], [1, 1])
            
            
    def disable_spotmeter(self, instances:list):
        # Disables spotmeters with the given indices
        self.modbus.unit_id(SPOTMETER_REGS['UNIT_ID'])
        for inst in instances:
            base_reg_addr = (inst*4000)
            self.modbus.write_multiple_registers(base_reg_addr + SPOTMETER_REGS['ENABLE_SPOTMETER'], [1, 1]) 
    
    def get_spotmeter_temps(self, instances:list, unit:str='Celsius'):
        """
        Get the temperature readings for the specified spotmeters - assumes that the spotmeters are already enabled.

        Parameters
        ----------
        instances : list
            List of spotmeter instance IDs for which temperature readings are required.
        unit : str, optional
            Output temperature units, one of 'Kelvin' or 'Celsius'. The default is 'Celsius'.

        Returns
        -------
        list of float values.

        """
        # Get spotmeter temperature for the given indices
        self.modbus.unit_id(SPOTMETER_REGS['UNIT_ID'])
        ret_vals = []
        conv = {'Celsius' : -273.1, 'Kelvin' : 0}
        for inst in instances:
            base_reg_addr = (inst*4000)
            temp_raw = self.modbus.read_holding_registers(base_reg_addr + SPOTMETER_REGS['SPOT_TEMPERATURE'], 6)
            val = parse_float(temp_raw[-2:]) + conv.get(unit, 0)
            ret_vals.append(val)
        return ret_vals
            
        
#cam = Ax8ThermalCamera("192.168.1.11")