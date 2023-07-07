# Generate vegetation indices layers

import os
import sys
import rioxarray as rxr
import streamlit as st
from streamlit.web import cli as stcli
from rasterio.io import MemoryFile

from utils import gis
from utils.streamlit_config import *

st.markdown(change_font, unsafe_allow_html=True)
st.markdown(hide_footer, unsafe_allow_html=True)

uploaded_files = st.file_uploader("TIF files", type=['tif', 'tiff'], accept_multiple_files=True)
if len(uploaded_files) != 0:
    st.success(f"{len(uploaded_files)} files successfully uploaded", icon="✅")

collected_bands = []

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
        RGB = gis.read_tif(RGB_file)
        if RGB is not None:
            collected_bands.append('RGB')
        # c12.markdown(f"\n RGB(Depth, Y, X): {RGB.shape}")

    if R_filename != "None":
        R_file = uploaded_files[filenames.index(R_filename) - 1]
        R = gis.read_tif(R_file)
        if R is not None:
            collected_bands.append('R')

    if G_filename != "None":
        G_file = uploaded_files[filenames.index(G_filename) - 1]
        G = gis.read_tif(G_file)
        if G is not None:
            collected_bands.append('G')

    if B_filename != "None":
        B_file = uploaded_files[filenames.index(B_filename) - 1]
        B = gis.read_tif(B_file)
        if B is not None:
            collected_bands.append('B')

    if RE_filename != "None":
        RE_file = uploaded_files[filenames.index(RE_filename) - 1]
        RE = gis.read_tif(RE_file)
        if RE is not None:
            collected_bands.append('RE')

    if NIR_filename != "None":
        NIR_file = uploaded_files[filenames.index(NIR_filename) - 1]
        NIR = gis.read_tif(NIR_file)
        if NIR is not None:
            collected_bands.append('NIR')

    vi_requirements = {
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

    st.divider() 

    st.selectbox("Select VI layer:", vi_options)
    


# streamlit run pycode\vegetation_indices.py
try:
    if __name__ == '__main__':
        sys.argv = ["streamlit", "run", os.path.join("pycode", os.path.basename(__file__))]
        # sys.exit(stcli.main())
        sys.exit(stcli.main())
except:
    pass
