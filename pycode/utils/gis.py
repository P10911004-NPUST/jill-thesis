import rioxarray as rxr
from rasterio.io import MemoryFile

def read_memory(memoryfile):
    with MemoryFile(memoryfile) as mf:
        with mf.open() as ds:
            data_array = rxr.open_rasterio(ds)
    return data_array.squeeze()

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
    return ret

def print_raster(raster):
    print(
        f"shape: {raster.rio.shape}\n"
        f"resolution: {raster.rio.resolution()}\n"
        f"bounds: {raster.rio.bounds()}\n"
        f"sum: {raster.sum().item()}\n"
        f"CRS: {raster.rio.crs}\n"
    )