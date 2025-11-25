# make_ico.py  
from PIL import Image
import sys, os

if len(sys.argv) < 2:
    print("PNGをここにドロップしてね！")
    input()
    exit()

png_path = sys.argv[1]
ico_path = os.path.splitext(png_path)[0] + ".ico"
img = Image.open(png_path).convert("RGBA")
img.save(ico_path, format="ICO", sizes=[(256,256), (512,512)])
print(f"完成！ → {ico_path}")
os.startfile(os.path.dirname(ico_path))
input()
