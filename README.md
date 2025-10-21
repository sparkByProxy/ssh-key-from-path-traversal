Just a small script that searches for users' SSH keys via a path traversal attack.
It's for everyone who, like me, constantly forgets any key file name other than id_rsa.


## Disclaimer
This proof of concept (PoC) script is provided for educational and research purposes only.
Do not use it to target or compromise any systems that you do not own or do not have explicit, written permission to test.

The author assumes no responsibility or liability for any misuse or damage caused by this script.


## Program Flow
It bruteforces the path depth to take (the `../` count).
Then it parses `/etc/passwd` to extract all users with a shell (only `/bin/bash` and `/bin/sh` for now).

for every user it cycles through common the home directory of the users and all ssh keyfile names.

If it gots a key, it prints it to the terminal.


## Debugging
If you have to debug the http reqeusts, just modify the loglevel to this.
```python
logging.basicConfig(level=logging.DEBUG)
```

## CVE-2021-41773
I used the script against Apache 2.4.49 several times in CTFs.
To check this CVE manually, [this is a great explanation of it](https://www.hackthebox.com/blog/cve-2021-41773-explained).


## LFI Vulnerabilities
It also works against webapps with LFI vulnerabilities that run on linux machines.

## Usage
for CVE-2021-41773
`python ssh.py "http://192.168.161.52/cgi-bin/"`

or for other LFIs
`python ssh.py "http://192.168.161.52/zm/index.php?view=file&path="`




## ToDos
- [x] url as cli argument
- [x] use usernames directly from /etc/passwd
- [ ] create ssh keyfile after a finding (and chmod 400)
- [ ] create passphrase hash with ssh2john and output hashcat command to crack it (e.g. `ssh2john id_rsa_anita > anita.hash && john anita.hash --wordlist=/usr/share/wordlists/rockyou.txt`)
- [ ] fancy terminal colors for a hit
