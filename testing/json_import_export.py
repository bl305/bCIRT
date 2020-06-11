#!/usr/bin/env python3
import json

# data1 = {"id":"1","enabled":"True"}
# data2 = [{"id":"1","enabled":"True"},{"id":"1","enabled":"True"}]
data2 = [{ "id": "MQ==", "enabled": "VHJ1ZQ==", "name": "VW5rbm93bg==", "description": "SXRlbSBoYXMgYmVlbiBjaGVja2VkLCBidXQgcmVwdXRhdGlvbiBkYXRhYmFzZXMgaGF2ZSBubyBnb29kIG9yIGJhZCByZXB1dGF0aW9uIHZhbHVlIGZvciB0aGlzIGl0ZW0u", "description_html": "PHA+SXRlbSBoYXMgYmVlbiBjaGVja2VkLCBidXQgcmVwdXRhdGlvbiBkYXRhYmFzZXMgaGF2ZSBubyBnb29kIG9yIGJhZCByZXB1dGF0aW9uIHZhbHVlIGZvciB0aGlzIGl0ZW0uPC9wPgo="},{ "id": "Mg==", "enabled": "VHJ1ZQ==", "name": "Q2xlYW4=", "description": "UmVwdXRhdGlvbiBkYXRhYmFzZSBjb250YWlucyB0aGUgaXRlbSBhbmQgaXQgaXMgY2xlYW4u", "description_html": "PHA+UmVwdXRhdGlvbiBkYXRhYmFzZSBjb250YWlucyB0aGUgaXRlbSBhbmQgaXQgaXMgY2xlYW4uPC9wPgo="},{ "id": "Mw==", "enabled": "VHJ1ZQ==", "name": "U3VzcGljaW91cw==", "description": "UmVwdXRhdGlvbiBkYXRhYmFzZSBjb250YWlucyBzb21lIGluZm9ybWF0aW9uIGJ1dCBjYW5ub3QgdGVsbCBmb3Igc3VyZS4=", "description_html": "PHA+UmVwdXRhdGlvbiBkYXRhYmFzZSBjb250YWlucyBzb21lIGluZm9ybWF0aW9uIGJ1dCBjYW5ub3QgdGVsbCBmb3Igc3VyZS48L3A+Cg=="},{ "id": "NA==", "enabled": "VHJ1ZQ==", "name": "TWFsaWNpb3Vz", "description": "VGhlIGl0ZW0gaXMgbWFsaWNpb3VzLg==", "description_html": "PHA+VGhlIGl0ZW0gaXMgbWFsaWNpb3VzLjwvcD4K"}]
# print(type(data1))
# print(type(data2))
# print("jdata1:")
jdata1 = json.dumps(data2)
# print(type(jdata1))
# print(jdata1)
# print("ldata1:")
# ldata1 = json.loads(jdata1)
# print(type(ldata1))
# print(ldata1)

jdata2 = json.dumps(data2)
print(type(jdata2))
print(jdata2)
ldata2 = json.loads(jdata2)
print(type(ldata2))
print(ldata2[0]['id'])
