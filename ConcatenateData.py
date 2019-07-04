#!/usr/bin/env python
# coding: utf-8

# # Preparing the data

# ## Concatenate all the data

# In[1]:


import pandas


# In[69]:


def check_order_of_candidates(line):
    words = [s.lower() for s in line.split()]
    trump_index = words.index("trump")
    clinton_index = words.index("clinton")
    johnson_index = words.index("johnson")
    return (trump_index < clinton_index) and (clinton_index < johnson_index)

def find_row_range(filename):
    try:
        with open(filename) as f:
            for i, line in enumerate(f):
                if "TRUMP" in line:
                    assert check_order_of_candidates(line)
                if "President" in line:
                    start = i + 2
                if "Totals:" in line:
                    stop = i - 1
                    return start, stop - start
    except Exception as e:
        print(filename)
        print(e)
        assert False


# In[ ]:


column_suffixes = {
    "Election Day": "_ED",
    "Absentee by Mail": "_AB",
    "Absentee By Mail": "_AB",
    "Advance in Person": "_AD",
    "Advance In Person": "_AD",
    "Provisional": "_PR",
    "Choice Total": "",
}

column_map = {
    "Registered Voters": "REG_VOTE",
    "Precinct": "PRECINCT",
}

candidate_map = {
    "": "PRES16R",
    ".1": "PRES16D",
    ".2": "PRES16L"
}

for identifier, candidate_col in candidate_map.items():
    for col, suffix in column_suffixes.items():
        column_map[col + identifier] = candidate_col + suffix


# In[147]:


def sum_advance_columns(df):
    num_columns = 0
    cols = [col for col in df.columns if "advance in person" in col.lower() and "." not in col]
    if len(cols) > 1:
        advance_columns_map = {
            suffix: [f"{col}{suffix}" for col in cols]
            for suffix in ["", ".1", ".2"]
        }
        for suffix, advance_columns in advance_columns_map.items():
            df["Advance in Person" + suffix] = df[advance_columns].sum(axis=1)
        columns_to_drop = [col for cols in advance_columns_map.values() for col in cols]
        for suffix in advance_columns_map:
            if "Advance in Person" + suffix in columns_to_drop:
                columns_to_drop.remove("Advance in Person" + suffix)
        return df.drop(columns_to_drop, axis="columns")
    return df


# In[148]:


def read_county_txt(county):
    filename = f"./data/{county}/detail.txt"
    skiprows, nrows = find_row_range(filename)
    df = pandas.read_csv(filename, sep="\s\s+", skiprows=skiprows, nrows=nrows, engine="python")
    df = sum_advance_columns(df)
    result = df.rename(column_map, axis="columns").drop("Total", axis="columns")
    result["COUNTY"] = county
    return result


# In[149]:


counties = os.listdir("./data/")
county_dataframes = [read_county_txt(county) for county in counties]


# In[150]:


columns = set(county_dataframes[0].columns)

for df in county_dataframes:
    if set(df.columns) != columns:
        print(columns - set(df.columns))


# In[151]:


df = pandas.concat(county_dataframes, ignore_index=True)


# In[48]:


new_names = {"Ben_Hill": "Ben Hill", "Jeff_Davis": "Jeff Davis"}
df["COUNTY"] = df["COUNTY"].apply(lambda p: new_names.get(p, p))


# In[49]:


df.COUNTY.unique()


# In[56]:


df.to_csv("./GA_precincts_with_absentee.csv", index=False)


# ## Bring counties into alignment

# In[51]:


import geopandas


# In[52]:


gdf = geopandas.read_file("./shapefiles/GA_precincts16.shp")


# In[53]:


new_names = {"CHATTOOGA": "Chattooga"}
gdf["CTYNAME"] = gdf["CTYNAME"].apply(lambda n: new_names.get(n, n))


# In[54]:


assert set(gdf["CTYNAME"]) == set(df["COUNTY"])


# In[55]:


gdf.to_file("./shapefiles/GA_precincts16.shp")

