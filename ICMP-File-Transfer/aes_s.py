from socket import *
import os
import struct
import sys
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
import ip

class AEScipher:
    def __init__(self):
        self.key = b"aaaaaaaaaaaaaaaa"
        self.iv = b'1111111111111111'

    def encrypt(self, raw):
        raw = pad(raw, AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(raw)

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(enc), AES.block_size)

def parse_ip_header(ip_header):
    ip_headers = struct.unpack("!BBHHHBBH4s4s", ip_header[:20])
    ip_payloads = ip_header[20:]
    return ip_headers, ip_payloads


def parse_icmp_header(icmp_data):
    icmp_headers = struct.unpack("!BBHHH", icmp_data[:8])
    icmp_payloads = icmp_data[8:]
    return icmp_headers, icmp_payloads


def parsing(host):
    # raw socket 생성 및 bind
    if os.name == "nt":
        sock_protocol = IPPROTO_IP
    else:
        sock_protocol = IPPROTO_ICMP
    sock = socket(AF_INET, SOCK_RAW, sock_protocol)
    sock.bind((host, 0))

    # socket 옵션
    sock.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

    # promiscuous mode 켜기
    if os.name == "nt":
        sock.ioctl(SIO_RCVALL, RCVALL_ON)

    file_path = "./enc.png"
    if os.path.isfile(file_path):
        os.remove(file_path)
    receive_bytes = 0
    try:
        while True:
            data = sock.recvfrom(65535)
            ip_headers, ip_payloads = parse_ip_header(data[0])
            if ip_headers[6] == 1:  # ICMP Only
                ip_source_address = inet_ntoa(ip_headers[8])
                ip_destination_address = inet_ntoa(ip_headers[9])
                print(f"{ip_source_address} => {ip_destination_address}")
                icmp_headers, icmp_payloads = parse_icmp_header(ip_payloads)
                receive_bytes += len(icmp_payloads)
                if icmp_headers[0] == 8:
                    print(f"Receiving data... {receive_bytes}")
                    if icmp_payloads == b"EOF":
                        print("Finished !!!")
                        sock.ioctl(SIO_RCVALL, RCVALL_OFF)
                        break
                    with open(file_path, "ab") as f:
                        f.write(icmp_payloads)

                print("=" * 20)
    except KeyboardInterrupt:  # Ctrl-C key input
        if os.name == "nt":
            sock.ioctl(SIO_RCVALL, RCVALL_OFF)


if __name__ == "__main__":
    host = ip.myip  # 자신의 IP 주소로 변경
    print("START SNIFFING at [%s]" % host)
    parsing(host)
    print("DECRYPTE FILE START")
    enc = b""
    with open("./enc.png", "rb") as f:
        while True:
            line = f.readline()
            if not line: break
            enc = enc + line
    f.close()
    with open("./recv_logo.png", "wb") as f:
        f.write(AEScipher().decrypt(enc))
    f.close()
