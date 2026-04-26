import tkinter as tk
from tkinter import messagebox, ttk
import shutil
import os
import subprocess
import sys
import ctypes
import webbrowser

def is_admin():
    try:
        return subprocess.run(['net', 'session'], capture_output=True).returncode == 0
    except:
        return False

def run_as_admin():
    if not is_admin():
        messagebox.showwarning("权限警告", "需要管理员权限来修改环境变量。请以管理员身份运行此程序。")
        return False
    return True

def update_log(message):
    text_log.config(state='normal')
    text_log.insert(tk.END, message + '\n')
    text_log.config(state='disabled')
    text_log.see(tk.END)

def install_adb():
    update_log("开始安装ADB...")
    if not run_as_admin():
        update_log("需要管理员权限。")
        return
    source = 'Driver'
    dest = r'C:\Program Files (x86)\Driver'
    if not os.path.exists(source):
        update_log("错误：Driver文件夹不存在")
        return
    if os.path.exists(dest):
        update_log("错误：目标目录已存在")
        return
    try:
        update_log("正在复制Driver文件夹...")
        shutil.copytree(source, dest)
        update_log("Driver文件夹复制成功")
    except Exception as e:
        update_log(f"复制失败: {str(e)}")
        return
    new_path = dest
    try:
        update_log("正在添加环境变量...")
        # 获取当前系统PATH
        result = subprocess.run(['reg', 'query', 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', '/v', 'PATH'], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("无法读取PATH")
        current_path = ''
        for line in result.stdout.split('\n'):
            if 'PATH' in line and 'REG_' in line:
                current_path = line.split('    ')[-1].strip()
                break
        if new_path not in current_path:
            new_full_path = f'{current_path};{new_path}'
            subprocess.run(['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', '/v', 'PATH', '/t', 'REG_EXPAND_SZ', '/d', new_full_path, '/f'], check=True)
            subprocess.run(['setx', 'PATH', new_full_path], check=True)
            update_log("环境变量添加成功。请重启命令提示符或系统以生效。")
        else:
            update_log("路径已在环境变量中")
    except Exception as e:
        update_log(f"添加环境变量失败: {str(e)}")

def enable_blur(window):
    try:
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        class DWM_BLURBEHIND(ctypes.Structure):
            _fields_ = [
                ("dwFlags", ctypes.c_uint32),
                ("fEnable", ctypes.c_bool),
                ("hRgnBlur", ctypes.c_void_p),
                ("fTransitionOnMaximized", ctypes.c_bool),
            ]
        bb = DWM_BLURBEHIND()
        bb.dwFlags = 0x00000001 | 0x00000002  # DWM_BB_ENABLE | DWM_BB_BLURREGION
        bb.fEnable = True
        bb.hRgnBlur = None
        bb.fTransitionOnMaximized = False
        ctypes.windll.dwmapi.DwmEnableBlurBehindWindow(hwnd, ctypes.byref(bb))
    except:
        pass  # 如果不支持毛玻璃效果，忽略

def open_bilibili():
    webbrowser.open("https://space.bilibili.com/391882110")  # 请替换为您的Bilibili主页UID

def open_github():
    webbrowser.open("https://github.com/xiehuajieaa/adb")  # 请替换为您的GitHub仓库URL

# GUI
root = tk.Tk()
root.title("ADB Boom")
root.geometry("450x350")
root.attributes("-alpha", 0.95)  # 设置半透明

# 启用毛玻璃效果
enable_blur(root)

# 设置样式，使按钮更圆润
style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=(20, 10), relief="flat", borderwidth=0, background="#0078D4", foreground="black")
style.map("TButton", background=[("active", "#005A9E")])

# 小按钮样式，与版本号一致
style.configure("Small.TButton", font=("Arial", 8), padding=(5, 2), relief="flat", borderwidth=0, background="#0078D4", foreground="black")
style.map("Small.TButton", background=[("active", "#005A9E")])

# 布局：按钮在上，编辑框在下
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(side='top', fill='x', pady=20)

ttk.Button(button_frame, text="Install ADB and fastboot", command=install_adb).pack()

text_log = tk.Text(root, height=12, state='disabled', font=("Consolas", 10), bg="#f9f9f9", fg="#333", relief="flat", borderwidth=1)
text_log.pack(side='top', fill='both', expand=True, padx=20, pady=(0, 20))

# 分隔线
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=20, pady=10)

# 底部按钮和版本号
bottom_frame = tk.Frame(root, bg="#f0f0f0")
bottom_frame.pack(side='bottom', fill='x', pady=10)

ttk.Button(bottom_frame, text="Bilibili", style="Small.TButton", command=open_bilibili).pack(side='left', padx=10)
ttk.Button(bottom_frame, text="GitHub", style="Small.TButton", command=open_github).pack(side='left', padx=10)
version_label = tk.Label(bottom_frame, text="Ver 1.0.0", font=("Arial", 8), bg="#f0f0f0")
version_label.pack(side='right', padx=10)

root.mainloop()