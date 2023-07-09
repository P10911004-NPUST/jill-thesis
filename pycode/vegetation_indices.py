# Generate vegetation indices layers

import os
import sys
import rioxarray as rxr
import streamlit as st
from streamlit.web import cli as stcli
from rasterio.io import MemoryFile

from utils import gis
from utils.streamlit_config import *

vi_requirements = {
        'CSM': ['DSM', 'DTM'],
        'NDVI': ['NIR', 'R'],
        'DATT': ['NIR', 'RE', 'R'],
        'GNDVI': ['NIR', 'G'],
        'NDTI': ['R', 'G'],
        'NExG': ['R', 'G', 'B'],
        'NGRDI': ['R', 'G'],
        'VARI': ['R', 'G', 'B'],
        }

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
    DSM_filename = st.selectbox("DSM band: ", options=['None'], disabled=True)
    DTM_filename = st.selectbox("DTM band: ", options=['None'], disabled=True)
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
    DSM_filename = st.selectbox("DSM band: ", options=filenames)
    DTM_filename = st.selectbox("DTM band: ", options=filenames)

    if RGB_filename != "None":
        # [lst.index(str) - 1] is to match the index length of the uploaded_files
        RGB_file = uploaded_files[filenames.index(RGB_filename) - 1]
        RGB = gis.read_tif(RGB_file)

    if R_filename != "None":
        R_file = uploaded_files[filenames.index(R_filename) - 1]
        R = gis.read_tif(R_file).squeeze()

    if G_filename != "None":
        G_file = uploaded_files[filenames.index(G_filename) - 1]
        G = gis.read_tif(G_file).squeeze()

    if B_filename != "None":
        B_file = uploaded_files[filenames.index(B_filename) - 1]
        B = gis.read_tif(B_file).squeeze()

    if RE_filename != "None":
        RE_file = uploaded_files[filenames.index(RE_filename) - 1]
        RE = gis.read_tif(RE_file).squeeze()

    if NIR_filename != "None":
        NIR_file = uploaded_files[filenames.index(NIR_filename) - 1]
        NIR = gis.read_tif(NIR_file).squeeze()

    if DSM_filename != "None":
        DSM_file = uploaded_files[filenames.index(DSM_filename) - 1]
        DSM = gis.read_tif(DSM_file).squeeze()
    
    if DTM_filename != "None":
        DTM_file = uploaded_files[filenames.index(DTM_filename) - 1]
        DTM = gis.read_tif(DTM_file).squeeze()

    if 'RGB' in globals():
        if RGB.shape[0] not in [3, 4]:
            st.code("RGB image should has at least 3 bands")
        else:
            for rgb in ['R', 'G', 'B']:
                i = 0
                if rgb not in globals():
                    exec(f"{rgb} = RGB[{i}]")
                i += 1

    collected_bands = [i for i in ['R', 'G', 'B', 'RE', 'NIR', 'DSM', 'DTM'] if i in globals()]
    
    # Get the smallest bands in area for resizing the others
    if len(collected_bands) > 1:
        ref = collected_bands[0]
        for band in collected_bands:
            ref_dim = eval(f"{ref}.shape[-2] * {ref}.shape[-1]")
            band_dim = eval(f"{band}.shape[-2] * {band}.shape[-1]")
            if band_dim < ref_dim:
                ref = band

        for band in collected_bands:
            if band != ref:
                pass
                # r = gis.layer_match(R, globals()[ref])
                # globals()[band] = gis.layer_match(globals()[band], globals()[ref])

        if R is not None and DTM is not None:
            r = gis.layer_match(R, DTM)
            st.code(DTM.crs)
            st.code(r.crs)
            

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
        sys.exit(stcli.main())
except:
    pass
