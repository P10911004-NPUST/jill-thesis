# Generate vegetation indices layers

import os
import sys
import matplotlib.pyplot as plt
import rioxarray as rxr
import streamlit as st
from streamlit.web import cli as stcli
from rasterio.io import MemoryFile

from pycode.utils import gis

img_list = os.listdir("./test")

for i in img_list:
    if i.endswith('tif'):
        i_dir = os.path.join(os.getcwd(), 'test', i)
        i_name = i.split('.')[:-1][0]
        globals()[i_name] = rxr.open_rasterio(i_dir).squeeze()

RGB.shape[0] in [3, 4]
rh, rw = RE.shape

# r = RGB[0].rio.reproject_match(G)
r = gis.layer_match(RGB[0], G)
g = gis.layer_match(RGB[1], R)
print(f"R.shape = {R.shape} = {R.shape[-1]} * {R.shape[-2]} = {R.shape[-1] * R.shape[-2]}")
len(R.data.reshape(-1))



RG = RGB[0] - G
rG = r - G

plt.subplots()
plt.subplot(231), RGB[0].plot.imshow(robust = False), plt.title(f'RGB[0]: {RGB[0].shape}')
plt.subplot(232), G.plot.imshow(robust = False), plt.title(G.shape), plt.title(f'G: {G.shape}')
plt.subplot(233), RG.plot.imshow(robust = False), plt.title(RG.shape), plt.title(f'R-G: {RG.shape}')
plt.subplot(234), r.plot.imshow(robust = False), plt.title(r.shape), plt.title(f'r: {r.shape}')
plt.subplot(235), g.plot.imshow(robust = False), plt.title(g.shape), plt.title(f'g: {g.shape}')
plt.subplot(236), rG.plot.imshow(robust = False), plt.title(rG.shape), plt.title(f'r-G: {rG.shape}')
plt.show()

DTM.plot.imshow(robust = True)
plt.show()

gis.print_raster(R)


# If a single R, G, B is missing, then substitute with RGB image
if 'RGB' in globals():
    for rgb in ['R', 'G', 'B']:
        i = 0
        if rgb not in globals():
            exec(f"{rgb} = RGB[{i}]")
        i += 1

collected_bands = [i for i in ['R', 'G', 'B', 'RE', 'NIR', 'DSM', 'DTM'] if i in globals()]

# Select the band which is the smallest one in area from the collected_bands 
# as the reference layer to resize the others.
ref = collected_bands[0]
for band in collected_bands:
    ref_dim = eval(f"{ref}.shape[-2] * {ref}.shape[-1]")
    band_dim = eval(f"{band}.shape[-2] * {band}.shape[-1]")
    if band_dim < ref_dim:
        ref = band

for band in collected_bands:
    if band != ref:
        # exec(f"{band} = gis.layer_match({band}, {ref})")
        globals()[band] = gis.layer_match(globals()[band], globals()[ref])

vi_requirements = {
    'CSM': ['DSM', 'DTM'],
    'NDVI': ['NIR', 'R'],
    'DATT': ['NIR', 'RE', 'R'],
    'GNDVI': ['NIR', 'G'],
    'NDTI': ['R', 'G'],
    'NExG': ['R', 'G', 'B'],
    'NGRDI': ['R', 'G'],
    'VARI': ['R', 'G', 'B']
    }
    
vi_options = []
for key, val in vi_requirements.items():
    res = True
    for i in val:
        if i not in collected_bands:
            res = False
            break
    if res:
        vi_options.append(key)
print(vi_options)
    
