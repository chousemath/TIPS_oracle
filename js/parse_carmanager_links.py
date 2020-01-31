import json

def run():
    try:
        with open('carmanager_links.txt', 'r') as f:
            lines = [f'http://carmanager.co.kr/PopupFrame/CarDetail/{x.strip()}' for x in f.readlines() if x.strip()]
            data = {x: True for x in lines}
        with open('carmanager_links.json', 'w') as json_file:
            json.dump(data, json_file)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    run()
