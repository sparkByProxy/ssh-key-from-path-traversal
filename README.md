Just a small script that searches for users' SSH keys via a path traversal attack.
It's for everyone who, like me, constantly forgets any key file name other than id_rsa.

## Disclaimer
This proof of concept (PoC) script is provided for educational and research purposes only.
Do not use it to target or compromise any systems that you do not own or do not have explicit, written permission to test.

The author assumes no responsibility or liability for any misuse or damage caused by this script.

## CVE-2021-41773
I used the script against Apache 2.4.49 several times in CTFs.
To check this CVE manually, [this is a great explanation of it](https://www.hackthebox.com/blog/cve-2021-41773-explained).

## ToDos
- [ ] url as cli argument
- [ ] use usernames directly from /etc/passwd
- [ ] create ssh keyfile after a finding (and chmod 400)
- [ ] create passphrase hash with ssh2john and output hashcat command to crack it
- [ ] fancy terminal colors for a hit
