# coding: utf-8
import xml.etree.ElementTree as ET
from collections import defaultdict
import re, codecs, json
from pymongo import MongoClient

p_3 = re.compile(r'^([a-z|_]+):([a-z|_]+):([a-z|_]+)$')
p_2 = re.compile(r'^([a-z|_]+):([a-z|_]+)$')
p_1 = re.compile(r'^([a-z|_]+)$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# UPDATE THIS VARIABLE
mapping = { "St.": "Street",
            "St": "Street",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Expwy": "Expressway",
            }

def update_name(name, mapping):
    for key,value in mapping.items():
        if name.find(key) != -1:
            name = name.replace(key,value)
            break

    return name

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
	node = defaultdict(dict)
	if element.tag=='node' or element.tag=='way':
		node['type_id'] = element.tag
		node['pos'] = list()
		node['created'] = dict()
		for key in element.attrib:
			if key in CREATED:
				node['created'][key] = element.attrib[key]
				continue
			if key in ['lat','lon']:
				node['pos'].append(float(element.attrib['lat']))
				node['pos'].append(float(element.attrib['lon']))
				continue
			node[key] = element.attrib[key]
		if len(node['pos'])==4:
			del node['pos'][2:]
		else:
			del node['pos']
		# get tag info
		for elem in element.iter('tag'):
			k = elem.attrib['k']
			v = elem.attrib['v']

			# update name/street
			if k in ["name","name:en", "addr:street"]:
				v = update_name(v, mapping)

			# ignore problem chars
			if problemchars.search(k):
				continue
			# match ***:***:***
			if p_3.search(k):
				r = p_3.search(k)
				s1 = r.group(1)
				s2 = r.group(2)
				s3 = r.group(3)
				if type(node[s1])!=dict:
					temp = node[s1]
					node[s1] = defaultdict(dict)
					node[s1]['value'] = temp
				elif s2 in node[s1].keys() and type(node[s1][s2])!=str:
					node[s1][s2][s3] = v
				elif s2 in node[s1].keys() and type(node[s1][s2])==str:
					temp = node[s1][s2]
					node[s1][s2] = dict()
					node[s1][s2]['value'] = temp
				else:
					node[s1][s2] = dict()
					node[s1][s2][s3] = v
				continue
			# match ***:***
			if p_2.search(k):
				r = p_2.search(k)
				s1 = r.group(1)
				s2 = r.group(2)
				if type(node[s1])==str:
					temp = node[s1]
					node[s1] = defaultdict(dict)
					node[s1]['value'] = temp
					node[s1][s2] = v
				else:
					node[s1][s2] = v
				continue
			# match ***
			if p_1.search(k):
				r = p_1.search(k)
				s1 = r.group()
				node[s1] = v
				continue
		if element.tag=='way':
			node['node_refs'] = list()
			for elem in element.iter('nd'):
				node['node_refs'].append(elem.attrib['ref'])
	return node

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            # insert db
            # if len(el)!=0:
            # 	db.osm_shenzhen.insert(el)
            # else:
            # 	continue
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+",\n")
                else: 
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
	client = MongoClient("mongodb://localhost:27017")
	db = client.examples
	data = process_map('shenzhen_china.osm', True)