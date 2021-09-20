from socket import *
import os
import struct
import ip

#ip header + icmp header + message
#ip header : 20byte
#icmp header : 8byte 

def parse_ip_header(ip_header):
    # BBHHHBBH4s4s : 1+1+2+2+2+1+1+2+4+4 = 20byte
    ip_headers = struct.unpack("!BBHHHBBH4s4s", ip_header[:20])
    ip_payloads = ip_header[20:]
    return ip_headers, ip_payloads


def parse_icmp_header(icmp_data):
    # BBHHH : 1+1+2+2+2 = 8byte
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
    # 사용자가 header에 접근 허용
    # header도 같이 sniffing
    sock.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

    # promiscuous mode 켜기
    if os.name == "nt":
        sock.ioctl(SIO_RCVALL, RCVALL_ON)

    try:
        while True:
            # ip datagram : ip header + payload (max : 65536 byte)
            data = sock.recvfrom(65535)
            # recvfrom 반환 값 (bytes, address) = (수신한 데이터, 데이터 송신 socket 주소)
            ip_headers, ip_payloads = parse_ip_header(data[0])
            # icmp :1 / tcp : 6 / udp : 17
            if ip_headers[6] == 1:  # ICMP Only
                ip_source_address = inet_ntoa(ip_headers[8])
                ip_destination_address = inet_ntoa(ip_headers[9])
                print(f"{ip_source_address} => {ip_destination_address}")
                icmp_headers, icmp_payloads = parse_icmp_header(ip_payloads)
                if icmp_headers[0] == 0:
                    print("Echo Reply")
                elif icmp_headers[0] == 8:
                    print("Echo Request")
                print("icmp_headers => ", icmp_headers)
                print("icmp_payloads => ", icmp_payloads)
                print("==========================")
    except KeyboardInterrupt:  # Ctrl-C key input
        if os.name == "nt":
            sock.ioctl(SIO_RCVALL, RCVALL_OFF)


if __name__ == "__main__":
    host = ip.myip  # 자신의 IP 주소로 변경
    print("START SNIFFING at [%s]" % host)
    parsing(host)