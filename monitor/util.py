from monitor import db
import json
import requests
import threading
import time

def register_server(address):
    if not (address.startswith("http://") or address.startswith("https://")):
        address = "http://" + address
    try:
        id_ = db.insert_table(address.strip())
        return {"host": address, "id": id_}
    except Exception as e:
        return {"host": address, "id": -1}


    # r = json.dumps({"host": address, "id": id_})
    # print(r)
    # return r


def get_all_servers():
    rows = db.get_all_rows()
    res = []
    for row in rows:
        # res.append(json.dumps(row))
        res.append(row)
    return res


def get_server_by_id(server_id):
    row = db.get_row(int(server_id))
    return row
    # return json.dumps(row)


def check_server_health(address):
    try:
        response = requests.get(url=address)
        if  200 <= response.status_code < 300:
            id_ = db.update_by_address(address.strip(), 1)
        else:
            id_ = db.update_by_address(address.strip(), -1)
    except:
        id_ = db.update_by_address(address.strip(), -1)
    # print(f'{id_}) {address} ** status updated ** {response.status_code}')


def check_all():
    with open('config.json') as fp:
        config = json.load(fp)
    interval = config.get('checking_interval', 1) * 60
    while True:
        servers = db.get_all_rows()
        for server in servers:
            check_server_health(server['address'])
        # print("#"*50)
        time.sleep(interval)


def health_check():
    th = threading.Thread(target=check_all)
    th.daemon = True
    th.start()


def cleanup():
    db.close_connection()
    