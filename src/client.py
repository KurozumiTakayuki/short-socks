"""
short-socksサーバ　プロトタイプ
"""
import socket
import pickle

buf_size = 2048


class Client:
    def __init__(self, socket_path):
        # ソケット位置を設定する
        self.socket_path = socket_path

    def set(self, key, value):
        # コネクション作成
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path)

        # 値をシリアライズ
        s_value = pickle.dumps(value)

        # 操作種別、キー、オブジェクトをタプルにしてさらにシリアライズして送信
        operation_data = ("set", key, s_value)
        s.send(pickle.dumps(operation_data))

        # レスポンスを受け取る
        response = s.recv(buf_size)

        # コネクション切断
        s.close()

        return pickle.loads(response)

    def get(self, key):
        # コネクション作成
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path)

        # 操作種別、キーをタプルにしてシリアライズして送信
        operation_data = ("get", key)
        s.send(pickle.dumps(operation_data))

        # レスポンスを受け取る
        response = s.recv(buf_size)

        # コネクション切断
        s.close()

        # 通信用と保存用で2回シリアライズしているため、2回デシリアライズする
        s_value = pickle.loads(response)

        return pickle.loads(s_value)

    def save(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path)
        operation_data = ("save",)
        s.send(pickle.dumps(operation_data))
        data = s.recv(buf_size)
        s.close()

        return pickle.loads(data)

    def load(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path)
        operation_data = ("load",)
        s.send(pickle.dumps(operation_data))
        data = s.recv(buf_size)
        s.close()

        return pickle.loads(data)

    def keys(self):
        # コネクション作成
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.socket_path)

        # 操作種別、キーをタプルにしてシリアライズして送信
        operation_data = ("keys",)
        s.send(pickle.dumps(operation_data))

        # レスポンスを受け取る
        response = s.recv(buf_size)

        # コネクション切断
        s.close()

        # 結果を返す
        return pickle.loads(response)
