

# import pyflwdir, some dependencies and convenience methods
import numpy as np
import rasterio
import pyflwdir
import matplotlib.pyplot as plt
import time
import sys

start = time.time()
with rasterio.open(sys.argv[1],"r") as src:
    elevtn = src.read(1)
    nodata = src.nodata
    transform = src.transform
    crs = src.crs
    extent = np.array(src.bounds)[[0, 2, 1, 3]]
    latlon = src.crs.is_geographic
    prof = src.profile

# read and parse flow direciton data
with rasterio.open(sys.argv[2], "r") as src:
    flwdir = src.read(1)
    crs = src.crs
    extent = np.array(src.bounds)[[0, 2, 1, 3]]
    flw = pyflwdir.from_array(
        flwdir,
        ftype="d8",
        transform=src.transform,
        latlon=crs.is_geographic,
        cache=True,
    )

# first we derive the upstream area map
uparea = flw.upstream_area("km2")

# HAND based on streams defined by a minimal upstream area of 1000 km2
hand = flw.hand(drain=uparea > 1000, elevtn=elevtn)
end = time.time()
print(end - start)
# plot
ax = plt.plot(title="Height above nearest drain (HAND)")
im = plt.imshow(
    np.ma.masked_equal(hand, -9999),
    extent=extent,
    cmap="gist_earth_r",
    alpha=0.5,
    vmin=0,
    vmax=50,
)
plt.colorbar(im)

fig = plt.gcf()
cax = fig.add_axes([0.82, 0.37, 0.02, 0.12])
fig.colorbar(im, cax=cax, orientation="vertical")
cax.set_ylabel("HAND [m]")
plt.savefig(sys.argv[3])
plt.show()





