f = open('400006')
wr = open('testdata', 'w')

import json
stuff = json.loads(f.read())
stuff['data'] = stuff['data'][:10]
wr.write(json.dumps(stuff))

wr.close()