'''
Created on Jul 10, 2023

@author: FF16GK3
'''
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
# Create a Basemap instance
map = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')

# Draw coastlines, countries, and boundaries
map.drawcoastlines(linewidth=0.5)
map.drawcountries(linewidth=0.5)
map.drawmapboundary(fill_color='lightblue')

# Generate random scalar field data
lats = np.linspace(-90, 90, 100)
lons = np.linspace(-180, 180, 200)
lons, lats = np.meshgrid(lons, lats)
data = np.random.rand(lats.shape[0], lons.shape[1])

# Plot scalar field data
x, y = map(lons, lats)
plt.contourf(x, y, data, cmap='viridis')

# Add colorbar and title
plt.colorbar(label='Scalar Field')
plt.title('Scalar Field Map')

# Create a Basemap instance
map = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')

# Draw coastlines, countries, and boundaries
map.drawcoastlines(linewidth=0.5)
map.drawcountries(linewidth=0.5)
map.drawmapboundary(fill_color='lightblue')

# Generate random vector field data
lats = np.linspace(-90, 90, 20)
lons = np.linspace(-180, 180, 40)
lons, lats = np.meshgrid(lons, lats)
u = np.random.randn(lats.shape[0], lons.shape[1])
v = np.random.randn(lats.shape[0], lons.shape[1])

# Plot vector field data
x, y = map(lons, lats)
map.quiver(x, y, u, v, scale=1000, pivot='middle', color='r')

# Add title
plt.title('Vector Field Map')

# Display the map
plt.show()

