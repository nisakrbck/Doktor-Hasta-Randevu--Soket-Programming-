import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 12345

doctors = []
patients = []
lock = threading.Lock()
next_doctor_id = 1
next_patient_id = 1

# Doktorların randevulu hastaları
doctor_patients = {}


def handle_doctor(conn, addr, doctor_name):
    conn.sendall(f"Hoşgeldiniz {doctor_name}".encode())
    print(f"{doctor_name} TCP ile bağlandı.")

    # Doktorun randevulu hastalarını tanımla (örnek veriler)
    doctor_patients[doctor_name] = []

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data.strip().lower() == "hasta kabul":
                with lock:
                    if patients:
                        patient_conn, patient_name = patients.pop(0)
                        print(f"{patient_name} -> {doctor_name}")
                        conn.sendall(f"{patient_name} çağrıldı.".encode())
                        patient_conn.sendall(
                            f"{doctor_name} sizi çağırıyor. Randevuyu kabul ediyor musunuz? (Evet/Hayır)".encode())

                        # 10 saniye bekle
                        patient_conn.settimeout(10.0)  # 10 saniye zaman aşımı
                        try:
                            response = patient_conn.recv(1024).decode().lower()
                            if response == "evet":
                                print(f"{patient_name} {doctor_name} randevusunu kabul etti")
                                doctor_patients[doctor_name].append(patient_name)
                                conn.sendall(f"{patient_name} randevuyu kabul etti.".encode())
                                patient_conn.sendall("Randevunuz onaylandı.".encode())
                            else:
                                conn.sendall(f"{patient_name} randevuyu reddetti.".encode())
                                patient_conn.sendall("Randevuyu reddettiniz.".encode())
                        except socket.timeout:
                            conn.sendall(f"{patient_name} zaman aşımına uğradı, sıradaki hasta çağrılıyor.".encode())
                            patient_conn.sendall("Randevu zaman aşımına uğradı.".encode())
                        finally:
                            patient_conn.sendall("Geçmiş olsun".encode())
                            patient_conn.close()
                            print(f"{patient_name} ayrıldı")
                    else:
                        conn.sendall("Bekleyen hasta bulunmamaktadır.".encode())

        except Exception as e:
            print(f"{doctor_name} ile iletişimde hata: {e}")
            break
    conn.close()
    with lock:
        doctors.remove((conn, doctor_name))
    print(f"{doctor_name} bağlantısı kesildi.")


def handle_udp_patient(data, addr, udp_socket):
    global next_patient_id
    with lock:
        if not doctors:
            udp_socket.sendto("Sistemde doktor yok. Bağlantı reddedildi.".encode(), addr)
            return
        name = f"Hasta{next_patient_id}"
        next_patient_id += 1
        udp_socket.sendto(f"Hoşgeldiniz {name}".encode(), addr)
        print(f"{name} UDP ile bağlandı.")
        # Her hasta için UDP soket ile TCP gibi bağlantı kurulamadığından, geçici TCP bağlantısı açılabilir (geliştirilebilir)
        # Burada UDP mesaj gönderme/cevap alma simülasyonu yapılıyor
        dummy_conn = DummySocketUDP(udp_socket, addr)
        patients.append((dummy_conn, name))


class DummySocketUDP:
    def __init__(self, udp_sock, addr):
        self.sock = udp_sock
        self.addr = addr
        self.buffer = ""

    def sendall(self, msg):
        self.sock.sendto(msg, self.addr)

    def recv(self, bufsize):
        data, _ = self.sock.recvfrom(bufsize)
        return data

    def settimeout(self, timeout):  # <-- EKLENEN METOT
        self.sock.settimeout(timeout)

    def close(self):
        self.sock.sendto("Bağlantı kapatıldı.".encode(), self.addr)


def start_server():
    global next_doctor_id  # 'global' kullanarak global değişkene atıfta bulunuyoruz

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((HOST, PORT))
    tcp_socket.listen()

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((HOST, PORT))

    print(f"Sunucu {HOST}:{PORT} adresinde başlatıldı...")

    def tcp_listener():
        global next_doctor_id  # Burada da 'global' kullanmamız gerekiyor
        while True:
            conn, addr = tcp_socket.accept()
            client_type = conn.recv(1024).decode()  # İlk gelen veriyi istemci türü olarak kabul et
            print(f"Gelen bağlantı: {client_type} ({addr})")

            with lock:
                if client_type.lower() == "doktor":
                    name = f"Doktor{next_doctor_id}"
                    next_doctor_id += 1
                    doctors.append((conn, name))
                    threading.Thread(target=handle_doctor, args=(conn, addr, name), daemon=True).start()
                elif client_type.lower() == "hasta":
                    name = f"Hasta{next_patient_id}"
                    next_patient_id += 1
                    patients.append((conn, name))
                    print(f"{name} hasta olarak bağlandı.")
                else:
                    print(f"Hatalı istemci türü: {client_type}")
                    conn.close()

    def udp_listener():
        while True:
            try:
                data, addr = udp_socket.recvfrom(1024)
            except ConnectionResetError:
                print(f"UDP istemcisi {addr} bağlantıyı ani şekilde kapattı (Reset).")
                continue
            except Exception as e:
                print(f"UDP dinleyicide beklenmeyen hata: {e}")
                continue

            if not data:
                continue

            # Hasta daha önce bağlanmamışsa:
            existing_addrs = [p[0].addr for p in patients if isinstance(p[0], DummySocketUDP)]
            if addr not in existing_addrs:
                handle_udp_patient(data, addr, udp_socket)

    # TCP ve UDP listener'larını başlat
    threading.Thread(target=tcp_listener, daemon=True).start()
    threading.Thread(target=udp_listener, daemon=True).start()

    # Ana thread'i sonsuza kadar beklet (örneğin klavyeyle kesilene kadar)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    start_server()
