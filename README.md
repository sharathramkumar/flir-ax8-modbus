# flir-ax8-modbus
A Python library to interface with the FLIR AX-8 Thermal Camera using the Modbus interface.

Supports the following operations
1. View image feed from the camera
2. Temperature measurement
3. Access camera functions such as spotmeter and other internal registers

Use the following lines to connect to a thermal camera feed

    cam = Ax8ThermalCamera(<ip_address>)
    cam.set_spotmeter_parameters(<parameters>)
    cam.enable_spotmeter(instances=[(1,30,40), (2,50,20)])
    cam.get_spotmeter_temps([1,2])
    cam.disable_spotmeter([1,2])
