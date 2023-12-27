Overview
--------

I wrote this app to convert from a yaml POTA input log to an ADIF file
for upload to https://pota.app.

Normally I use pen and paper to log my pota contacts, then input into HAMRS
app running on an M1 Macbook Pro. Then export the POTA logbook to an ADI file
for upload to https://pota.app.

HAMRS is currently [broken on this platform][1].

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
