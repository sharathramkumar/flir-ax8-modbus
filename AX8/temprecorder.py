# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 15:17:30 2021

@author: Sharath
"""


from ax8 import Ax8ThermalCamera
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#%%

cam = Ax8ThermalCamera("192.168.1.111")
cam.video.toggle_feed()
#%% Cell 2
#params = {'reflected_temp': 273.1 + 25.7, 'emissivity': 0.9, 'distance': 0.25}
#cam.set_spotmeter_parameters(params)
#%%
import datetime as dt
import time
data = []
while True:
    try:
        t1, t2 = cam.get_spotmeter_temps([1,2])
    except:
        continue
    data.append((dt.datetime.now().strftime('%H:%M:%S'), t1, t2))
    time.sleep(1)
#%%
import pickle
pickle.dump(data, open('temps.dat', 'wb'))