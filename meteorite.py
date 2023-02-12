import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


data = pd.read_csv('meteorite-landings.csv')


# Remove invalid coordinates
data = data[(data.reclat != 0.0) & (data.reclong != 0.0)]
data.info()

# Clean up relicts
valids = data.groupby('nametype').get_group('Valid').copy()
valids.dropna(inplace=True)
valids.info()


# Visualise by geographic location
map = Basemap(projection='cyl')
map.drawmapboundary(fill_color='w')
map.drawcoastlines(linewidth=0.5)
map.drawmeridians(range(0, 360, 20),linewidth=0.1)

# Plot equator, tropics & polar circles
map.drawparallels([-66.56083,-23.5,0.0,23.5,66.56083], linewidth=0.6)
x, y = map(valids.reclong,valids.reclat)
map.scatter(x, y, marker='.',alpha=0.25,c='green',edgecolor='None')
plt.title('Meteorite impacts', fontsize=15)


# Add heatmap
h = plt.hist2d(valids.reclong,valids.reclat,bins=(np.arange(-180,182,2),np.arange(-90,92,2)))
X,Y = np.meshgrid(h[1][:-1]+1.0,h[2][:-1]+1.0)

map = Basemap(projection='cyl')
map.drawmapboundary(fill_color='w')
map.drawcoastlines(linewidth=0.6)
map.drawmeridians(range(0, 360, 20),linewidth=0.1)
map.drawparallels([-66.56083,-23.5,0.0,23.5,66.56083], linewidth=0.6)

data_interp, x, y = map.transform_scalar(np.log10(h[0].T+0.1), X[0], Y[:,0], 360, 360, returnxy=True)
map.pcolormesh(x, y, data_interp,cmap='hot_r')
map.colorbar()
plt.title('Meteorite impact heatmap', fontsize=15)


# Compare meteorites with and without eyewitnesses
v_fell = valids.groupby('fall').get_group('Fell')
v_found = valids.groupby('fall').get_group('Found')

plt.figure(figsize=(10,10))

plt.subplot(211)
h = plt.hist2d(v_fell.reclong,v_fell.reclat,bins=(np.arange(-180,182,2),np.arange(-90,92,2)))
X,Y = np.meshgrid(h[1][:-1]+1.0,h[2][:-1]+1.0)

map = Basemap(projection='cyl')
map.drawmapboundary(fill_color='w')
map.drawcoastlines(linewidth=0.6)
map.drawmeridians(range(0, 360, 20),linewidth=0.1)
map.drawparallels([-66.56083,-23.5,0.0,23.5,66.56083], linewidth=0.6)

data_interp, x, y = map.transform_scalar(np.log10(h[0].T+0.1), X[0], Y[:,0], 360, 360, returnxy=True)
map.pcolormesh(x, y, data_interp,cmap='hot_r')
map.colorbar()
plt.title('Heatmap of meteorites seen falling', fontsize=15)

plt.subplot(212)
h = plt.hist2d(v_found.reclong,v_found.reclat,bins=(np.arange(-180,182,2),np.arange(-90,92,2)))
X,Y = np.meshgrid(h[1][:-1]+1.0,h[2][:-1]+1.0)

map = Basemap(projection='cyl')
map.drawmapboundary(fill_color='w')
map.drawcoastlines(linewidth=0.6)
map.drawmeridians(range(0, 360, 20),linewidth=0.1)
map.drawparallels([-66.56083,-23.5,0.0,23.5,66.56083], linewidth=0.6)

data_interp, x, y = map.transform_scalar(np.log10(h[0].T+0.1), X[0], Y[:,0], 360, 360, returnxy=True)
map.pcolormesh(x, y, data_interp,cmap='hot_r')
map.colorbar()
plt.title('Meteorites found', fontsize=15)


# Compare impact sighting with population density
map = Basemap(projection='cyl',resolution='i')
#map.warpimage(image='http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si=875430&cs=rgb&format=JPEG&width=1440&height=720')
map.scatter(v_found.reclong,v_found.reclat,marker='.',alpha=0.5,edgecolor='None',color='m')

plt.title('Mapping meteorites found with population density', fontsize=15)

map = Basemap(projection='cyl',resolution='i')
#map.warpimage(image='http://neo.sci.gsfc.nasa.gov/servlet/RenderData?si=875430&cs=rgb&format=JPEG&width=1440&height=720')
map.scatter(v_fell.reclong,v_fell.reclat,marker='.',alpha=0.5,edgecolor='None',color='k')

plt.title('Mapping meteorite impacts sighted with population density', fontsize=15)


# Visualising by year of impact
plt.subplot(211)
valids.year.hist(bins=np.arange(1900,2014,1),figsize=(8,7))
plt.title('Discoveries per year 1900-2013')
plt.xlim(1900,2014)

plt.subplot(212)
valids.year.hist(bins=np.arange(1900,2023,10),figsize=(8,7))
plt.title('Discoveries per decade 1900-2013')
plt.xlim(1900,2014)
