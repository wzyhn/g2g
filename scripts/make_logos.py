"""Generate multi-size compressed logos from logo.png.

Outputs (PNG, palette-optimized):
  assets/favicon-32.png       浏览器标签页
  assets/favicon-180.png      Apple touch / Android home
  assets/logo-48.png          topbar
  assets/logo-256.png         欢迎页大图
  assets/favicon.ico          兼容老浏览器 (16+32+48)
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "logo.png"
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

img = Image.open(SRC).convert("RGBA")
print(f"source: {img.size}  {SRC.stat().st_size / 1024:.0f} KB")

# 多尺寸 PNG
sizes = [
    (32,  "favicon-32.png"),
    (180, "favicon-180.png"),
    (48,  "logo-48.png"),
    (256, "logo-256.png"),
]
for size, name in sizes:
    out = img.resize((size, size), Image.LANCZOS)
    target = OUT / name
    out.save(target, "PNG", optimize=True)
    print(f"  -> {name}  {size}x{size}  {target.stat().st_size / 1024:.1f} KB")

# .ico 多分辨率
ico_target = OUT / "favicon.ico"
img.save(ico_target, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
print(f"  -> favicon.ico  multi-res  {ico_target.stat().st_size / 1024:.1f} KB")

# 报告总体积
total = sum((OUT / name).stat().st_size for _, name in sizes) + ico_target.stat().st_size
print(f"\ntotal assets: {total / 1024:.1f} KB")
print(f"source:      {SRC.stat().st_size / 1024:.0f} KB")
print(f"reduction:   {(1 - total / SRC.stat().st_size) * 100:.0f}%")
