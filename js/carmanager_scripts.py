import json
import io

with open('carmanager_links.txt', 'r') as f:
    data = {}
    while True:
        line = f.readline()
        if not line:
            break
        try:
            i_start = line.index('carmangerDetailWindowPopUp')
            i_end = line.index("')\"")
            data[line[i_start:i_end+2].replace('"', "'").strip()] = True

        except Exception as e:
            print(str(e))
    with io.open('carmanager_links.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
