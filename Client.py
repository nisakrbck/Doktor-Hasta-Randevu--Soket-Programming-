
import socket
import sys
import threading

HOST = '127.0.0.1'
PORT = 12345

def doktor_tcp_istemcisi():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall("Doktor".encode())

        mesaj = s.recv(1024).decode()
        print(mesaj)

        while True:
            komut = input("Komut girin (Hasta Kabul / exit): ").strip().lower()
            if komut == "exit":
                break
            elif komut == "hasta kabul":
                s.sendall(komut.encode())
                veri = s.recv(1024).decode()
                print("Sunucu:", veri)


def hasta_udp_istemcisi():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto("Hasta".encode(), (HOST, PORT))
        mesaj, _ = s.recvfrom(1024)
        print(mesaj.decode())

        while True:
            try:
                s.settimeout(30.0)
                veri, _ = s.recvfrom(1024)
                mesaj = veri.decode()
                print(mesaj)

                if "randevuyu kabul ediyor musunuz" in mesaj.lower():
                    cevap = input("Randevuyu kabul ediyor musunuz? (Evet/Hayır): ").strip().lower()
                    s.sendto(cevap.encode(), (HOST, PORT))
                    break
            except socket.timeout:
                break
            except Exception as e:
                print(f"Hata: {e}")
                break

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Kullanım: python 22100011069_Client.py <Doktor/Hasta> <TCP/UDP>")
        sys.exit(1)

    rol = sys.argv[1].lower()
    protokol = sys.argv[2].lower()

    if rol == "doktor" and protokol == "tcp":
        doktor_tcp_istemcisi()
    elif rol == "hasta" and protokol == "udp":
        hasta_udp_istemcisi()
    else:
        print("Hatalı giriş. Doğru kullanım: Doktor TCP veya Hasta UDP")

