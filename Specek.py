import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import platform
import psutil
import cpuinfo
import socket
import wmi
import time
import netifaces
import datetime
import threading

# Function untuk ambil MAC Address berdasarkan jenis interface
def get_network_adapters_info():
    adapters_info = []
    for interface in netifaces.interfaces():
        try:
            addrs = netifaces.ifaddresses(interface)
            mac_info = addrs.get(netifaces.AF_LINK)
            mac = mac_info[0]['addr'] if mac_info and 'addr' in mac_info[0] else "Tidak Ditemukan"
            
            ip_info = addrs.get(netifaces.AF_INET)
            ip = ip_info[0]['addr'] if ip_info else "Tidak Ditemukan"
            
            adapters_info.append(f"{interface} - MAC: {mac}, IP: {ip}")
        except Exception as e:
            adapters_info.append(f"{interface} - Error: {e}")
    return adapters_info

# Function untuk ambil IP Address akurat
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Tidak ditemukan"

# Function untuk ambil device spesifikasi
def get_specs():
    c = wmi.WMI()

    try:
        cpu = cpuinfo.get_cpu_info()
        gpu = ", ".join([gpu.Name for gpu in c.Win32_VideoController()]) or "Tidak ditemukan"
        serial_number = c.Win32_BIOS()[0].SerialNumber or "Tidak ditemukan"
        computer_name = socket.gethostname() or "Tidak ditemukan"
        year = c.Win32_BIOS()[0].ReleaseDate[:4] if c.Win32_BIOS()[0].ReleaseDate else "Tidak ditemukan"

        drive_info = [f"{disk.Model} ({disk.MediaType})" for disk in c.Win32_DiskDrive()]

        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)

        manufacturer = c.Win32_ComputerSystem()[0].Manufacturer or "Tidak ditemukan"
        model = c.Win32_ComputerSystem()[0].Model or "Tidak ditemukan"

        os_version = platform.platform()
        cpu_cores = psutil.cpu_count(logical=False) or "Tidak ditemukan"

        uptime_seconds = int(time.time() - psutil.boot_time())
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{hours} Jam {minutes} Menit {seconds} Detik"

        ip_address = get_ip_address()

        check_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update label values
        labels["Waktu Cek"].set(check_time)
        labels["CPU"].set(cpu['brand_raw'])
        labels["GPU"].set(gpu)
        labels["Serial Number"].set(serial_number)
        labels["Computer Name"].set(computer_name)
        labels["Tahun Pembuatan"].set(year)
        labels["Drive"].set(", ".join(drive_info))
        labels["RAM"].set(f"{ram} GB")
        labels["Merk & Tipe"].set(f"{manufacturer} {model}")
        labels["OS Version"].set(os_version)
        labels["CPU Cores"].set(cpu_cores)
        labels["System Uptime"].set(uptime)
        labels["IP Address"].set(ip_address)

        # Ambil semua adapter
        adapter_info = "\n".join(get_network_adapters_info())
        labels["Network Adapters"].set(adapter_info)
        
        status_var.set("Spesifikasi berhasil diambil.")

    except Exception as e:
        status_var.set(f"Error: {e}")

# Function untuk export hasil ke file txt
def run_specs_thread():
    threading.Thread(targer=get_specs, daemon=True).start()

def save_to_file():
    try:
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")])
        if not filename:
            return

        with open(filename, "w", encoding="utf-8") as f:
            for field in spec_fields:
                value = labels[field].get()
                f.write(f"{field}: {value}\n")

        messagebox.showinfo("Berhasil", f"Spesifikasi berhasil disimpan ke {filename}")
        status_var.set("Hasil disimpan ke file.")

    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file: {e}")
        status_var.set("Gagal menyimpan file.")

# Function copy ke clipboard
def copy_to_clipboard():
    try:
        text = ""
        for field in spec_fields:
            value = labels[field].get()
            text += f"{field}: {value}\n"

        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        messagebox.showinfo("Disalin", "Spesifikasi telah disalin ke clipboard.")
        status_var.set("Disalin ke clipboard.")

    except Exception as e:
        status_var.set(f"Error: {e}")

# GUI setup
root = tk.Tk()
root.title("HokBen Spec Checker v1.0")
root.geometry("720x650")
root.resizable(False, False)

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

labels = {}
row = 0

spec_fields = [
    "Waktu Cek", "CPU", "GPU", "Serial Number", "Computer Name", "Tahun Pembuatan",
    "Drive", "RAM", "Merk & Tipe", "OS Version", "CPU Cores", "System Uptime", "IP Address", "Network Adapters"
]

for field in spec_fields:
    ttk.Label(mainframe, text=field).grid(column=0, row=row, sticky=tk.W, padx=5, pady=2)
    labels[field] = tk.StringVar()
    ttk.Label(mainframe, textvariable=labels[field], wraplength=500).grid(column=1, row=row, sticky=tk.W, padx=5, pady=2)
    row += 1

# Tombol-tombol
ttk.Button(mainframe, text="Cek Spesifikasi", command=get_specs).grid(column=0, row=row, columnspan=2, pady=8)
ttk.Button(mainframe, text="Simpan ke File", command=save_to_file).grid(column=0, row=row+1, columnspan=2, pady=8)
ttk.Button(mainframe, text="Copy ke Clipboard", command=copy_to_clipboard).grid(column=0, row=row+2, columnspan=2, pady=8)

# Status bar
status_var = tk.StringVar()
status_var.set("Siap.")
status_bar = ttk.Label(root, textvariable=status_var, relief="sunken", anchor="w", padding=5)
status_bar.grid(column=0, row=1, sticky=(tk.W, tk.E))

root.mainloop()