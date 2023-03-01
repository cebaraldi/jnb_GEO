#!/usr/bin/env python
# coding: utf-8

# # Geographics vs. Projected CRS

# In[1]:


get_ipython().run_line_magic('reset', '-sf')
from pandas import read_csv
#import pandas as pd
import geopandas as gpd


# ## Read the Gauss-Kr&uuml;ger coordinates from a csv file

# In[2]:


# MGI 1901 / Balkans zone 6 EPSG:8678
coord_fn = 'GeoMaks2022-coords.csv'
gk_pd = read_csv(coord_fn, skipinitialspace=True)
gk_pd['label']='Area'
print(gk_pd)


# [UTM Zone](https://mangomap.com/robertyoung/maps/69585/what-utm-zone-am-i-in-#)

# ## Create GeoPandas GeoDataFrame from Pandas Dataframe

# In[3]:


gk_gdf = gpd.GeoDataFrame(
    gk_pd, geometry=gpd.points_from_xy(gk_pd.GKE, gk_pd.GKN))

gk_gdf.plot()
print(gk_gdf)
print(gk_gdf.crs) # None CRS assigned yet


# In[4]:


#gk_gdf.explore()


# ## Set GeoDataFrame to Projected CRS: EPSG:8678,  MGI 1901 / Balkans zone 6

# In[5]:


gk_gdf.crs = "EPSG:8678" 
gk_gdf.crs


# ## Parcel with id 13398 in Loznicko Polije has an area of 3083.2436 square metres

# In[6]:


res = gk_gdf.dissolve('label').convex_hull
res.to_wkt()
print(res)
print(res.area)
res.plot()


# In[7]:


res.explore()


# ## Set GeoDataFrame to Geographic 2D CRS: EPSG:4326, WGS 84

# In[8]:


geo_gdf = gk_gdf.to_crs(epsg='4326') 
#print(geo_gdf.geometry.x)
#print(geo_gdf.geometry.y)
print(geo_gdf)
geo_gdf.crs


# In[9]:


#geo_gdf.explore()


# ## Obtain the ESRI WKT
# [ESRI WKT](https://epsg.io) for EPSG 8678area

# In[10]:


ESRI_WKT = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'


# ## Save the file as an ESRI Shapefile
# 
# [shapfile_extensions](https://webhelp.esri.com)

# In[11]:


#gk_gdf.to_file(filename = 'gk.shp', driver = 'ESRI Shapefile')#, crs_wkt = ESRI_WKT)
geo_gdf.to_file(filename = 'geo.shp', driver = 'ESRI Shapefile')#, crs_wkt = ESRI_WKT)

