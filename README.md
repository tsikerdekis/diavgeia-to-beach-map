# diavgeia-to-beach-map

A collection of scripts to read pdfs from from diavgeia.gov.gr and create a table and other info on licenced businesses that have rights to operate on the Greek beaches.

The export.json needs to be obtained from diavgeia.gov.gr using:
```https://diavgeia.gov.gr/luminapi/api/search/export?q=q:[%22%CE%B1%CE%B4%CE%B5%CE%B9%CE%B1%22,%22%CE%B1%CF%80%CE%BB%CE%B7%CF%82%22,%22%CF%87%CF%81%CE%B7%CF%83%CE%B7%CF%82%22,%22%CE%B1%CE%B9%CE%B3%CE%B9%CE%B1%CE%BB%CE%BF%CF%85%22]&fq=decisionType:%22%CE%A0%CE%91%CE%A1%CE%91%CE%A7%CE%A9%CE%A1%CE%97%CE%A3%CE%97%20%CE%A7%CE%A1%CE%97%CE%A3%CE%97%CE%A3%20%CE%A0%CE%95%CE%A1%CE%99%CE%9F%CE%A5%CE%A3%CE%99%CE%91%CE%9A%CE%A9%CE%9D%20%CE%A3%CE%A4%CE%9F%CE%99%CE%A7%CE%95%CE%99%CE%A9%CE%9D%22&fq=organizationUid:%226140%22&sort=relative&wt=json
```

Then dl_pdfs.py will get the pdfs, parse_pdf.py will parse the pdfs and extract the data, then output them in dat.json. In turn this json is read by index.html.

# TODO

* Add a map with the locations of the businesses (possibly use OCR since recent records include coordinates)
* Display on map. Bing is currently free and supports this.
* get_lanlon.py does not work for Greek locations. Probably will remain an inactive script.
* testing folder contains map experiments

# Contribute

If you need help or want to contribute, please contact me at: https://michael.tsikerdekis.com