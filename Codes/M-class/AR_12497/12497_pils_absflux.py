#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 22:30:51 2022

@author: shreeyeshbiswal
"""

import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

AR = "12497"
core_dir = "/home/shreeyeshbiswal/IDLWorkspace/Dataset_PF/"
base_dir = "/home/shreeyeshbiswal/IDLWorkspace/Dataset_PF/AR_" + AR
dir_list = sorted(os.listdir(base_dir))
n = len(dir_list)
m = 10 # values per file 
tot_len_matrix = np.zeros(shape=(n,m))
max_len_matrix = np.zeros(shape=(n,m))
abs_flx_matrix = np.zeros(shape=(n,m))
index = np.arange(0,n)
height = np.arange(0,m)*0.36

P3 = 'Absolute Flux near PILs (10$^{20}$ Mx); AR ' + AR
colorbarticks = [0, 10, 20, 30, 40, 50, 60, 70, 80]
cbar_min = 0
cbar_max = 80
flare_time = 106.60

for i in range(0,n):

    Time_tag = dir_list[i]
    Time = Time_tag[0:19]
    Hour = Time[11:13]        
    print(Time)
    dir = "/home/shreeyeshbiswal/IDLWorkspace/Dataset_PF/AR_" + AR + "/" + Time_tag
    os.chdir(dir)
    
    # the if-else statement takes care of missing data 
    if len(os.listdir(dir)) != 0:
        mpils = np.loadtxt("PF_ext_mpils_" + Time + ".dat")
        print(np.shape(mpils))
        tot_len_matrix[i,:] = mpils[:,0]
        max_len_matrix[i,:] = mpils[:,1]
        abs_flx_matrix[i,:] = mpils[:,2]
        print(Hour)
    else:
        tot_len_matrix[i,:] = np.nan
        max_len_matrix[i,:] = np.nan
        abs_flx_matrix[i,:] = np.nan
        print("Empty directory")

os.chdir(core_dir)  

x = np.arange(0,n)

figure(figsize=(10,10), dpi=100000)
figure, axs = plt.subplots(10)
figure.set_figheight(15)
figure.set_figwidth(9)
cm = plt.cm.get_cmap('afmhot')
mpl.rc('xtick', labelsize=13) 

# Plot
sc = axs[0].scatter(x, abs_flx_matrix[:,9], c = abs_flx_matrix[:,9], vmin=cbar_min, vmax=cbar_max, s=10, cmap=cm)

for i in range(0,m):
    axs[i].scatter(x, abs_flx_matrix[:,9-i], c = abs_flx_matrix[:,9-i], vmin=cbar_min, vmax=cbar_max, s=10, cmap=cm)

for i in range(0,m):
    axs[i].set_ylim([cbar_min, cbar_max])

plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[]);  
axs[9].tick_params(axis='x', labelsize=16)
axs[9].set_xticks(np.arange(0,n,24))

# Hide the ylims of individual boxes
for i in range(0,m):
    axs[i].set_yticks([])

# Show heights in the altitude
heightfont = 16
for i in range(0,m):
    max_alt = (m-1)*0.36
    altitude = max_alt-(i*0.36)
    alt_str = "{:.2f}".format(altitude)
    axs[i].set_ylabel(alt_str + '          ', fontsize = heightfont, rotation = 0)

# Show flare occurence in dotted lines
for i in range(0,m):
    axs[i].axvline(x = flare_time, ymin = 0, ymax = 1, linestyle = '--', color = 'k', alpha=0.40)# Show heights in the altitude

# Orient the text
st = dir_list[0]
start_time = st[0:4] + '/' + st[5:7] + '/' + st[8:10] + '/' + st[11:13] + ':' + st[14:16]
axs[0].text(-21, (cbar_max + (0.35*(cbar_max - cbar_min))), P3, fontsize=23)
axs[5].text(-42, 0.5*(cbar_max - cbar_min), 'Height (Mm)', rotation = 90, fontsize=18)
axs[9].text(21, (cbar_min - (0.65*(cbar_max - cbar_min))), 'Time after ' + start_time + ' (hrs)', rotation = 0, fontsize=18)

figure.subplots_adjust(right=0.8)
cbar_ax = figure.add_axes([0.85, 0.15, 0.05, 0.7])
cbar_ax.tick_params(labelsize=16) 
figure.colorbar(sc, cax=cbar_ax, ticks=colorbarticks)
plt.subplots_adjust(wspace=0.5, hspace=0)
plt.show()

mpl.rcParams.update(mpl.rcParamsDefault)
