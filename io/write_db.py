import os
import plyvel
import json


cur_dir = os.path.dirname(__file__)
data_path = os.path.join(cur_dir, '../data')


db = plyvel.DB(os.path.join(data_path, 'testdb'),
               create_if_missing=True)


reaction = u'fatigue'

d1 = {'name': u'd1_name', 'type': u'd1_type'}
d2 = {'name': u'd2_name', 'type': u'd2_type', 'lbl': 'yo the label actually gives a warning abou this reaction'}

obj = [d1, d2]

s = json.dumps(obj)

db.put(str(reaction), s)

db.close()