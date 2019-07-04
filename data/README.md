Each county is in a separate folder by county name.

**detail.xls** is actually an Excel XML file. At the moment, we know of no Python Excel XML readers. Standard Excel libraries like xlrd do not work. The only way to read in appears to be to use an XML parser and extract the desired worksheet and data. Alternatively, the Excel files can be opened manually and worksheet "2" (2016 Presidenial elections) can be exported to CSV. (Note that "2" is a name, not an index). If we want to analyze any other elections, automation would be better.

**detail.txt** has the same data as **detail.xls** in text form, but not as an easily parsable CSV or TSV. Each worksheet of **detail.xls** (representing one election in 2016) appears as a fixed-width table appended after a gap of four lines. The format appears to be fixed-width but no attempt is made to account for data (precinct names) that overflows the fixed-width limit.

