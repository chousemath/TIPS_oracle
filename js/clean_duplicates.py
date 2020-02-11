import hashlib
from os import path, listdir, remove

def md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

for root in [x for x in listdir('.') if path.isdir(x)]:
    print(f'Searching through {root}')
    m5_map = {}
    total = 0
    duplicates = 0
    for fpath in [path.join(root, x) for x in listdir(root) if '.html' in x]:
        total += 1
        m5 = md5(fpath)
        if m5_map.get(m5) is None:
            m5_map[m5] = True
        else:
            duplicates += 1
            remove(fpath)
    
    print(f'total: {total}, duplicates: {duplicates}\n\n')

