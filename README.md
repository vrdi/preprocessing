# README

## Data

Georgia counties report precinct-level election results using a standard format. Provided in both Excel and text format. The data dictionary for presidential elections only:

`COUNTY`: County
`PRECINCT`: Precinct
`PRES16D`: Number of votes for 2016 Democratic presidential candidate
`PRES16D_AB`: Number of absentee votes for 2016 Democratic presidential candidate
`PRES16D_AD`: Number of advance in person votes for 2016 Democratic presidential candidate
`PRES16D_ED`: Number of election day votes for 2016 Democratic presidential candidate
`PRES16D_PR`: Number of provisional votes for 2016 Democratic presidential candidate
`PRES16L`: Number of votes for 2016 Libertarian presidential candidate
`PRES16L_AB`: Number of absentee votes for 2016 Libertarian presidential candidate
`PRES16L_AD`: Number of advance in person votes for 2016 Libertarian presidential candidate
`PRES16L_ED`: Number of election day votes for 2016 Libertarian presidential candidate
`PRES16L_PR`: Number of provisional votes for 2016 Libertarian presidential candidate
`PRES16R`: Number of votes for 2016 Republican presidential candidate
`PRES16R_AB`: Number of absentee votes for 2016 Republican presidential candidate
`PRES16R_AD`: Number of advance in person votes for 2016 Republican presidential candidate
`PRES16R_ED`: Number of elecetion day votes for 2016 Republican presidential candidate
`PRES16R_PR`: Number of provisional votes for 2016 Republican presidential candidate
`REG_VOTE`: Number of registered voters

## ConcatenateData.ipynb

Reads in each of county text files with 2016 presidential data (stored in **data** folder). Parses data, creates data frames, concatenates, outputs **GA_precincts_with_absentee.csv**.

Currently problem in that format is fixed-width *except* if the precinct name is long it is crushed against the second (numeric) column, and the extra spaces shift all subsequent columns to the right.

## MatchingPrecincts.ipynb

**Purpose**: Match voting data from tabular concatenated precinct file to precinct shapefile for all Georgia.

Currently exploratory. Some precinct sums don't match county-level total votes.

## ResolvingOverlaps.ipynb

**Purpose**: Resolve overlap between neighboring geographies in a shapefile. Assumes shapefile should be a lattice (?).


