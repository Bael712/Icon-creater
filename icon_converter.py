import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def convert_to_ico():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

    if not file_path:
        return

    try:
        img = Image.open(file_path)
        save_path = os.path.splitext(file_path)[0] + ".ico"
        img.save(save_path, format="ICO")
        messagebox.showinfo("成功", f"変換完了！\n{save_path}")
    except Exception as e:
        messagebox.showerror("エラー", f"変換中に問題が発生しました:\n{e}")

# GUI
root = tk.Tk()
root.title("画像 → ICO 変換アプリ")
root.geometry("300x150")

label = tk.Label(root, text="画像ファイルを ICO に変換します", pady=10)
label.pack()

button = tk.Button(root, text="ファイルを選ぶ", command=convert_to_ico, width=20)
button.pack(pady=10)

root.mainloop()
