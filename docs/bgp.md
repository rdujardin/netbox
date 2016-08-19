# BGP extension

BGP is a Netbox extension developed for IXPs. It allows to automate BGP routes filtering, by storing all the customers ASNs in database with their routes (prefixes) declared in IRRs.

When you add or update an ASN object, if the field *Lock AS SET* is false, data about the ASN are automatically updated : WHOIS requests are sent through the port 53 to the NTT and RIPE databases in order to get the AS Name and the AS SETs v4 and v6 the customer declared exported to you (you can set your ASN in BGP_SELF_ASN in configuration.py). Then, the extension uses the software *bgpq3* (it must be installed on the server in order that the extension works correctly, its path can be set in BGP_BGPQ3_PATH in configuration.py) to get the routes declared by the AS or by its declared AS-SET if available, in both IPv4 and IPv6.

If these requests fail, the fields are set empty.

If you don't want data about an ASN to be automatically loaded, set its field *Lock AS SET* as true. The AS Name will be automatically loaded, but not the AS SETs nor the prefixes.

See the source code of the automatically-loading at bgp/models.py for more detail.

