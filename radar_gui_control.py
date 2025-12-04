import socket
import time
import tkinter as tk
from tkinter import messagebox

# Ana Radar Uygulamasinin Soket Ayarlari (radar_app.py ile ayni olmali)
HOST = '127.0.0.1' 
PORT = 65432       

def send_command(command):
    """Soket uzerinden ana uygulamaya komut gonderir."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(command.encode('utf-8'))
            print(f"[GUI] Komut gonderildi: {command}")
    except ConnectionRefusedError:
        # Ana uygulama (server) calismiyorsa uyari ver
        messagebox.showerror(
            "Baglanti Hatasi", 
            "Ana Radar Uygulamasi (radar_app.py) calismiyor. Lutfen once radar uygulamasini baslatin."
        )
    except Exception as e:
        messagebox.showerror("Hata", f"Bir sorun olustu: {e}")

# --- Tkinter Arayuzu ---

def create_gui():
    """Grafiksel kullanici arayuzunu (GUI) olusturur."""
    root = tk.Tk()
    root.title("Radar Kontrol Paneli")
    root.geometry("300x250") # Pencere boyutunu biraz artiralim
    root.resizable(False, False)

    # Baslik Etiketi
    title_label = tk.Label(
        root, 
        text="RADAR HIZLI AYARLAR", 
        font=("Helvetica", 14, "bold"), 
        pady=10
    )
    title_label.pack()
    
    # Aciklama Etiketi
    desc_label = tk.Label(
        root,
        text="Menzil adimlari 50 cm'dir.",
        font=("Helvetica", 10),
        pady=5
    )
    desc_label.pack()

    # Artir Butonu
    btn_increase = tk.Button(
        root, 
        text="➕ Menzili Artir", 
        command=lambda: send_command('ARTIR'),
        width=25,
        height=1
    )
    btn_increase.pack(pady=3)

    # Azalt Butonu
    btn_decrease = tk.Button(
        root, 
        text="➖ Menzili Azalt", 
        command=lambda: send_command('AZALT'),
        width=25,
        height=1
    )
    btn_decrease.pack(pady=3)

    # Sifirla Butonu
    btn_reset = tk.Button(
        root, 
        text="🔄 Menzili Sifirla (400 cm)", 
        command=lambda: send_command('SIFIRLA'),
        width=25,
        height=1
    )
    btn_reset.pack(pady=3)
    
    # Ayirici
    separator = tk.Frame(root, height=1, bd=1, relief=tk.SUNKEN)
    separator.pack(fill=tk.X, padx=10, pady=5)
    
    # Kilitlenme Kontrolu (Sadece Gosterge)
    lock_label = tk.Label(
        root, 
        text="Kilitlenme Durumu: Otomatik", 
        font=("Helvetica", 10, "italic"),
        fg="blue"
    )
    lock_label.pack(pady=3)

    root.mainloop()

if __name__ == "__main__":
    create_gui()