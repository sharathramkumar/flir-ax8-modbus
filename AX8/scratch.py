# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 12:14:14 2021

@author: Sharath
"""

#%% Cell 1
from ax8 import Ax8ThermalCamera
import matplotlib.pyplot as plt
import numpy as np

#%%

cam = Ax8ThermalCamera("192.168.1.111")

#%% Cell 2
params = {'reflected_temp': 273.1 + 25.7, 'emissivity': 0.9, 'distance': 0.25}
cam.set_spotmeter_parameters(params)

#%% C3
# out = []
# for ii in range(0, 60, 4):  
#     cam.enable_spotmeter(instances=[(1,40,ii), (2,40,ii+1), (3,40,ii+2), (4,40,ii+3)])
#     temps = cam.get_spotmeter_temps([1,2,3,4])
#     out += [temps]
#%%
# plt.plot(out)
# #%%
# import numpy as np
#%%
# out = np.zeros((80,60))
# for ii in range(0, 80, 10):
#     for jj in range(0, 60, 5):
#         print("Now", ii, jj, '\n')
#         cam.enable_spotmeter(instances=[(1,ii,jj), (2,ii,jj+1), (3,ii,jj+2), (4,ii,jj+3), (5,ii,jj+4)])
#         temps = cam.get_spotmeter_temps([1,2,3,4,5])
#         for t in range(5):
#             out[ii][jj+t] = temps[t]
#%%
# import cv2
# import matplotlib.pyplot as plt
# #%%
# print(out[40,:])
# plt.plot(out[40,:][17:32])
#%%
# cutlines_x = {}
# for xx in range(30,50,4):
#     print("Running", xx)
#     cutlines_x[xx] = cam.get_cutline_x(xx)
# #%%
# print(cutlines_x[30])
# for kk in cutlines_x:
#     plt.plot(cutlines_x[kk][0] + 273.1, label = str(kk))
# plt.legend()
# #%%
# for kk in cutlines_x:
#     plt.plot(cutlines_x[kk][0] + 273.1, label = str(kk))
# plt.legend()
#%%
# ni_cutline = cam.get_cutline_x(x=45)
#%%
# x_ax = np.arange(60)
# plt.plot(x_ax, ni_cutline[0])
# plt.scatter(x_ax, ni_cutline[0])
#%%
pos = cam.get_spotmeter_position([1])
print(pos)
#%%
print(cam.get_spotmeter_temps([1,2]))
#%%
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ax8_thermal_primitiv_defs import th_primi

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

cam.enable_spotmeter([(1, th_primi['wafer_center_x'], th_primi['wafer_bbox_ur_y']),(2, th_primi['wafer_center_x'], th_primi['wafer_bbox_ll_y'])])

def animate(i, xs, ys):
    t1, t2 = cam.get_spotmeter_temps([1,2])
    tdiff = abs(round(t2 - t1, 2))
    
     # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(tdiff)

    # Limit x and y lists to 20 items
    xs = xs[-360:]
    ys = ys[-360:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.ylim((0,30))
    plt.title('Temperature difference over Time')
    plt.ylabel('Temperature (deg C)')

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=5000)
plt.show()    
#%%
ni_cutline = cam.get_cutline_y(y=th_primi['wafer_center_y'])
#%%
y_ax = np.arange(80)
plt.xlim((th_primi['wafer_bbox_ll_x'], th_primi['wafer_bbox_ur_x']))
#plt.ylim((th_primi['wafer_bbox_ll_x'], th_primi['wafer_bbox_ur_x']))
plt.plot(y_ax, ni_cutline[0])
plt.scatter(y_ax, ni_cutline[0])
#%%
cam.enable_spotmeter([(1, th_primi['wafer_center_x'], th_primi['wafer_center_y'])])