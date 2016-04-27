#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

"""
The output should be a list of dictionaries in for following format:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

    <tag k="addr:housenumber" v="5158"/>
    <tag k="addr:street" v="North Lincoln Avenue"/>
    <tag k="addr:street:name" v="Lincoln"/>
    <tag k="addr:street:prefix" v="North"/>
    <tag k="addr:street:type" v="Avenue"/>
    <tag k="amenity" v="pharmacy"/>

"tags" should be formatted into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

    <nd ref="305896090"/>
    <nd ref="1719825889"/>

"way" should appear as:

{...
"node_refs": ["305896090", "1719825889"]
...
}
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
postal_codes = re.compile(r'^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
ATTRIB = ["id", "visible", "amenity", "cuisine", "name", "phone"]

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Crescent", "West", "South", "East", "North", "Vista",
            "Gardens", "Circle", "Gate", "Heights", "Park", "Way", "Mews", "Keep", "Westway", "Glenway",
            "Queensway", "Wood", "Path"]

street_mapping = {"Ave": "Avenue",
           "St.": "Street",
           "Rd.": "Road",
           "StreetE": "Street East",
           "Robertoway": "Roberto Way"
           }


# TODO: refactor shape_element


def audit_street_type(street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            # street_types[street_type].add(street_name)
            return update_name(street_name, street_mapping)
    else:
        None

# for st_type, ways in st_types.iteritems():
#     for name in ways:
#         better_name = update_name(name, mapping)
#         print name, "=>", better_name


def update_name(name, mapping):
    for key in mapping.iterkeys():
        if re.search(key, name):
            name = re.sub(key, mapping[key], name)

    return name


def is_street_name(address_key):
    return address_key == 'addr:street'


def audit_postal_type(postal_types, postal_code):
    m = postal_codes.search(postal_code)
    if m:
        postal_code = m.group()
        if postal_code not in expected:
            # TODO: create new or have mapping as null just need new string
            return update_name(postal_code, street_mapping)
        else:
            None


def is_postal_code(address_key):
    return address_key == 'addr:postalcode'


def shape_element(element):

    if element.tag == 'node' or element.tag == 'way':

        # Add empty created dictionary and k/v = type: node/way
        node = {'created': {}, 'type': element.tag}

        # Update pos array with lat and lon
        if 'lat' in element.attrib and 'lon' in element.attrib:
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]

        # Deal with node and way attributes
        for k in element.attrib:

            if k == 'lat' or k == 'lon':
                continue
            if k in CREATED:
                node['created'][k] = element.attrib[k]
            else:
                # Add direct key/value items of node/way
                node[k] = element.attrib[k]

        # Deal with second level tag items
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            v = tag.attrib['v']

            # Search for problem characters in 'k' and ignore them
            if problemchars.search(k):
                # Add to array to print out later
                continue
            elif is_street_name(k):
                v = audit_street_type(v)
            elif is_postal_code(k):
                v = audit_postal_code(v)

            if v is not None:
                node[k] = v

        # TODO: Update audited information here OR do it one item at a time within audit_x_type

        # Add key/value node ref from way
        node_refs = []
        for nd in element.iter('nd'):
            node_refs.append(nd.attrib['ref'])

        if len(node_refs) > 0:
            node['node_refs'] = node_refs

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('sample.osm', False)
    pprint.pprint(data)


if __name__ == "__main__":
    test()
