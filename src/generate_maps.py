import os
from PIL import Image, ImageDraw, ImageFont

MAPS_DIR = "assets/maps"
os.makedirs(MAPS_DIR, exist_ok=True)

# 1. Carica l'immagine originale croppata
orig_path = os.path.join(MAPS_DIR, "watcher_kaira.png")
orig_img = Image.open(orig_path).convert("RGBA")
width, height = orig_img.size

# 2. Estrai il marker rosso
# Bounding box del marker originale: x=[412, 449], y=[212, 239]
marker_crop = orig_img.crop((410, 210, 452, 242))

# Rendiamo trasparente lo sfondo del marker
marker_rgba = marker_crop.copy()
pixels = marker_rgba.load()
for x in range(marker_rgba.width):
    for y in range(marker_rgba.height):
        r, g, b, a = pixels[x, y]
        # Se è rosso o contorno nero
        is_red = (r > 120 and g < 75 and b < 75)
        is_black = (r < 55 and g < 55 and b < 55)
        if not (is_red or is_black):
            pixels[x, y] = (0, 0, 0, 0)

marker_rgba.save(os.path.join(MAPS_DIR, "marker_icon.png"))

# 3. Crea la base pulita senza marker
clean_base = orig_img.copy()
clean_pixels = clean_base.load()
# Rimpiazza l'area del marker con il colore della sabbia dell'isola circostante
sample_color = orig_img.getpixel((415, 204))
for x in range(408, 454):
    for y in range(208, 244):
        r, g, b, a = clean_pixels[x, y]
        if (r > 120 and g < 75 and b < 75) or (r < 55 and g < 55 and b < 55):
            noise = ((x * 17 + y * 11) % 12) - 6
            clean_pixels[x, y] = (
                max(0, min(255, sample_color[0] + noise)),
                max(0, min(255, sample_color[1] + noise)),
                max(0, min(255, sample_color[2] + noise)),
                255
            )

clean_base.save(os.path.join(MAPS_DIR, "clean_base.png"))

# 4. Definiamo le coordinate e i nomi dei Boss su Chaotic Lower Reshanta
bosses = {
    "watcher_kaira": {
        "name": "Watcher Kaira",
        "x": 431,
        "y": 226,
        "desc": "Isola Centrale Destra"
    },
    "executor_kaira": {
        "name": "Executor Kaira",
        "x": 195,
        "y": 230,
        "desc": "Sulfur Tree Island (Ovest)"
    },
    "executor_tamasa": {
        "name": "Executor Tamasa",
        "x": 310,
        "y": 320,
        "desc": "Isola Sud (Asteria)"
    },
    "executor_argo": {
        "name": "Executor Argo",
        "x": 560,
        "y": 140,
        "desc": "Fortezza Est / Roah"
    },
    "guardian_lord_nahma": {
        "name": "Guardian Lord Nahma",
        "x": 420,
        "y": 145,
        "desc": "Cuore di Reshanta"
    },
    "artifact_siege": {
        "name": "Artifact Siege",
        "x": 510,
        "y": 125,
        "desc": "Artefatti di Reshanta"
    }
}

for boss_id, data in bosses.items():
    map_img = clean_base.copy()
    draw = ImageDraw.Draw(map_img)

    bx = data["x"]
    by = data["y"]

    # Disegna cerchi concentrici di attenzione (pulsing radar radar rosso/oro)
    draw.ellipse((bx - 26, by - 26, bx + 26, by + 26), outline=(239, 68, 68, 120), width=3)
    draw.ellipse((bx - 18, by - 18, bx + 18, by + 18), outline=(245, 158, 11, 200), width=2)

    # Incolla il marker del boss
    mw, mh = marker_rgba.size
    map_img.paste(marker_rgba, (bx - mw // 2, by - mh // 2), marker_rgba)

    # Badge con nome del Boss
    label = f"BOSS: {data['name']}"
    # Box badge
    box_w = len(label) * 8 + 16
    box_h = 24
    box_x = max(10, min(width - box_w - 10, bx - box_w // 2))
    box_y = max(10, by - 44 if by > 50 else by + 30)

    # Disegna badge scuro con bordo dorato
    draw.rectangle((box_x, box_y, box_x + box_w, box_y + box_h), fill=(17, 22, 29, 230), outline=(245, 158, 11), width=2)
    draw.text((box_x + 8, box_y + 4), label, fill=(255, 255, 255))

    out_file = os.path.join(MAPS_DIR, f"{boss_id}.png")
    map_img.save(out_file, "PNG")
    print(f"[OK] Generata mappa con marker: {out_file}")

print("Tutte le mappe sono state generate con successo!")
