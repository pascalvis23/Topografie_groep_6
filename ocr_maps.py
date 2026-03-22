"""
OCR op de 'namen' kaartafbeeldingen om stadsnamen + exacte posities te vinden.
Vergelijkt OCR-resultaten met de bekende lijsten en schrijft provinces.js.
"""
import easyocr
import cv2
import numpy as np
import json
import os
import re

MAPS_DIR = r"C:\Software\Topografiekaart_6\app\public\maps"
OUT_JSON  = r"C:\Software\Topografiekaart_6\ocr_results.json"

# Bekende stadsnamen per les (voor matching)
STEDEN_PER_LES = {
    1: ["Steenwijk","Giethoorn","Hardenberg","Kampen","Zwolle","Ommen",
        "Deventer","Nijverdal","Almelo","Rijssen","Oldenzaal","Hengelo",
        "Enschede","Haaksbergen"],
    2: ["Zierikzee","Domburg","Veere","Middelburg","Goes","Yerseke",
        "Vlissingen","Breskens","Terneuzen","Hulst"],
    3: ["Roodeschool","Appingedam","Delfzijl","Groningen",
        "Hoogezand-Sappemeer","Winschoten","Haren","Roden","Zuidlaren",
        "Veendam","Assen","Stadskanaal","Borger","Ter Apel","Beilen",
        "Westerbork","Hoogeveen","Emmen","Klazienaveen","Meppel",
        "Coevorden","Schoonebeek"],
    4: ["Urk","Emmeloord","Dronten","Lelystad","Almere","Zeewolde",
        "Amersfoort","Soest","De Bilt","Woerden","Utrecht","Zeist",
        "Nieuwegein","Veenendaal","Grebbeberg"],
    5: ["Bergen op Zoom","Roosendaal","Waalwijk","'s-Hertogenbosch","Oss",
        "Oisterhout","Kaatsheuvel","Breda","Boxtel","Uden","Boxmeer",
        "Venray","Tilburg","Eindhoven","Helmond","Valkenswaart","Weert",
        "Venlo","Roermond","Sittard","Geleen","Hoensbroek","Heerlen",
        "Kerkrade","Maastricht","Valkenburg","Vaals"],
    6: ["Noordwijk","Leiden","Wassenaar","Alphen aan den Rijn",
        "Scheveningen","Den Haag","Zoetermeer","Gouda","Delft",
        "Hoek van Holland","Vlaardingen","Schiedam","Rotterdam",
        "Spijkenisse","Dordrecht","Gorinchem"],
    7: ["Texel","Den Helder","Enkhuizen","Hoorn","Alkmaar","Purmerend",
        "Volendam","IJmuiden","Zaandam","Zandvoort","Haarlem","Amsterdam",
        "Amstelveen","Schiphol","Aalsmeer","Bussum","Hilversum"],
    8: ["Dokkum","Leeuwarden","Franeker","Harlingen","Drachten","Bolsward",
        "Sneek","Joure","Heerenveen","Stavoren","Lemmer","Wolvega",
        "Vlieland","Terschelling","Ameland","Schiermonnikoog"],
    9: ["Nunspeet","Harderwijk","Nijkerk","Apeldoorn","Barneveld","Zutphen",
        "Ede","Wageningen","Arnhem","Groenlo","Doetinchem","Winterswijk",
        "Tiel","Elst","Zevenaar","Nijmegen"],
}

# Les-ID → bestandsnaam afbeelding
LES_FILES = {
    1: "les1_overijssel_namen.png",
    2: "les2_zeeland_namen.png",
    3: "les3_groningen_drenthe_namen.png",
    4: "les4_flevoland_utrecht_namen.png",
    5: "les5_brabant_limburg_namen.png",
    6: "les6_zuidholland_namen.png",
    7: "les7_noordholland_namen.png",
    8: "les8_fryslan_namen.png",
    9: "les9_gelderland_namen.png",
}

def normalize(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

def best_match(ocr_text, candidates, threshold=0.6):
    """Fuzzy match OCR tekst naar bekende stadsnaam."""
    ocr_norm = normalize(ocr_text)
    best_score = 0
    best_name = None
    for cand in candidates:
        cand_norm = normalize(cand)
        # Substring match
        if ocr_norm in cand_norm or cand_norm in ocr_norm:
            score = len(ocr_norm) / max(len(cand_norm), 1)
            if score > best_score:
                best_score = score
                best_name = cand
        # Levenshtein-achtige: hoeveel tekens overlappen
        overlap = sum(1 for c in ocr_norm if c in cand_norm)
        score2 = overlap / max(len(cand_norm), 1)
        if score2 > best_score and score2 > threshold:
            best_score = score2
            best_name = cand
    return best_name, best_score

print("EasyOCR initialiseren (eerste keer duurt even)...")
reader = easyocr.Reader(['nl', 'en'], gpu=False, verbose=False)

all_results = {}

for les_id, filename in LES_FILES.items():
    img_path = os.path.join(MAPS_DIR, filename)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Les {les_id}: bestand niet gevonden: {img_path}")
        continue

    h, w = img.shape[:2]
    steden = STEDEN_PER_LES[les_id]
    print(f"\nLes {les_id} ({filename}): OCR uitvoeren...")

    # OCR uitvoeren
    results = reader.readtext(img_path, detail=1, paragraph=False)

    found = {}
    all_texts = []

    for (bbox_pts, text, conf) in results:
        if conf < 0.2:
            continue
        # bbox_pts = [[x0,y0],[x1,y1],[x2,y2],[x3,y3]]
        xs = [p[0] for p in bbox_pts]
        ys = [p[1] for p in bbox_pts]
        cx = (min(xs) + max(xs)) / 2 / w * 100
        cy = (min(ys) + max(ys)) / 2 / h * 100
        x0_pct = round(min(xs) / w * 100, 1)
        x1_pct = round(max(xs) / w * 100, 1)   # rechter rand = waar de marker-* staat
        all_texts.append({
            "text": text,
            "x":  round(cx, 1),    # midden
            "x0": x0_pct,          # linker rand
            "x1": x1_pct,          # rechter rand ≈ positie van de kaartmarkerdot (na de naam)
            "y":  round(cy, 1),
            "conf": round(conf, 2)
        })

        # Match tegen bekende steden
        matched, score = best_match(text, steden)
        if matched and score > 0.55 and matched not in found:
            found[matched] = {"x": round(cx, 1), "y": round(cy, 1), "conf": round(conf, 2), "ocr": text}
            print(f"  OK {matched:30s} x={cx:5.1f}%  y={cy:5.1f}%  ('{text}', score={score:.2f})")

    # Ontbrekende steden melden
    missing = [s for s in steden if s not in found]
    if missing:
        print(f"  NIET gevonden ({len(missing)}): {', '.join(missing)}")

    all_results[les_id] = {"found": found, "all_texts": all_texts}

# Sla op
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print(f"\nResultaten opgeslagen: {OUT_JSON}")
