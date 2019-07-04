#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas
import geopandas
import matplotlib.pyplot as plt
from fuzzywuzzy import process


# In[37]:


df = pandas.read_csv("./GA_precincts_with_absentee.csv")


# In[38]:


gdf = geopandas.read_file("./shapefiles/GA_precincts16.shp")


# In[70]:


def search_for_match(precinct, county, gdf=gdf, column="PRECINCT_N"):
    choices = gdf[gdf["CTYNAME"] == county][column]
    name, rating, index = process.extractOne(precinct, choices)
    return {"county": county, "precinct": precinct, "rating": rating, "match_index": index}


# In[76]:


def find_matches(df, gdf, column="PRECINCT_N"):
    assert set(df["COUNTY"]) == set(gdf["CTYNAME"])
    counties = df["COUNTY"].unique()
    records = [
        search_for_match(precinct, county, gdf=gdf, column=column)
        for county in counties
        for precinct in df[df["COUNTY"] == county]["PRECINCT"]
    ]
    matches = pandas.DataFrame.from_records(records)
    matches["match_value"] = matches["match_index"].map(gdf[column])
    return matches


# In[77]:


matches = find_matches(df, gdf)


# In[119]:


matches.rating.hist()


# In[120]:


len(df) - len(gdf)


# ## The problem counties
# 
# ### Counties with bad match scores:
# 
# - Bacon
# - Bleckley ✅
# - Chatham
# - Chattahoochee
# - Clarke
# - Crawford ✅
# - Rockdale
# - Spalding ⚠️
# - Taylor
# 
# ### Counties with different numbers of precincts:
# 
# - Bibb 1
# - Chattooga 1
# - Columbia 3
# - Crawford 3 ✅
# - DeKalb 3
# - Effingham 2
# - Fayette 2
# - Forsyth 4
# - Fulton 1
# - Gwinnett 1
# - Henry 1
# - Lowndes 2
# - Muscogee 2
# - Newton 2
# - Pickens 1
# 

# In[121]:


for county in counties:
    difference = len(df[df["COUNTY"] == county]) - len(gdf[gdf["CTYNAME"] == county])
    if difference > 0:
        print(county, difference)


# In[127]:


average_by_county = matches.groupby("county").rating.mean()
average_by_county[average_by_county < 90]


# ### Crawford

# In[131]:


crawford = df[df["COUNTY"] == "Crawford"]
crawford_gdf = gdf[gdf["CTYNAME"] == "Crawford"]


# In[129]:


columns_to_aggregate = [
    'PRES16D', 'PRES16D_AB', 'PRES16D_AD',
    'PRES16D_ED', 'PRES16D_PR', 'PRES16L', 'PRES16L_AB', 'PRES16L_AD',
    'PRES16L_ED', 'PRES16L_PR', 'PRES16R', 'PRES16R_AB', 'PRES16R_AD',
    'PRES16R_ED', 'PRES16R_PR', 'REG_VOTE'
]


# It looks like the shapefile has merged the "COUNTY" and "CITY" parts of each of precincts 1B, 2, and 3 into singular precincts 1B, 2, and 3.

# In[138]:


merged_crawford_precincts = crawford.groupby(crawford["PRECINCT"].apply(lambda s: s.split()[0])).sum()
merged_crawford_precincts


# In[140]:


merged_crawford_precincts.reset_index(inplace=True)
merged_crawford_precincts["COUNTY"] = "Crawford"


# In[143]:


assert set(merged_crawford_precincts.columns) == set(df.columns)


# In[146]:


merged_crawford_precincts.to_csv("./merged/crawford.csv", index=False)


# ### Bleckley

# In[147]:


df[df["COUNTY"] == "Bleckley"]


# In[148]:


gdf[gdf["CTYNAME"] == "Bleckley"]


# This one is just a single precinct in both datasets, and the vote totals match, so I feel good about matching it.

# ### Spalding

# In[149]:


df[df["COUNTY"] == "Spalding"]


# In[150]:


gdf[gdf["CTYNAME"] == "Spalding"]


# This one is wild! I suppose our next course of action is try and figure out where these landmarks ("SENIOR CENTER", "CITY PARK") are and then match that to our precinct geometries. We could also talk to the county for more information.

# ### Bacon

# In[151]:


df[df["COUNTY"] == "Bacon"]


# In[152]:


gdf[gdf["CTYNAME"] == "Bacon"]


# ## Errors in the data concatenation
# 
# It looks like we read in some of the counties' data wrong. This might be the cause of these discrepancies in the vote totals between our two datasets:

# In[168]:


errors_r = (df.groupby("COUNTY")["PRES16R"].sum() - gdf["PRES16R"].astype(int).groupby(gdf["CTYNAME"]).sum())


# In[169]:


errors_r[errors_r != 0]


# In[177]:


errors_d = (df.groupby("COUNTY")["PRES16D"].sum() - gdf["PRES16D"].astype(int).groupby(gdf["CTYNAME"]).sum())
errors_d[errors_d != 0]


# You can see that, at least for Chatham, the names of the precincts were too long and extended all the way to the first vote totals without a whitespace separator:

# In[174]:


df[df["COUNTY"] == "Chatham"]["PRECINCT"]


# That parsing error is throwing off the vote totals. :(
