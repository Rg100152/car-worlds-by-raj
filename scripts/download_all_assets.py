#!/usr/bin/env python3
import os
import io
import math
import random
import urllib.request
import urllib.error
from PIL import Image, ImageDraw, ImageFilter

BASE = "/home/raj/Desktop/1/car worlds "
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}
MIN_BYTES = 15_000

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def is_valid_image(data: bytes) -> bool:
    if len(data) < MIN_BYTES:
        return False
    if data[:2] == b"\xff\xd8":
        return True
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return True
    return False

def download_one(url: str, out_path: str, min_bytes=MIN_BYTES) -> bool:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=45) as r:
            data = r.read()
        if len(data) < min_bytes:
            print(f"[SKIP small] {url} -> {len(data)}")
            return False
        # basic image validation
        if not (data[:2] == b"\xff\xd8" or data[:8] == b"\x89PNG\r\n\x1a\n" or (data[:4]==b"RIFF" and data[8:12]==b"WEBP")):
            print(f"[SKIP type] {url}")
            return False
        ensure_dir(out_path)
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"[OK] {out_path} ({len(data)//1024} KB)")
        return True
    except Exception as e:
        print(f"[FAIL] {url} -> {e}")
        return False

def download_with_fallback(out_path: str, urls, min_bytes=MIN_BYTES) -> bool:
    for url in urls:
        if download_one(url, out_path, min_bytes=min_bytes):
            return True
    print(f"[MISSING] {out_path}")
    return False

# ---------- Pattern generation (reliable) ----------
def gen_carbon_fiber(path):
    w,h=1200,800
    img = Image.new("RGB",(w,h),(18,20,24))
    d = ImageDraw.Draw(img)
    step=16
    for y in range(0,h,step):
        for x in range(0,w,step):
            c = 28 if ((x//step + y//step) % 2 == 0) else 12
            d.rectangle([x,y,x+step-1,y+step-1], fill=(c,c,c))
    # weave highlight
    for y in range(0,h,step*2):
        d.rectangle([0,y,w,y+2], fill=(45,45,48))
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    img.save(path, "JPEG", quality=92)

def gen_hex_grid(path):
    w,h=1200,800
    img = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(img)
    r=28
    dx = r*math.sqrt(3)
    dy = r*1.5
    for row in range(-1,int(h/dy)+2):
        for col in range(-1,int(w/dx)+2):
            cx = col*dx + (dx/2 if row%2 else 0)
            cy = row*dy
            pts=[]
            for i in range(6):
                a = math.radians(60*i-30)
                pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
            d.polygon(pts, outline=(255,255,255,55))
    img.save(path, "PNG")

def gen_speed_lines(path):
    w,h=1400,900
    img = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(img)
    random.seed(7)
    for i in range(180):
        y = random.randint(0,h)
        x1 = random.randint(-200, w)
        length = random.randint(120, 520)
        thickness = random.randint(1,3)
        alpha = random.randint(35,110)
        color = (255,255,255,alpha)
        d.line([(x1,y),(x1+length,y+random.randint(-12,12))], fill=color, width=thickness)
    img.save(path, "PNG")

def gen_mesh_gradient(path):
    w,h=1400,900
    base = Image.new("RGB",(w,h),(20,30,48))
    top = Image.new("RGB",(w,h),(20,30,48))
    td = ImageDraw.Draw(top)
    blobs = [
        (200,200,255,120,80,160),
        (1100,180,56,189,248,140),
        (300,700,251,191,36,130),
        (1000,650,251,113,133,120),
    ]
    for cx,cy,rr,gg,bb,rad in blobs:
        for r in range(rad,0,-4):
            a = int(80 * (r/rad))
            td.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(rr,gg,bb))
    top = top.filter(ImageFilter.GaussianBlur(80))
    img = Image.blend(base, top, 0.85)
    img.save(path, "JPEG", quality=92)

def gen_topo_lines(path):
    w,h=1200,800
    img = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(img)
    random.seed(3)
    for i in range(28):
        y0 = i*32 + random.randint(-8,8)
        pts=[]
        for x in range(0,w+40,40):
            y = y0 + int(18*math.sin((x/120.0)+i*0.4)) + random.randint(-4,4)
            pts.append((x,y))
        d.line(pts, fill=(255,255,255,60), width=2)
    img.save(path, "PNG")

def gen_brushed_metal(path):
    w,h=1200,800
    img = Image.new("RGB",(w,h),(140,145,150))
    d = ImageDraw.Draw(img)
    random.seed(11)
    for y in range(h):
        v = 130 + random.randint(-18,18)
        d.line([(0,y),(w,y)], fill=(v,v,v+4))
    # subtle horizontal sheen
    for x in range(0,w,3):
        a = 150 + int(20*math.sin(x/40))
        d.line([(x,0),(x,h)], fill=(a,a,a+2))
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    img.save(path, "JPEG", quality=92)

def gen_circuit(path):
    w,h=1200,800
    img = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(img)
    random.seed(5)
    for _ in range(120):
        x = random.randint(0,w)
        y = random.randint(0,h)
        l = random.randint(40,180)
        if random.random()<0.5:
            x2=x+l; y2=y
        else:
            x2=x; y2=y+l
        d.line([(x,y),(x2,y2)], fill=(56,189,248,90), width=2)
        d.ellipse([x2-3,y2-3,x2+3,y2+3], fill=(251,191,36,140))
    img.save(path, "PNG")

def gen_tire_tread(path):
    w,h=1200,800
    img = Image.new("RGB",(w,h),(25,27,32))
    d = ImageDraw.Draw(img)
    for y in range(0,h,40):
        offset = 20 if (y//40)%2 else 0
        for x in range(-40,w+40,80):
            d.polygon([(x+offset,y),(x+offset+30,y),(x+offset+45,y+20),(x+offset+15,y+20)], fill=(55,58,66))
            d.polygon([(x+offset+40,y+20),(x+offset+70,y+20),(x+offset+55,y+40),(x+offset+25,y+40)], fill=(45,48,55))
    img = Image.blend(img, Image.new("RGB",(w,h),(15,15,18)), 0.25)
    img.save(path, "JPEG", quality=92)

def gen_blueprint(path):
    w,h=1200,800
    img = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(img)
    step=40
    for x in range(0,w,step):
        d.line([(x,0),(x,h)], fill=(255,255,255,35), width=1)
    for y in range(0,h,step):
        d.line([(0,y),(w,y)], fill=(255,255,255,35), width=1)
    for x in range(0,w,step*5):
        d.line([(x,0),(x,h)], fill=(56,189,248,60), width=1)
    for y in range(0,h,step*5):
        d.line([(0,y),(w,y)], fill=(56,189,248,60), width=1)
    img.save(path, "PNG")

def gen_noise(path):
    w,h=800,800
    random.seed(42)
    img = Image.new("L",(w,h))
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            pixels[x,y] = random.randint(90,165)
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    img.convert("RGBA").save(path, "PNG")

def generate_patterns():
    pdir = os.path.join(BASE, "assets/images/patterns")
    os.makedirs(pdir, exist_ok=True)
    gens = {
        "carbon-fiber.jpg": gen_carbon_fiber,
        "hex-grid.png": gen_hex_grid,
        "speed-lines.png": gen_speed_lines,
        "mesh-gradient.jpg": gen_mesh_gradient,
        "topo-lines.png": gen_topo_lines,
        "brushed-metal.jpg": gen_brushed_metal,
        "circuit-pattern.png": gen_circuit,
        "tire-tread.jpg": gen_tire_tread,
        "blueprint-grid.png": gen_blueprint,
        "noise-grain.png": gen_noise,
    }
    for name, fn in gens.items():
        out = os.path.join(pdir, name)
        fn(out)
        sz = os.path.getsize(out)
        print(f"[PATTERN] {out} ({sz//1024} KB)")

# ---------- Downloads ----------
def download_hero_and_bg():
    assets = {
        os.path.join(BASE, "assets/images/hero.jpg"): [
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1920&q=80",
            "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1920&q=80",
            "https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=1920&q=80",
        ],
        os.path.join(BASE, "assets/images/bg-wallpaper.jpg"): [
            "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1920&q=80",
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1920&q=80",
            "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1920&q=80",
        ],
    }
    for out, urls in assets.items():
        download_with_fallback(out, urls, min_bytes=100_000)

def download_cars():
    # Curated Unsplash photo URLs (real car photos)
    cars = {
        "bugatti-chiron.jpg": [
            "https://images.unsplash.com/photo-1566023888476-6f17e8b4e8b6?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&w=1600&q=80",
        ],
        "ferrari-sf90.jpg": [
            "https://images.unsplash.com/photo-1592198084033-aade902d1aae?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=1600&q=80",
        ],
        "lamborghini-aventador.jpg": [
            "https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?auto=format&fit=crop&w=1600&q=80",
        ],
        "porsche-911.jpg": [
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=1600&q=80",
        ],
        "rolls-royce.jpg": [
            "https://images.unsplash.com/photo-1631295868223-63265b40d9e4?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1600&q=80",
        ],
        "bmw-m4.jpg": [
            "https://images.unsplash.com/photo-1617531653332-bd46c24f2068?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1600&q=80",
        ],
        "mercedes-gwagon.jpg": [
            "https://images.unsplash.com/photo-1520031441872-265e4ff70366?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1600&q=80",
        ],
        "audi-r8.jpg": [
            "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1614200187524-dc4b892acf16?auto=format&fit=crop&w=1600&q=80",
        ],
        "tesla-model-s.jpg": [
            "https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1536700503339-1e4b06520771?auto=format&fit=crop&w=1600&q=80",
        ],
        "ford-mustang.jpg": [
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1584345604476-8ec5f82d718c?auto=format&fit=crop&w=1600&q=80",
        ],
        "nissan-gtr.jpg": [
            "https://images.unsplash.com/photo-1611859266238-4b98091d9d9b?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=1600&q=80",
        ],
        "toyota-supra.jpg": [
            "https://images.unsplash.com/photo-1632245889029-e406faaa34cd?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1611821064430-0d40291d0f0b?auto=format&fit=crop&w=1600&q=80",
        ],
        "tata-suv.jpg": [
            "https://images.unsplash.com/photo-1506015391300-4802dc74de2e?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1600&q=80",
        ],
        "mahindra-thar.jpg": [
            "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1609521263047-f8f205293f24?auto=format&fit=crop&w=1600&q=80",
        ],
        "mclaren.jpg": [
            "https://images.unsplash.com/photo-1621135802920-133df287f89c?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&w=1600&q=80",
        ],
        "aston-martin.jpg": [
            "https://images.unsplash.com/photo-1608340821332-3a73fadd890c?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1567808291548-fc3ee04dbcf0?auto=format&fit=crop&w=1600&q=80",
        ],
        "koenigsegg.jpg": [
            "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80",
        ],
        "pagani.jpg": [
            "https://images.unsplash.com/photo-1566023888476-6f17e8b4e8b6?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1600&q=80",
        ],
        "bentley.jpg": [
            "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1631295868223-63265b40d9e4?auto=format&fit=crop&w=1600&q=80",
        ],
        "maserati.jpg": [
            "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1600&q=80",
        ],
        "dodge-challenger.jpg": [
            "https://images.unsplash.com/photo-1612544448445-b8232cff3b6c?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1600&q=80",
        ],
        "chevrolet-camaro.jpg": [
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1584345604476-8ec5f82d718c?auto=format&fit=crop&w=1600&q=80",
        ],
        "jeep-wrangler.jpg": [
            "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1506015391300-4802dc74de2e?auto=format&fit=crop&w=1600&q=80",
        ],
        "range-rover.jpg": [
            "https://images.unsplash.com/photo-1609521263047-f8f205293f24?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1600&q=80",
        ],
        "honda-civic-type-r.jpg": [
            "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1611859266238-4b98091d9d9b?auto=format&fit=crop&w=1600&q=80",
        ],
        "lexus-lc.jpg": [
            "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1600&q=80",
        ],
        "mercedes-amg.jpg": [
            "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1600&q=80",
        ],
        "ferrari-roma.jpg": [
            "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1592198084033-aade902d1aae?auto=format&fit=crop&w=1600&q=80",
        ],
        "porsche-taycan.jpg": [
            "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80",
        ],
        "bmw-i8.jpg": [
            "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1617531653332-bd46c24f2068?auto=format&fit=crop&w=1600&q=80",
        ],
        "classic-muscle.jpg": [
            "https://images.unsplash.com/photo-1566008885218-90abf9200ddb?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1489824904134-891ab64532f1?auto=format&fit=crop&w=1600&q=80",
        ],
        "jaguar-f-type.jpg": [
            "https://images.unsplash.com/photo-1567808291548-fc3ee04dbcf0?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1608340821332-3a73fadd890c?auto=format&fit=crop&w=1600&q=80",
        ],
        "volvo-xc90.jpg": [
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1600&q=80",
            "https://images.unsplash.com/photo-1506015391300-4802dc74de2e?auto=format&fit=crop&w=1600&q=80",
        ],
    }
    outdir = os.path.join(BASE, "assets/images/cars")
    ok=0; fail=0
    for name, urls in cars.items():
        out = os.path.join(outdir, name)
        if download_with_fallback(out, urls):
            ok+=1
        else:
            fail+=1
    print(f"\nCars: OK={ok} FAIL={fail}")
    return ok, fail

if __name__ == "__main__":
    generate_patterns()
    download_hero_and_bg()
    download_cars()
    # validation
    print("\n--- Validation ---")
    bad = []
    for root,_,files in os.walk(os.path.join(BASE, "assets/images")):
        for f in files:
            p = os.path.join(root,f)
            sz = os.path.getsize(p)
            with open(p,'rb') as fh:
                head = fh.read(16)
            is_img = head[:2]==b'\xff\xd8' or head[:8]==b'\x89PNG\r\n\x1a\n' or (head[:4]==b'RIFF' and head[8:12]==b'WEBP')
            if not is_img or sz < 1000:
                bad.append((p,sz))
    if bad:
        print("BAD FILES:")
        for b in bad: print(b)
    else:
        print("All image files look valid.")
