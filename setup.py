import os
import sys
import subprocess
from pathlib import Path

pyenv_dir = Path(sys.executable).parent.parent
pkgs = os.listdir(os.path.join(pyenv_dir, "Lib", "site-packages"))

if not os.path.exists(os.path.join(pyenv_dir.parent, ".streamlit")):
    os.mkdir(".streamlit")

def pipwin_install(pkgs_name):
    if [i for i in pkgs if i.startswith(pkgs_name) is None]:
        subprocess.check_call([sys.executable, '-m', 'pipwin', 'install', pkgs_name])
    else:
        print(f"{pkgs_name} already exists.")

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pipwin', 'wheel'])
pipwin_install("GDAL")
pipwin_install("Fiona")

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'geopandas', 'rioxarray'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pycaret[full]'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'streamlit'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-contrib-python', 'scikit-image'])

# process output with an API in the subprocess module:
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
