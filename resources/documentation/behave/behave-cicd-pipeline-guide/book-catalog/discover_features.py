import json
from pathlib import Path


features = sorted(str(p) for p in Path('features').rglob('*.feature') if 'steps' not in p.parts)
shards = 4
print(json.dumps([features[i::shards] for i in range(shards)]))
