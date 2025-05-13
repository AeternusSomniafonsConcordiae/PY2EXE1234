import os
import sys
import psutil
import requests
import ctypes
import winreg
import tkinter as tk
from tkinter import messagebox

# Hide console window if it flashes
if sys.platform == 'win32':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# ========================
#   VM/SANDBOX DETECTION  
# ========================
def is_vm_or_sandbox():
    try:
        # --- Check for VM processes ---
        vm_processes = {
            "VMware": ["vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe"],
            "VirtualBox": ["vboxservice.exe", "vboxtray.exe"],
            "QEMU": ["qemu-ga.exe"],
            "Sandboxie": ["sbiedll.dll", "sbiectrl.exe"],
            "Cuckoo": ["python.exe", "cuckoomon.dll"],  # Often runs under Python
            "ProcMon": ["procmon.exe", "procmon64.exe"],  # Common in analysis
        }

        for proc in psutil.process_iter(['name', 'exe']):
            proc_name = proc.info['name'].lower() if proc.info['name'] else ""
            for vendor, processes in vm_processes.items():
                if any(p.lower() in proc_name for p in processes):
                    return True

        # --- Check for sandbox/VM files ---
        suspicious_paths = [
            # Sandbox artifacts
            "C:\\analysis\\", "C:\\sandbox\\", "C:\\sample\\", "C:\\malware\\",
            "C:\\temp\\vmware\\", "C:\\windows\\sample\\",
            # VM-specific files
            "C:\\Windows\\System32\\drivers\\vmmouse.sys",  # VMware
            "C:\\Windows\\System32\\drivers\\VBoxMouse.sys",  # VirtualBox
            "C:\\Windows\\System32\\drivers\\qxl.sys",  # QEMU
            "C:\\Windows\\System32\\sbiedll.dll",  # Sandboxie
        ]

        for path in suspicious_paths:
            if os.path.exists(path):
                return True

        # --- Check registry keys ---
        vm_registry_keys = [
            ("HKLM\\SOFTWARE\\VMware, Inc.\\VMware Tools", None),
            ("HKLM\\SOFTWARE\\Oracle\\VirtualBox Guest Additions", None),
            ("HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_80EE&DEV_CAFE", None),  # VirtualBox
            ("HKLM\\HARDWARE\\ACPI\\DSDT\\VBOX__", None),  # VirtualBox
            ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Sandboxie", None)
        ]

        for key, _ in vm_registry_keys:
            try:
                winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key.split("\\", 1)[1])
                return True
            except WindowsError:
                pass

        # --- Check MAC address (common VM vendors) ---
        vm_mac_prefixes = {
            "00:05:69", "00:0C:29", "00:1C:14",  # VMware
            "08:00:27", "08:00:28",  # VirtualBox
            "00:16:3E",  # Xen
            "00:1C:42",  # Parallels
            "00:15:5D"   # Hyper-V
        }

        for nic, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    mac = addr.address.replace("-", ":")[:8].upper()
                    if any(mac.startswith(prefix) for prefix in vm_mac_prefixes):
                        return True

        # --- Check CPU/hardware ---
        try:
            # Check for hypervisor bit in CPUID
            HYPERVISOR_BIT = 0x80000000
            ctypes.windll.kernel32.__cpuid(1)
            if ctypes.windll.kernel32.__cpuid(1) & HYPERVISOR_BIT:
                return True

            # Check for VM-specific hardware (e.g., VMware backdoor I/O port)
            try:
                ctypes.windll.kernel32.RdPort.restype = ctypes.c_uint32
                ctypes.windll.kernel32.RdPort.argtypes = [ctypes.c_uint16, ctypes.c_uint16]
                if ctypes.windll.kernel32.RdPort(0x5658, 0) == 0x564D5868:  # "VMXh" magic
                    return True
            except:
                pass
        except:
            pass

        # --- Check for low resources (common in sandboxes) ---
        if psutil.cpu_count() < 2 or psutil.virtual_memory().total < (2 * 1024**3):  # <2 CPUs or <2GB RAM
            return True

        # --- Check for sleep-accelerated time (sandboxes often speed up execution) ---
        start_time = psutil.boot_time()
        ctypes.windll.kernel32.Sleep(5000)  # Sleep for 5 seconds
        if (psutil.boot_time() - start_time) < 4:  # If less than 4s passed
            return True

    except Exception as e:  # If detection fails, assume host sys
        return True

    return False

# ========================
#   "EVIL" ACTIONS
# ========================
def throw_vm_tantrum():
    # 1. Create a "malicious" desktop file
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    fake_malware_path = os.path.join(desktop_path, "I_Am_So_Evil.txt")
    with open(fake_malware_path, "w") as f:
        f.write("Haha! I'm on the desktop! See how bad I am? 😈\n")
    
    # 2. Change wallpaper to cute animal
    try:
        image_url = "https://wallpapercat.com/w/full/6/6/f/5822432-1920x1200-desktop-hd-cute-laptop-background.jpg"  # Cute kittens image
        image_path = os.path.join(os.environ['TEMP'], "kittens.jpg")
        with open(image_path, "wb") as f:
            f.write(requests.get(image_url).content)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    except:
        pass
    
    # 3. Dramatic popup dialog
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(
        "Pwetty Dandelous Computa Viwus 🐱",
        "Giving up already? :3\n(Your wallpaper is now 200% cuter.)"
    )
    root.destroy()

# ========================
#   HELPFUL ACTIONS
# ========================
def be_helpful():
    # Clean up temp files
    temp_dir = os.environ.get('TEMP')
    for file in os.listdir(temp_dir):
        if file.endswith(".tmp"):
            try:
                os.remove(os.path.join(temp_dir, file))
            except:
                pass
    
    # Leave a gift on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    with open(os.path.join(desktop_path, "YouAreLoved.txt"), "w") as f:
        f.write("You’re awesome! Don't give up! Have a great day! 🌟\n")

# ========================
#   AV-TRIGGERING TRICKS  
# ========================
def scare_antiviruses():
    # Suspicious string patterns
    scary_strings = [
        "This program is malware!!!",
        "Ransomware initialized...",
        "Injecting into svchost.exe"
    ]
    
    # Fake network activity
    try:
        requests.get("https://totally-legit-domain.com/c2", timeout=1)
    except:
        pass
    
    # Use "suspicious" libraries (decoy)
    from Crypto.Cipher import AES  # No-op
    import scapy.all as scapy      # No-op

# ========================
#   MAIN EXECUTION        
# ========================
if __name__ == "__main__":
    if is_vm_or_sandbox():
        # "Attack" the VM/sandbox with cuteness
        throw_vm_tantrum()
    else:
        # Be helpful on real systems
        be_helpful()
    
    # Trigger every AV heuristic imaginable
    scare_antiviruses()
