from PIL import Image
from psd_tools import PSDImage
import os
import time

start_time = time.time()

palcache = {}


def palette_match(color, palette):
    if color in palcache:
        return palcache[color]

    closest_color = (0, 0, 0)
    closest_dist = 1000000
    for c in palette:
        dist = color_distance(color, c)
        if dist < closest_dist:
            closest_dist = dist
            closest_color = c
    return closest_color


def color_distance(color1, color2):
    return pow(abs(color2[0] - color1[0]), 2) + pow(abs(color2[1] - color1[1]), 2) + pow(abs(color2[2] - color1[2]), 2)


def get_palette(img):
    pal = []
    img = img.convert("RGB")
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            col = img.getpixel((i, j))
            if col not in pal:
                pal.append(col)
    return pal


def palettise(img, palette):
    out = Image.new("RGB", img.size, "black")
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            out.putpixel((i, j), palette_match(img.getpixel((i, j)), palette))
    return out


# Get PIL Images from all files in textures/

print("get textures")

texture_path = "textures/"
textures = [f for f in os.listdir(texture_path) if os.path.isfile(os.path.join(texture_path, f))]

imgs = {}

for f in textures:
    if len(f[:f.find('.')]) == 0:
        continue
    name = f[:f.find('.')]
    ext = f[f.find('.') + 1:]
    if ext == "png":
        imgs[name]=Image.open(texture_path+f)
    elif ext == "psd":
        imgs[name] =PSDImage.load(texture_path+f).as_PIL()

# Get palettes from all images in palettes/

print("get palettes")

pals = {}
palettes_path = "palettes/"
palettes = [f for f in os.listdir(palettes_path) if os.path.isfile(os.path.join(palettes_path, f))]


for f in palettes:
    if len(f[:f.find('.')]) == 0:
        continue
    name = f[:f.find('.')]
    ext = f[f.find('.') + 1:]
    if ext == "png":
        pals[name]=get_palette(Image.open(palettes_path+f))


# for every texture, palettise it!!!

for n, p in pals.items():
    print(n+" textures...")
    # clear palette cache for each palette
    pal_cache = {}
    output_folder = "output/"+n
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    for tn, t in imgs.items():
        out = palettise(t, p)
        out.save(output_folder + "/" + tn + ".png")

print("Done!")
print("time: "+str(time.time()-start_time))