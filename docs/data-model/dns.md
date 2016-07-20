The DNS component of NetBox deals with the management of DNS zones.

# Zones

A zone corresponds to a zone file in a DNS server, it stores the SOA (Start Of Authority) record and other records that are stored as Record objects.

As zones are readable through the REST API, it is possible to write some external script which automatically generates zone files for a DNS server,
this feature is not directly provided by NetBox though.

---

# Record

Each Record object represents a DNS record, i.e. a link between a hostname and a resource, which can be either an IP address or a text value,
for instance another hostname if the record is of CNAME type.

Records must be linked to an existing zone, and hold either an existing IP address link or a text value.

Reverse DNS is not supported by Record objects, but by the "Host Name" field in IP addresses.
