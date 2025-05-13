import os
import sys
import psutil
import requests
import ctypes
import tkinter as tk
from tkinter import messagebox

# ========================
#   VM/SANDBOX DETECTION  
# ========================
def is_vm_or_sandbox():
    # Check for VM processes
    vm_processes = ["vmtoolsd", "vboxservice", "qemu-ga", "procmon"]
    for proc in psutil.process_iter(['name']):
        if any(vm in proc.info['name'].lower() for vm in vm_processes):
            return True
    # Check for sandbox artifacts
    sandbox_files = ["C:\\analysis\\sandbox.txt", "C:\\sample\\malware.exe"]
    for path in sandbox_files:
        if os.path.exists(path):
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
    
    # 2. Change wallpaper to cute animal (Windows only)
    try:
        image_url = "https://i.imgur.com/dQlQ0kK.jpg"  # Cute kitten image
        image_path = os.path.join(os.environ['TEMP'], "kitten.jpg")
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
        f.write("You’re awesome! Have a great day! 🌟\n")

# ========================
#   AV-TRIGGERING TRICKS  
# ========================
def scare_antiviruses():
    # Suspicious string patterns (but do nothing)
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