from pythonping import ping
from time import sleep
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
import ip

plain=b""
with open("./send_logo.png", "rb") as f:
    while True:
        line = f.readline()
        if not line: break
        plain=plain+line
f.close()


class AEScipher:
    def __init__(self):
        self.key = b"aaaaaaaaaaaaaaaa"
        self.iv = b'1111111111111111'

    def encrypt(self, plain):
        plain = pad(plain, AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(plain)

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(enc), AES.block_size)

if __name__ == '__main__':
    print('ICMP FILE TRANSFER')

    print('CREATE ENCRYPTED FILE')
    enc = AEScipher().encrypt(plain)
    with open("./enc.png", "wb") as f:
        f.write(enc)
    f.close()

    print('TRANSFER ENCRYPTED FILE')
    with open("./enc.png", "rb") as f:
        while True:
            byte = f.read(1024)
            if byte == b"":  # EOF, Null
                ping(ip.myip, verbose=True, count=1, payload=b"EOF")
                break
            ping(ip.myip, verbose=True, count=1, payload=byte)
            sleep(0.5)
    f.close()