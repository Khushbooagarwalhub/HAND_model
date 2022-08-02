# import pyflwdir, some dependencies and convenience methods
import numpy as np
import rasterio
import pyflwdir
import matplotlib.pyplot as plt
import time
import sys

start = time.time()

with rasterio.open(sys.argv[1], "r") as src:
    elevtn = src.read(1)
    nodata = src.nodata
    transform = src.transform
    crs = src.crs
    extent = np.array(src.bounds)[[0, 2, 1, 3]]
    latlon = src.crs.is_geographic
    prof = src.profile

flw = pyflwdir.from_dem(
    data=elevtn,
    nodata=src.nodata,
    transform=transform,
    latlon=latlon,
    outlets="min",
)

d8_data = flw.to_array(ftype="d8")
d8_data

# update data type and nodata value properties which are different compared to the input elevation grid and write to geotif
prof.update(dtype=d8_data.dtype, nodata=247)
with rasterio.open(sys.argv[2], "w", **prof) as src:
    src.write(d8_data, 1)
end = time.time()
print(end - start)
