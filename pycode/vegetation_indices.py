''' Generate vegetation indices layers '''
# streamlit run pycode\vegetation_indices.py
# streamlit config show > .streamlit\config.toml
# raise upload file size limits to 10 GB
# change [server] param in config.toml --> maxmaxUploadSize = 10000

import os
import tempfile
import numpy as np
import pandas as pd
import cv2
import skimage as ski
import rioxarray as rxr
import geopandas as gpd
import streamlit as st
import xarray as xr
from rasterio.io import MemoryFile


def read_tif(tifFile):
    with MemoryFile(tifFile) as mf:
        with mf.open() as ds:
            data_array = rxr.open_rasterio(ds)
    return data_array

def layer_match(lyr, ref):
    ret = lyr.rio.reproject_match(ref)
    ret = ret.assign_coords({
        'x': ref.x,
        'y': ref.y
    })
    return ref


st.markdown("""
<style>
    @font-face {
    font-family: 'HarmonyOS_Sans_Bold';
    font-style: normal;
    font-weight: 400;
    src: url(https://github.com/P10911004-NPUST/pycaret/tree/main/fonts/HarmonyOS_Sans/HarmonyOS_Sans/HarmonyOS_Sans_Bold.ttf) format('ttf');
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
    html, body, [class*="css"]  {
    font-family: 'HarmonyOS_Sans_Bold';
    font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("TIF files", type=['tif', 'tiff'], accept_multiple_files=True)
if len(uploaded_files) != 0:
    st.success(f"{len(uploaded_files)} files successfully uploaded", icon="✅")

c11, c12 = st.columns([5, 2])

if len(uploaded_files) == 0:
    RGB_filename = st.selectbox("RGB band: ", options=['None'], disabled=True)
    R_filename = st.selectbox("R band: ", options=['None'], disabled=True)
    G_filename = st.selectbox("G band: ", options=['None'], disabled=True)
    B_filename = st.selectbox("B band: ", options=['None'], disabled=True)
    RE_filename = st.selectbox("RE band: ", options=['None'], disabled=True)
    NIR_filename = st.selectbox("NIR band: ", options=['None'], disabled=True)
else:
    filenames = [file.name for file in uploaded_files]
        # After inserting a string, the length of filenames is not matching with uploaded_files
        # this can raise error during indexing uploaded_files with the filenames index.
    filenames.insert(0, 'None')

    RGB_filename = st.selectbox("RGB band: ", options=filenames)
    R_filename = st.selectbox("R band: ", options=filenames)
    G_filename = st.selectbox("G band: ", options=filenames)
    B_filename = st.selectbox("B band: ", options=filenames)
    RE_filename = st.selectbox("RE band: ", options=filenames)
    NIR_filename = st.selectbox("NIR band: ", options=filenames)

    if RGB_filename != "None":
        # [lst.index(str) - 1] is to match the index length of the uploaded_files
        RGB_file = uploaded_files[filenames.index(RGB_filename) - 1]
        RGB = read_tif(RGB_file) 
        # c12.markdown(f"\n RGB(Depth, Y, X): {RGB.shape}")

    if R_filename != "None":
        R_file = uploaded_files[filenames.index(R_filename) - 1]
        R = read_tif(R_file)

    if G_filename != "None":
        G_file = uploaded_files[filenames.index(G_filename) - 1]
        G = read_tif(G_file)

    if B_filename != "None":
        B_file = uploaded_files[filenames.index(B_filename) - 1]
        B = read_tif(B_file)

    if RE_filename != "None":
        RE_file = uploaded_files[filenames.index(RE_filename) - 1]
        RE = read_tif(RE_file)

    if NIR_filename != "None":
        NIR_file = uploaded_files[filenames.index(NIR_filename) - 1]
        NIR = read_tif(NIR_file)
st.divider()
        

    # st.write(f"(Depth, X, Y): {RGB.shape}")
    # st.write(f"(Depth, X, Y): {R.shape}")
    # st.write(f"(Depth, X, Y): {G.shape}")
    # st.write(f"(Depth, X, Y): {B.shape}")
    # st.write(f"(Depth, X, Y): {RE.shape}")
    # st.write(f"(Depth, X, Y): {NIR.shape}")

# if RGB is not None:
#     RGB_ = read_tif(RGB)
#     R_ = RGB_[0, :, :]
#     G_ = RGB_[1, :, :]
#     B_ = RGB_[2, :, :]
#     with c12:
#         c11.markdown(f"RGB.shape: {RGB_.shape}\nName: {RGB.name}")

# if R is not None:
#     R_ = read_tif(R)[0, :, :]
#     with c22:
#         st.write(f"R.shape: {R_.shape}")

# if G is not None:
#     G_ = read_tif(G)[0, :, :]
    

# if B is not None:
#     B_ = read_tif(B)[0, :, :]
    

# if RE is not None:
#     RE_ = read_tif(RE)[0, :, :]
#     R_ = layer_match(R_, RE_)
#     G_ = layer_match(G_, RE_)
#     B_ = layer_match(B_, RE_)

# if NIR is not None:
#     NIR_ = read_tif(NIR)[0, :, :]
#     R_ = layer_match(R_, NIR_)
#     G_ = layer_match(G_, NIR_)
#     B_ = layer_match(B_, NIR_)
#     RE_ = layer_match(B_, RE_)



# streamlit run pycode\vegetation_indices.py
