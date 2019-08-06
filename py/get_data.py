import pymongo
import json
import io
import os
from normalize import normalize
from dotenv import load_dotenv
load_dotenv()

client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client.oracle
col = db.encar

last_50 = col.find().limit(50);
data = {}
for doc in last_50:
    print(doc.get('_id'))

# with io.open('unmapped_colors.json', 'w') as output:
#     output.write(json.dumps(unmapped_colors, ensure_ascii=False))
