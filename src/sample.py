"""
short-socks利用サンプル
"""
from client import Client


def main():
    client = Client('/tmp/myapp.sock')
    value = "テストデータ"
    client.set("key001", value)
    value = client.get("key001")
    print(value)


if __name__ == '__main__':
    main()
