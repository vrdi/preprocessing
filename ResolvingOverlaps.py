#!/usr/bin/env python
# coding: utf-8

# In[1]:


import maup
import geopandas
import matplotlib.pyplot as plt


# In[2]:


ut = geopandas.read_file("https://github.com/mggg-states/UT-shapefiles/raw/master/UT_precincts.zip")


# In[2]:


example = geopandas.read_file("zip://examples/overlaps.zip")


# In[6]:


resolved = maup.resolve_overlaps(example)


# In[17]:


resolved.plot(figsize=(12, 12), edgecolor="#004464", color="#eeeeee")
plt.axis('off')


# In[44]:


maup.adjacencies(example).plot(figsize=(14, 14))


# In[47]:


inters = maup.intersections(example, example, area_cutoff=None)


# In[50]:


non_self_inters = [i != j for i, j in inters.index]
inters = inters[non_self_inters]


# In[55]:


inters[inters.area > 0].plot(figsize=(12, 12), linewidth=5, edgecolor="black")


# In[64]:


inters.loc[[inters.area.idxmax()]].plot(figsize=(14,14))
plt.axis('off')


# In[65]:


polygon = inters[inters.area.idxmax()]


# In[80]:


from shapely.ops import triangulate

triangles = triangulate(polygon, edges=False)


# In[81]:


triangles_geo = geopandas.GeoSeries(triangles)

triangles_geo.centroid.scale(xfact=100).plot(figsize=(10, 10))


# In[87]:


from shapely.geometry import LineString
from shapely import affinity


# In[132]:


import numpy as np
from scipy.spatial import distance_matrix


# In[137]:


plt.matshow(distance_matrix(points, points))


# In[113]:


dist = distance_matrix(points, points)


# In[145]:


max_indices = np.argmax(dist, axis=1)


# In[83]:


line = LineString(triangles_geo.centroid)


# In[88]:


affinity.scale(line, xfact=100)


# In[18]:


example.plot(figsize=(12, 12), edgecolor="#004464", color="#eeeeee")
plt.axis('off')


# In[39]:


resolved


# In[41]:


resolved.loc[13].plot()


# In[ ]:




