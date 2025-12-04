import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import socket
import threading

# --- Global Ayarlar ---
SERIAL_PORT = 'COM3' # BURAYI KENDİ PORTUNUZLA DEĞİŞTİRİN
BAUD_RATE = 9600
MAX_DISTANCE = 400 

# --- Soket Ayarları ---
HOST = '127.0.0.1'  
PORT = 65432        
current_max_distance = MAX_DISTANCE
target_max_distance = MAX_DISTANCE
max_distance_step = 50 

# --- Seri Bağlantı ---
try:
    # Seri bağlantıyı başlat
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2) # Arduino'nun sıfırlanması için bekle
    print(f"Seri bağlantı başarılı: {SERIAL_PORT}")
except Exception as e:
    print(f"HATA: Seri bağlantı kurulamadı. Portu kontrol edin ({SERIAL_PORT}).\n{e}")
    exit()

# --- Soket Dinleyici Fonksiyonu (Kontrol Paneli için aynı kalır) ---
def handle_control_connection(conn):
    global target_max_distance
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode('utf-8').strip()
            print(f"\n[Kontrol] Komut alındı: {command}")
            if command == 'ARTIR':
                target_max_distance += max_distance_step
            elif command == 'AZALT':
                target_max_distance -= max_distance_step
                if target_max_distance < max_distance_step: target_max_distance = max_distance_step
            elif command == 'SIFIRLA':
                target_max_distance = MAX_DISTANCE
            print(f"[Kontrol] Yeni Hedef Mesafe: {target_max_distance} cm")
    except Exception as e:
        print(f"[Kontrol] Bağlantı Hatası: {e}")
    finally:
        conn.close()

def start_socket_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"[Kontrol Sunucusu] Dinliyor: {HOST}:{PORT}")
            while True:
                conn, addr = s.accept()
                print(f"[Kontrol Sunucusu] Bağlantı: {addr}")
                threading.Thread(target=handle_control_connection, args=(conn,)).start()
    except Exception as e:
        print(f"[Kontrol Sunucusu] Başlatma Hatası: {e}")

control_thread = threading.Thread(target=start_socket_server)
control_thread.daemon = True
control_thread.start()


# --- Grafik Ayarları (Matplotlib) ---
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, polar=True)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_rlim(0, current_max_distance)
ax.set_rticks(np.arange(0, current_max_distance + 1, 50))
ax.set_thetagrids(np.arange(0, 181, 10))
ax.set_title("Arduino Ultrasonik Radar Sistemi - Sürekli Tarama", va='bottom')
plt.ion() 
plt.show(block=False) 

scatter, = ax.plot([], [], 'o', color='r', markersize=6, alpha=0.8)
sweep_line, = ax.plot([], [], color='g', linewidth=2) 
print("Radar sistemi çalışıyor...")

all_targets_r = []
all_targets_theta = []

# --- Ana Radar Döngüsü ---
while True:
    try:
        if not plt.get_fignums():
            print("Grafik penceresi kapatıldı, çıkılıyor.")
            break

        # 1. Hızlı Ayar Uygulama
        if current_max_distance != target_max_distance:
            current_max_distance = target_max_distance
            ax.set_rlim(0, current_max_distance)
            ax.set_rticks(np.arange(0, current_max_distance + 1, 50))
            ax.set_title(f"Radar Sistemi - Menzil: {current_max_distance} cm", va='bottom')
            
            # Hedef listelerini temizle
            all_targets_r = [r for r in all_targets_r if r <= current_max_distance]
            all_targets_theta = [theta for r, theta in zip(all_targets_r, all_targets_theta) if r <= current_max_distance]

        # 2. Seri Porttan Veri Okuma
        if ser.in_waiting > 0:
            line_bytes = ser.readline()
            data_line = line_bytes.decode('utf-8').strip() 
            
            try:
                angle_deg, distance_cm = map(int, data_line.split(','))
            except ValueError:
                continue 
            
            angle_rad = np.deg2rad(angle_deg)
            
            # --- Görselleştirme ---
            sweep_line.set_data([angle_rad, angle_rad], [0, current_max_distance])

            if 0 < distance_cm < current_max_distance:
                all_targets_theta.append(angle_rad)
                all_targets_r.append(distance_cm)
            
            # Listeyi temiz tut
            max_points = 200
            if len(all_targets_r) > max_points: 
                all_targets_r = all_targets_r[-max_points:]
                all_targets_theta = all_targets_theta[-max_points:]

            # Grafik üzerindeki noktaları güncelle
            scatter.set_data(all_targets_theta, all_targets_r)

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.001) 
    
    except serial.SerialException:
        print("\nSeri Port bağlantısı kesildi.")
        break
    except KeyboardInterrupt:
        print("\nKullanıcı tarafından durduruldu.")
        break
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")
        break

# --- Temizleme ---
if 'ser' in locals() and ser.is_open:
    ser.close()
plt.close()
print("Program sonlandı.")