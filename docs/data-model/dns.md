The DNS component of NetBox deals with the management of DNS zones.

# Zones

A zone corresponds to a zone file in a DNS server, it stores the SOA (Start Of Authority) record and other records that are stored as Record objects.

The SOA Serial field is automatically created and updated each time something changes in the zone, i.e. each time you edit IP addresses or records
belonging to the zone, or the zone itself. It's in the following format : YYYYMMDDN with Y the year, M the month, D the day and N a counter.

Every zone can be exported as a zone file in BIND format, directly readable by a DNS server. As zones are readable through the REST API,
with a field containing their BIND format, it is possible to write an external script which automatically updates a DNS server
configuration from the Netbox database.

---

# Record

Each Record object represents a DNS record, i.e. a link between a hostname and a resource, which can be either an IP address or a text value,
for instance another hostname if the record is of CNAME type.

Records must be linked to an existing zone, and hold either an existing IP address link or a text value.

Reverse DNS is not supported by Record objects, but by the "Host Name" field in IP addresses.
