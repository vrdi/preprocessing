import pandas
from fuzzywuzzy import process


def search_for_match(precinct, index, county, gdf, column="PRECINCT_N"):
    choices = gdf[gdf["CTYNAME"] == county][column]
    try:
        name, rating, match_index = process.extractOne(precinct, choices)
    except Exception:
        return None
    return {
        "index": index,
        "county": county,
        "precinct": precinct,
        "rating": rating,
        "match_index": match_index,
    }


def find_matches(df, gdf, column="PRECINCT_N"):
    assert set(df["COUNTY"]) == set(gdf["CTYNAME"])
    counties = set(df["COUNTY"])
    records = [
        search_for_match(precinct, index, county, gdf=gdf, column=column)
        for county in counties
        for index, precinct in df[df["COUNTY"] == county]["PRECINCT"].items()
    ]
    records = [record for record in records if record is not None]
    matches = pandas.DataFrame.from_records(records)
    matches["match_value"] = matches["match_index"].map(gdf[column])
    return matches
