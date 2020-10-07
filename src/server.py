"""
short-socksサーバ　プロトタイプ
"""
import os
import socket
import pickle

BUCKET = dict()
buf_size = 2048
save_path = '/tmp/short-socks.dat'


def start(socket_path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(socket_path)
    s.listen(1)
    try:
        while True:
            connection, address = s.accept()
            accepted(connection, address)
    finally:
        os.remove(socket_path)


def accepted(connection, address):
    data = connection.recv(buf_size)
    data_tuple = pickle.loads(data)

    if type(data_tuple) != tuple:
        raise Exception

    op_type = data_tuple[0]
    if op_type == "set":
        set(connection, data_tuple)

    elif op_type == "get":
        get(connection, data_tuple)

    elif op_type == "save":
        save(connection, data_tuple)

    elif op_type == "load":
        load(connection, data_tuple)

    elif op_type == "keys":
        get_keys(connection, data_tuple)


def get_keys(connection, data_tuple):
    keys = list(BUCKET.keys())
    connection.send(pickle.dumps(keys))


def set(connection, data_tuple):
    key = data_tuple[1]

    if type(key) != str:
        raise Exception

    value = data_tuple[2]
    BUCKET[key] = value
    connection.send(pickle.dumps("OK"))


def get(connection, data_tuple):
    key = data_tuple[1]
    value = BUCKET.get(key)
    connection.send(pickle.dumps(value))


def save(connection, data_tuple):
    print("ディスクへの書き出し開始")
    bin_data = pickle.dumps(BUCKET)
    with open(save_path, "bw") as f:
        f.write(bin_data)
    connection.send(pickle.dumps("OK"))
    print("ディスクへの書き出し終了")


def load(connection, data_tuple):
    print("ディスクからの読み込み開始")
    with open(save_path, "br") as f:
        saved = f.read()
        global BUCKET
        BUCKET = pickle.loads(saved)
    connection.send(pickle.dumps("OK"))
    print("ディスクからの読み込み終了")


def main():
    start('/tmp/myapp.sock')


if __name__ == '__main__':
    main()
