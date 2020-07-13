import os
import shutil


count = 0
for x in (x for x in os.listdir('pages_detail_carmanager') if '.html' in x):
    print(x)
    shutil.copyfile(
        os.path.join('pages_detail_carmanager', x),
        os.path.join('carmanager_to_zip', x)
    )
    count += 1
    if count >= 400_000:
        break
