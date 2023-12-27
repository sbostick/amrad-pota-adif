Overview
--------

I wrote this to convert yaml POTA logs (inputs) to ADIF files (output)
for upload to https://pota.app. It gets the job done for now.

See Makefile for invocation example.
Entry point is src/main.py.

Typically I use pen and paper to log pota contacts. Then I manually enter the
data into the "HAMRS" app (running Apple MBP-M1). Then I export the POTA log
to an ADI file for upload.

HAMRS seems to be [broken on this platform][1].

[1]: https://community.hamrs.app/t/gear-menus-not-working-on-mac/4043


References
----------

IDIF Specification
* https://www.adif.org/305/ADIF_305.htm#QSO_Fields

QRZ Lookups
* https://www.qrz.com/docs/logbook/QRZLogbookAPI.html
* https://logbook.qrz.com/api
* https://xml.qrz.com/xcheck
* https://www.qrz.com/XML/current_spec.html  (see section "Callsign Lookups")

Python XML Parsing and Traversal
* https://docs.python.org/3/library/xml.etree.elementtree.html
* https://github.com/martinblech/xmltodict

Python Jinja2
* https://palletsprojects.com/p/jinja/
