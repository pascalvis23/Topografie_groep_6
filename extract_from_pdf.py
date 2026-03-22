"""
Extraheert stadsnamen + exacte posities rechtstreeks uit de PDF via PyMuPDF.
De tekst in de PDF heeft x,y coördinaten die we omzetten naar %-posities op de afbeelding.
"""
import fitz  # PyMuPDF
import json
import os

PDF_PATH = r"C:\Software\Topografiekaart_6\Geobas-topo6.pdf"

# Pagina-nummers (0-based) per les — pas aan als de volgorde anders is
# We inspecteren eerst alle pagina's
doc = fitz.open(PDF_PATH)

print(f"PDF heeft {len(doc)} pagina's\n")

# ─── Stap 1: Dump alle tekst per pagina met posities ──────────────────────────
all_pages = []
for page_num in range(len(doc)):
    page = doc[page_num]
    w, h = page.rect.width, page.rect.height

    # Haal alle tekstblokken op met coördinaten
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

    texts = []
    for block in blocks:
        if block["type"] != 0:  # 0 = tekst
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                txt = span["text"].strip()
                if not txt:
                    continue
                bbox = span["bbox"]  # (x0, y0, x1, y1) in PDF punten
                cx = (bbox[0] + bbox[2]) / 2  # centrum x
                cy = (bbox[1] + bbox[3]) / 2  # centrum y
                x_pct = round(cx / w * 100, 1)
                y_pct = round(cy / h * 100, 1)
                size = round(span["size"], 1)
                texts.append({
                    "text": txt,
                    "x": x_pct,
                    "y": y_pct,
                    "size": size,
                    "bbox": [round(b, 1) for b in bbox]
                })

    all_pages.append({
        "page": page_num + 1,
        "width": w,
        "height": h,
        "texts": texts
    })

doc.close()

# ─── Stap 2: Print overzicht per pagina ───────────────────────────────────────
for pg in all_pages:
    print(f"\n{'='*60}")
    print(f"PAGINA {pg['page']}  ({pg['width']:.0f} x {pg['height']:.0f} pt)")
    print(f"{'='*60}")
    # Sorteer op y dan x (van boven naar beneden, links naar rechts)
    sorted_texts = sorted(pg["texts"], key=lambda t: (t["y"], t["x"]))
    for t in sorted_texts:
        print(f"  [{t['x']:5.1f}%, {t['y']:5.1f}%]  sz={t['size']:4.1f}  \"{t['text']}\"")

# ─── Stap 3: Sla op als JSON voor verdere verwerking ─────────────────────────
out_json = r"C:\Software\Topografiekaart_6\pdf_texts.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(all_pages, f, ensure_ascii=False, indent=2)
print(f"\nJSON opgeslagen: {out_json}")
