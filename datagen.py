# Write some file here to generate a dataset from govtrack.us api

import httplib, json

conn = httplib.HTTPConnection('www.govtrack.us')
conn.request('GET', '/api/v1/bill/?congress=112&order_by=-current_status_date')
r1 = conn.getresponse()

print r1.reason
bills = json.loads(r1.read())["objects"]
print json.dumps(bills)

