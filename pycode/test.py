# Generate vegetation indices layers

import os
import sys
import rioxarray as rxr
import streamlit as st
from streamlit.web import cli as stcli
from rasterio.io import MemoryFile

from pycode.utils import gis

RGB = rxr.open_rasterio("test/RGB.tif")
# R = rxr.open_rasterio("test/R.tif")
G = rxr.open_rasterio("test/G.tif")
B = rxr.open_rasterio("test/B.tif")
RE = rxr.open_rasterio("test/RE.tif")
NIR = rxr.open_rasterio("test/NIR.tif")
DSM = rxr.open_rasterio("test/DSM.tif")
DTM = rxr.open_rasterio("test/DTM.tif")

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
    resized_img = {}
    if band != ref:
        exec(f"{band} = gis.layer_match({band}, {ref})")
        # print(f"{band} : ", eval(f"{band}.shape"))

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
    
